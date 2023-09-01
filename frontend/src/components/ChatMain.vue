<template>
  <div class="chat">

    <chat-config-panel
      @config-updated="chatConfig=$event"
      @on-error="message=$event"
    />

    <!-- eslint-disable vuejs-accessibility/click-events-have-key-events max-len -->
    <div id="chat-bubbles" class="row">
      <div
        v-for="(msg, indexMsg) in chat" :key="indexMsg"
        :class="msg.role === 'user' ? 'col s9 push-s3' : 'col s9'"
      >
        <div class="card-panel grey lighten-5" style="white-space: pre-wrap">
          {{ msg.content }}
          <div v-if="msg.sources" class="response-sources">
            Sources:<br/>
            {{msg.sources}}
            <br/>The LLM runs more restrictive when source reasoning is required.
          </div>
          <div class="right-align" v-if="msg.role != 'user'">
            <span v-if="showTags">
              <div v-for="(tag, indexTag) in msg.tags" :key="indexTag"
                class="chip" style="font-size: xx-small">
                {{ tag }}
              </div>
            </span>
            <span @click="showTags=1-showTags" style="color:lightgray;">
              &nbsp;<i class="material-icons">troubleshoot</i>
            </span>
          </div>
        </div>
      </div>

      <div v-if="streamText" class="col s9">
        <div class="card-panel grey lighten-5" style="white-space: pre-wrap">
          <div id="streaming-indicator" class="progress cyan lighten-5">
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
        <input name="user-input-box" type="text"
          v-model="userInput" @keyup.enter="sendInput"
          :disabled="isSendingInput || streamText.length"
        />
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
    predefinedCollection: { type: String, default: '' },
    predefinedDatabase: { type: String, default: '' },
  },

  data() {
    return {
      message: '',
      // from components
      chatConfig: {}, // see chat config panel
      selectedCollection: 'default', // see chat collection
      selectedCollectionOrigin: '',
      selectedDatabase: 'chroma',
      //
      blockedByDocSelection: this.requireDocSelection,
      // chat content
      authHeaders: {},
      isSendingInput: 0,
      showTags: 0,
      userInput: '',
      streamText: '',
      chat: [{ role: 'sys', content: this.initialMessage || 'initialMessage', tags: ['instruction'] }],
    };
  },

  mounted() {
    this.authHeaders = {
      Authorization: `Bearer ${window.localStorage.getItem('jwt')}`,
      Connection: 'keep-alive',
      'Content-type': 'application/json',
      'Cache-Control': 'no-cache',
    };
    // check predefined collection
    if (this.predefinedCollection && this.predefinedDatabase) {
      console.log('predefined', this.predefinedCollection, this.predefinedDatabase);
      this.selectedCollection = this.predefinedCollection;
      this.selectedDatabase = this.predefinedDatabase;
      this.blockedByDocSelection = 0;
    }
  },

  methods: {
    setCollectionFromEvent(event) {
      this.selectedCollection = event.selectedCollection;
      this.selectedCollectionOrigin = event.selectedCollectionOrigin;
      this.selectedDatabase = event.selectedDatabase;
      // eslint-disable-next-line no-undef
      M.toast({ html: `knowledge learned from &nbsp; <i>${this.selectedCollection} &nbsp;[${this.selectedDatabase}]</i> &nbsp;${this.selectedCollectionOrigin}` });
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
      const database = this.selectedDatabase;
      const llmModel = this.chatConfig.selectedModel;
      const sourceRequired = this.chatConfig.selectedSourceRequired;
      const response = await fetch(`${window.apiRoot}${this.endpoint}`, {
        method: 'POST',
        headers: this.authHeaders,
        body: `{"question": "${encodeURIComponent(this.userInput)}", "database": "${database}", "collection": "${collection}", "temperature": ${this.chatConfig.selectedTemperature}, "model": "${llmModel}", "include_source": "${sourceRequired}"}`,
      });
      this.chat.push({ role: 'user', content: this.userInput });
      this.isSendingInput = 0;

      // starting streaming
      const reader = response.body.getReader();
      this.userInput = '';
      this.streamText = ' ';
      while (true) {
        // eslint-disable-next-line no-await-in-loop
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = new TextDecoder('utf-8').decode(value);
        this.streamText += chunk;
      }

      const ResponseArray = this.streamText.split('SOURCES:');
      this.chat.push({
        role: 'sys',
        content: ResponseArray[0].trim(),
        sources: ResponseArray[1] ? ResponseArray[1].trim() : null,
        tags: this.assignTags(collection, database, llmModel),
      });
      this.streamText = '';
      this.scrollToBottom();
    },

    assignTags(collection, database, llmModel) {
      const tags = [database];
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
  color: gray;
}
.response-sources {
  font-size: smaller;
  color: darkgray;
  margin-top: 15px;
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
