<template>
  <div class="chat-about-me">
    <chat-main
      endpoint="/bot/stream/chat-document"
      initial-message="Welcome!
I am a chatbot that can help reading a document
You may use any preferred language."
      tooltip-message="
Kindly note that though instructed to be precise and fact-based, LLM can occasionally be wrong."
      :allow-db-selection="false"
      :require-doc-selection="true"
    />
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
