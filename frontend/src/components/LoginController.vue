<template>
  <div id="login-controller">
    <div v-if="username" id="login-prompt" class="row">
      <div class="col s12">
        <a href="#" class="btn white cyan-text">
          <i class="fab fa-google"></i> Login with Google
        </a>
      </div>
      <div class="col s12">
        <a href="#" class="btn white cyan-text">
          <i class="fab fa-github"></i> Login with Github
        </a>
      </div>
    </div>
    <div v-if="username" id="login-control" class="row">
      <div class="col s8">Welcome {{ username }}</div>
      <div class="col s2 tooltipped" data-position="top" data-tooltip="Profile">
        <a href="#">
          <i class="material-icons">person_outline</i>
        </a>
      </div>
      <div class="col s2 tooltipped" data-position="top" data-tooltip="Logout">
        <a href="#">
          <i class="material-icons">logout</i>
        </a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginController',
  data() {
    return {
      username: 'a',
    };
  },
};
</script>

<style scoped>
#login-prompt .btn {
  width: 100%;
  margin-top: 10px;
}
</style>
