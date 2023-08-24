<template>
  <div class="chat-about-me">
    <!-- eslint-disable max-len -->
    <chat-main
      endpoint="/bot/stream/chat-document"
      initial-message="Welcome!
I am a chatbot that can help reading a document
You may use any preferred language.

The provided content will be embedded to database on this server, and is not shared with GPT/Claude directly."
      tooltip-message="
Kindly note that though instructed to be precise and fact-based,
LLM can occasionally present inaccurate information."
      :allow-db-selection="false"
      :require-doc-selection="true"
    />
    <!-- eslint-enable max-len -->
  </div>
</template>

<script>
import ChatMain from '@/components/ChatMain.vue';

export default {
  name: 'ChatDocView',

  components: {
    ChatMain,
  },

  data() {
    return {
      isAuthOk: false,
    };
  },
};
</script>

<style scoped></style>
