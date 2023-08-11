<template>
  <div id="llm-admin">
    <require-login :require-admin="true" @auth-state="isAuthOk=$event" />
    <div v-if="isAuthOk">
      <h1>LLM Admin</h1>
    </div>
  </div>
</template>

<script>
import RequireLogin from '../components/RequireLogin.vue';

export default {
  name: 'LLMAdminView',

  components: {
    RequireLogin,
  },

  data() {
    return {
      isAuthOk: false,
    };
  },

  created() {
  },

  mounted() {
  },

  methods: {
  },
};
</script>

<style scoped>
</style>
