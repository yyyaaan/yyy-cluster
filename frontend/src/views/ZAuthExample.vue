<template>
  <div class="example-only">
    <require-login :require-admin="false" @auth-state="isAuthOk = $event" />
    
    <div v-if="isAuthOk">

    </div>
  </div>
</template>

<script>
import RequireLogin from '@/components/RequireLogin.vue';

export default {
  name: "AuthExample",

  components: {
    RequireLogin,
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

<style scoped>
</style>
