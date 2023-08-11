<template>
  <div class="about">
    <h1>This is an about page</h1>
  </div>
</template>

<script>

export default {
  name: 'AboutView',

  data() {
    return {
    };
  },

  beforeCreate() {
    // hide navbar
    document.getElementById('main-contents').classList.remove('pad-for-sidenav');
    document.getElementById('slide-out').classList.remove('sidenav-fixed');
    // eslint-disable-next-line no-undef
    M.AutoInit();
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
