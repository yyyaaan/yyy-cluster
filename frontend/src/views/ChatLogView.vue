<template>
  <div class="chat-codebase">

    <chat-main
      endpoint="/bot/stream/chat-document"
      initial-message="Welcome!
I am able to read and analyze the recent logs for the system.
The log is saved only locally, and I may not have holistic view."
      tooltip-message="
Kindly note that though instructed to be precise and fact-based,
LLM can occasionally present inaccurate information."
      :allow-db-selection="false"
      :require-doc-selection="false"
      predefined-collection="log-rolling"
      predefined-database="chroma"
    />

  </div>
</template>

<script>
import ChatMain from '@/components/ChatMain.vue';

export default {
  name: 'ChatLogView',

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
