<template>
  <div class="chat">
    <!-- eslint-disable vuejs-accessibility/click-events-have-key-events max-len -->
    <div id="row-info">
      <div v-if="message" @click="message = ''" class="card yellow lighten-5">
        <div class="card-content orange-text">
          Error: {{ message }}<br /><small>{{ debug }}</small>
        </div>
        <div class="card-action"><a @click="message = ''">Close</a></div>
      </div>
    </div>

    <div id="llm-config" class="row valign-wrapper">
      <div class="col s6 right-align" @click="showConfig = 1 - showConfig">
        <p class="mute" style="text-decoration: underline">
          <span v-if="showConfig">Close </span>
          <span v-else>Open LLM Options</span>
        </p>
      </div>

      <div v-if="showConfig && allowDbSelection" class="col s3 right-align">
        <label for="select-collection">
          Vector Database Selection
          <select id="select-collection" class="browser-default" v-model="selectedCollection">
            <option v-for="c in collections" :key="c" :value="c">{{ c }}</option>
          </select>
        </label>
      </div>

      <div v-if="showConfig" class="col s3 right-align">
        <label for="select-temperature">
          LLM Temperature
          <select id="select-temperature" class="browser-default" v-model="selectedTemperature">
            <option v-for="t in [0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9]" :key="t">{{ t }}</option>
          </select>
        </label>
      </div>
    </div>

    <div id="chat-bubbles" class="row">
      <div
        v-for="(msg, indexMsg) in chat"
        :key="indexMsg"
        :class="msg.role === 'user' ? 'col s9 push-s3' : 'col s9'"
      >
        <div class="card-panel grey lighten-5" style="white-space: pre-wrap">
          {{ msg.content }}
          <br />
          <div class="right-align">
            <div
              v-for="(tag, indexTag) in msg.tags"
              :key="indexTag"
              class="chip"
              style="font-size: xx-small"
            >
              {{ tag }}
            </div>
          </div>
        </div>
      </div>

      <div v-if="blockedByDocSelection" id="require-doc" class="col s9 push-s3">
        <div v-if="isLoadingUrlContent" class="col s12">
          <div class="progress"><div class="indeterminate"></div></div>
          <p>reading webpage and embedding the words... please wait</p>
        </div>

        <div v-if="!isLoadingUrlContent" class="card-panel grey lighten-5" style="white-space: pre-wrap">
          <div class="row">
            <div class="col s10">
              <input v-model="inputURL" placeholder="paste the web URL here" />
            </div>
            <div class="col s2 btn-small" @click="setInputURL">set</div>
          </div>
        </div>
      </div>

      <div v-if="streamText" class="col s9">
        <div class="card-panel grey lighten-5" style="white-space: wrap">
          {{ streamText }}
        </div>
      </div>
    </div> <!--end of require-doc-->

    <div v-if="!blockedByDocSelection" id="chat-input" class="row valign-wrapper">

      <div class="input-field col s10">
        <!-- eslint-disable-next-line vuejs-accessibility/form-control-has-label -->
        <input name="user-input-box" type="text" v-model="userInput" @keyup.enter="sendInput" />
      </div>
      <div v-if="!isSendingInput" class="col s2" @click="sendInput">
        <i class="material-icons" style="font-size: 30px; color: lightblue">send</i>
      </div>
      <div v-else class="col s2">
        <div class="progress"><div class="indeterminate"></div></div>
      </div>

    </div>
    <!-- eslint-enable vuejs-accessibility/click-events-have-key-events max-len -->

  </div>
</template>

<script>
export default {
  name: 'ChatPanel',

  props: {
    endpoint: String,
    initialMessage: String,
    tooltipMessage: String,
    allowDbSelection: Boolean,
    requireDocSelection: Boolean,
    // if true, later step needs to change blockedByDocSelection
  },

  data() {
    return {
      message: '',
      // configs
      showConfig: 0,
      collections: ['a', 'b', 'c'],
      selectedCollection: 'default',
      selectedTemperature: 0.1,
      // file input reuquired
      blockedByDocSelection: this.requireDocSelection,
      isLoadingUrlContent: 0,
      inputURL: '',
      // chat content
      authHeaders: {},
      isSendingInput: 0,
      userInput: '',
      streamText: '',
      chat: [{ role: 'sys', content: this.initialMessage || 'initialMessage', tags: [] }],
    };
  },

  mounted() {
    this.authHeaders = {
      Authorization: `Bearer ${window.localStorage.getItem('jwt')}`,
      Connection: 'keep-alive',
      'Content-type': 'application/json',
      'Cache-Control': 'no-cache',
    };
  },

  methods: {
    async sendInput() {
      this.scrollToBottom();
      this.isSendingInput = 1;
      if (this.userInput.length < 10) {
        this.message = 'question too short.';
        return;
      }
      if (this.userInput.length > 2500) {
        this.message = 'Input exceeding allowed length (2500 characters)';
        return;
      }

      const collection = this.selectedCollection;
      const response = await fetch(`${window.apiRoot}${this.endpoint}`, {
        method: 'POST',
        headers: this.authHeaders,
        body: `{"question": "${encodeURIComponent(this.userInput)}", "collection": "${collection}", "temperature": ${this.selectedTemperature}, "model": "gpt-4"}`,
      });
      this.chat.push({ role: 'user', content: this.userInput });
      this.isSendingInput = 0;

      // starting streaming
      this.userInput = '';
      const reader = response.body.getReader();
      while (true) {
        // eslint-disable-next-line no-await-in-loop
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = new TextDecoder('utf-8').decode(value);
        this.streamText += chunk;
      }

      this.chat.push({
        role: 'sys',
        content: this.streamText,
        tags: this.assignTags(collection),
      });
      this.streamText = '';
      this.scrollToBottom();
    },

    assignTags(collection) {
      if (this.inputURL.length) {
        return [`source: ${this.inputURL}`, `${this.selectedCollection.replace('tmp', '')}`];
      }
      if (collection === 'default') {
        return [];
      }
      return [`source: ${collection}`];
    },

    scrollToBottom() {
      setTimeout(() => {
        // eslint-disable-next-line no-undef
        // M.textareaAutoResize(document.getElementById('code-input'));
        document.getElementById('chat-input').scrollIntoView({ behavior: 'smooth', block: 'end' });
      }, 1200);
    },
  },

};
</script>

<style scoped>
.chat-card {
  border-radius: 15px;
  padding: 10px;
  border: powderblue solid 3px;
  margin-top: 10px;
}
select, .mute {
  color: lightgray;
}
</style>
