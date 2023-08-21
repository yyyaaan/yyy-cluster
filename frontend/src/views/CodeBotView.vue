<template>
  <div class="chat-about-me">
    <chat-main-code />
  </div>
</template>

<script>
import ChatMainCode from '@/components/ChatMainCode.vue';

export default {
  name: 'CodeBotView',

  components: {
    ChatMainCode,
  },

  data() {
    return {
    };
  },
};
</script>

<style scoped></style>
