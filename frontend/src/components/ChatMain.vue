<template>
  <div class="chat">

    <!-- @config-updated="chatConfig=$event;" -->
    <chat-config-panel
      @config-updated="observeConfig"
      :allow-db-selection="true"
    />

    <!-- eslint-disable vuejs-accessibility/click-events-have-key-events max-len -->
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

    <popup-message v-if="message" :message="message" />
  </div>
</template>

<script>
import PopupMessage from '@/components/PopupMessage.vue';
import ChatConfigPanel from '@/components/ChatConfigPanel.vue';

export default {
  name: 'ChatPanel',

  components: {
    ChatConfigPanel,
    PopupMessage,
  },

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
      chatConfig: {}, // see chat config panel
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
    console.log('received configuration', this.chatConfig);
  },

  methods: {
    observeConfig(event) {
      this.chatConfig = event;
      console.log('observed change', this.chatConfig);
    },

    async sendInput() {
      if (this.userInput.length < 10) {
        this.message = 'question too short.';
        return;
      }
      if (this.userInput.length > 2500) {
        this.message = 'Input exceeding allowed length (2500 characters)';
        return;
      }
      this.scrollToBottom();
      this.isSendingInput = 1;

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
