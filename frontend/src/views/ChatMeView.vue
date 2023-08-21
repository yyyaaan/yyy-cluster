<template>
  <div class="chat-about-me">

    <chat-main
      endpoint="/bot/stream/chat-about-me"
      initial-message="Welcome!
I am a chatbot that can tell about Yan Pan.
You may use any preferred language."
      tooltip-message="
Kindly note that though instructed to be precise and fact-based, LLM can occasionally be wrong."
      :allow-db-selection="false"
      :require-doc-selection="false"
    />

  </div>
</template>

<script>
import ChatMain from '@/components/ChatMain.vue';

export default {
  name: 'ChatMeView',

  components: {
    ChatMain,
  },

  data() {
    return {
    };
  },
};
</script>

<style scoped></style>
