<template>
  <div class="chat-about-me">
    <require-login :require-admin="false" @auth-state="isAuthOk = $event" />

    <div v-if="isAuthOk">
      <chat-panel
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

  </div>
</template>

<script>
import RequireLogin from '@/components/RequireLogin.vue';
import ChatPanel from '@/components/ChatPanel.vue';

export default {
  name: 'ChatMeView',

  components: {
    RequireLogin,
    ChatPanel,
  },

  data() {
    return {
      isAuthOk: false,
    };
  },

  created() {},

  mounted() {},

  methods: {},
};
</script>

<style scoped></style>
