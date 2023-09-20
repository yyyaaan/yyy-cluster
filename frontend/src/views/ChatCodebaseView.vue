<template>
  <div class="chat-codebase">

    <chat-main
      endpoint="/bot/stream/chat-document"
      initial-message="Welcome!
I can tell about how the API backend is built, for specific questions.
For example &#34;describe the token generation steps&#34;

The code base is saved only locally, and I may not have holistic view on the code base."
      tooltip-message="
Kindly note that though instructed to be precise and fact-based,
LLM can occasionally present inaccurate information."
      :allow-db-selection="false"
      :require-doc-selection="false"
      predefined-collection="codebase-default"
      predefined-database="elasticsearch"
    />

  </div>
</template>

<script>
import ChatMain from '@/components/ChatMain.vue';

export default {
  name: 'ChatCodebaseView',

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
