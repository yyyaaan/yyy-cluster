<template>
  <div class="code-bot">

    <chat-config-panel
      @config-updated="chatConfig=$event"
      @on-error="message=$event"
    />

    <div v-for="(one, indexCode) in codeAnalysis" :key="indexCode" class="row">
      <div class="col s6">
        <div class="card-panel grey lighten-2 input-box">
          <pre>{{one.input}}</pre>
        </div>
      </div>
      <div class="col s6">
        <div class="card-panel grey lighten-5" style="white-space: pre-wrap">
          {{one.output}}
          <div class="right-align">
            <div v-for="(tag, indexTag) in one.tags" :key="indexTag"
              class="chip" style="font-size: xx-small">
              {{ tag }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="streamText" id="running-analysis" class="row">
      <div class="col s6">
        <div class="card-panel grey lighten-5 input-box">
          <pre>{{streamInput}}</pre>
        </div>
      </div>
      <div class="col s6">
        <div class="card-panel grey lighten-5" style="white-space: wrap">
          <div id="streaming-indicator" class="progress cyan lighten-5">
            <div class="indeterminate cyan lighten-4"></div>
          </div>
          {{ streamText }}
        </div>
      </div>
    </div>

    <!-- eslint-disable-next-line max-len -->
    <!-- eslint-disable vuejs-accessibility/click-events-have-key-events vuejs-accessibility/label-has-for -->

    <div id="chat-input" class="row valign-wrapper">
      <div class="input-field col s10">
        <textarea
          id="code-input"
          class="materialize-textarea"
          data-length="2500"
          v-model="userInput"
          v-on:keypress.ctrl.enter="sendInput"
        >
        </textarea>
        <label for="code-input">Type or Paste Code, press CTRL-Enter to send</label>
      </div>
      <div v-if="!isSendingInput" class="col s2" @click="sendInput">
        <i class="material-icons" style="font-size: 30px; color: lightblue">send</i>
      </div>
      <div v-else class="col s2">
        <div class="progress"><div class="indeterminate"></div></div>
      </div>

    </div>

    <div id="popup-message" v-if="message">
      <div @click="message = ''" class="card yellow lighten-5">
        <p class="card-content orange-text">
          {{ message }}
        </p>
        <div class="card-action"><a href="#" @click="message = ''">Close</a></div>
      </div>
    </div>

    <!-- eslint-disable-next-line max-len -->
    <!-- eslint-enable vuejs-accessibility/click-events-have-key-events vuejs-accessibility/label-has-for -->
  </div>
</template>

<script>
import ChatConfigPanel from '@/components/ChatConfigPanel.vue';

export default {
  name: 'ChatMainCode',

  components: {
    ChatConfigPanel,
  },

  data() {
    return {
      message: '',
      endpoint: '/bot/stream/code',
      // from components
      chatConfig: {}, // see chat config panel
      // chat content
      authHeaders: {},
      isSendingInput: 0,
      userInput: '',
      streamInput: '',
      streamText: '',
      codeAnalysis: [{
        input: 'console.log("hello user!")',
        output: 'Hi, I am code bot!\nI am happy to explain and analyze the code for you.',
        tags: [],
      }],
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

      const llmModel = this.chatConfig.selectedModel;
      const response = await fetch(`${window.apiRoot}${this.endpoint}`, {
        method: 'POST',
        headers: this.authHeaders,
        body: `{"code": "${encodeURIComponent(this.userInput)}", "temperature": ${this.chatConfig.selectedTemperature}, "model": "${llmModel}"}`,
      });
      this.isSendingInput = 0;

      // starting streaming
      this.streamInput = this.userInput;
      this.userInput = '';
      const reader = response.body.getReader();
      while (true) {
        // eslint-disable-next-line no-await-in-loop
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = new TextDecoder('utf-8').decode(value);
        this.streamText += chunk;
      }

      this.codeAnalysis.push({
        input: this.streamInput,
        output: this.streamText,
        tags: llmModel !== 'gpt-4o' ? [llmModel] : [],
      });
      this.streamText = '';
      this.streamInput = '';
      this.scrollToBottom();
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
.input-box {
  color: #333;
  font-size: smaller;
  white-space: pre;
  overflow: auto;
}
#code-input {
  font-family: monospace;
  font-size: smaller;
}
#popup-message {
  z-index: 999999;
  position: fixed;
  top: 300px;
  width: 60%;
}
#streaming-indicator {
  margin: -25px 0 15px 0;
}
</style>
