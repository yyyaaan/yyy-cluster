<template>
  <div id="chat-about-me">
    <p>
      &nbsp;
      <a href="/llm-design"><i class="material-icons">account_tree</i>
      Chat Flow Design (for non-langchain)</a>
      &nbsp;
      <a href="/chat-codebase"><i class="material-icons">integration_instructions</i>
      Chat about how am I built</a>
    </p>

    <chat-main
      endpoint="/bot/stream/chat-about-me"
      initial-message="Welcome!
I am a chatbot that can tell about Yan Pan.
You may use any preferred language."
      tooltip-message="
Kindly note that though instructed to be precise and fact-based,
LLM can occasionally present inaccurate information."
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

<style scoped>
#chat-about-me {
  margin-top: 3%;
}
</style>
