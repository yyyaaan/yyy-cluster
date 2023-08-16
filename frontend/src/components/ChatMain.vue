<template>
  <div class="chat">

    <chat-config-panel
      @config-updated="chatConfig=$event"
      @on-error="message=$event"
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

      <div v-if="streamText" class="col s9">
        <div class="card-panel grey lighten-5" style="white-space: wrap">
          <div class="progress cyan lighten-5">
            <div class="indeterminate cyan lighten-4"></div>
          </div>
          {{ streamText }}
        </div>
      </div>

      <chat-set-collection
        v-if="blockedByDocSelection"
        @collection-updated="setCollectionFromEvent"
        @on-error="message=$event"
      />

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

    <p class="mute"><small>{{tooltipMessage}}</small></p>

    <div id="popup-message" v-if="message">
      <div @click="message = ''" class="card yellow lighten-5">
        <p class="card-content orange-text">
          {{ message }}
        </p>
        <div class="card-action"><a href="#" @click="message = ''">Close</a></div>
      </div>
    </div>
    <!-- eslint-enable vuejs-accessibility/click-events-have-key-events max-len -->
  </div>
</template>

<script>
import ChatConfigPanel from '@/components/ChatConfigPanel.vue';
import ChatSetCollection from '@/components/ChatSetCollection.vue';

export default {
  name: 'ChatPanel',

  components: {
    ChatConfigPanel,
    ChatSetCollection,
  },

  props: {
    endpoint: String,
    initialMessage: String,
    tooltipMessage: String,
    requireDocSelection: Boolean,
  },

  data() {
    return {
      message: '',
      // from components
      chatConfig: {}, // see chat config panel
      selectedCollection: 'default', // see chat collection
      selectedCollectionOrigin: '',
      //
      blockedByDocSelection: this.requireDocSelection,
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
    setCollectionFromEvent(event) {
      this.selectedCollection = event.selectedCollection;
      this.selectedCollectionOrigin = event.selectedCollectionOrigin;
      // eslint-disable-next-line no-undef
      M.toast({ html: `knowledge learned from &nbsp; <i>${this.selectedCollection}</i> ${this.selectedCollectionOrigin}` });
      this.blockedByDocSelection = 0;
      this.chat[0].content += `\n\nKnowledge from "${this.selectedCollection}" is now available.`;
    },

    async sendInput() {
      if (this.userInput.length < 10) {
        // eslint-disable-next-line no-undef
        M.toast({ html: 'question seems too short!' });
        return;
      }
      if (this.userInput.length > 2500) {
        this.message = 'Input exceeding allowed length (2500 characters)';
        return;
      }
      this.scrollToBottom();
      this.isSendingInput = 1;

      const collection = this.selectedCollection;
      const llmModel = this.chatConfig.selectedModel;
      const response = await fetch(`${window.apiRoot}${this.endpoint}`, {
        method: 'POST',
        headers: this.authHeaders,
        body: `{"question": "${encodeURIComponent(this.userInput)}", "collection": "${collection}", "temperature": ${this.chatConfig.selectedTemperature}, "model": "${llmModel}"}`,
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
        tags: this.assignTags(collection, llmModel),
      });
      this.streamText = '';
      this.scrollToBottom();
    },

    assignTags(collection, llmModel) {
      const tags = [];
      if (this.selectedCollectionOrigin.length) {
        tags.push(`source: ${this.selectedCollectionOrigin}`);
      } else if (collection !== 'default') {
        tags.push(`source: ${collection}`);
      }
      if (llmModel && llmModel !== 'gpt-3.5-turbo') { tags.push(llmModel); }
      return tags;
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
#popup-message {
  z-index: 999999;
  position: fixed;
  top: 300px;
  width: 60%;
}
.progress {
  margin: -25px 0 15px 0;
}
</style>
