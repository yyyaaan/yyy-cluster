<template>
  <div class="chat-about-me">
    <require-login v-if="!isAuthOk" @auth-state="isAuthOk = $event" />

    <div v-if="isAuthOk">
      <chat-main-code />
    </div>

  </div>
</template>

<script>
import RequireLogin from '@/components/RequireLogin.vue';
import ChatMainCode from '@/components/ChatMainCode.vue';

export default {
  name: 'CodeBotView',

  components: {
    RequireLogin,
    ChatMainCode,
  },

  data() {
    return {
      isAuthOk: false,
    };
  },
};
</script>

<style scoped></style>
