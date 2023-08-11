<template>
  <div id="login-controller">

    <div v-if="!username" id="login-prompt" class="row">
      <div class="col s12">
        <a :href="urlLoginGoogle" class="btn white cyan-text">
          <i class="fab fa-google"></i> Login with Google
        </a>
      </div>
      <div class="col s12">
        <a :href="urlLoginGithub" class="btn white cyan-text">
          <i class="fab fa-github"></i> Login with Github
        </a>
      </div>
    </div>

    <div v-if="username" id="login-control" class="row">
      <div class="col s8">Welcome {{ username }}</div>
      <div class="col s2 tooltipped" data-position="top" data-tooltip="Profile">
        <a href="/profile">
          <i class="material-icons">person_outline</i>
        </a>
      </div>
      <div class="col s2 tooltipped" data-position="top" data-tooltip="Logout">
        <a @click="logout" href="#">
          <i class="material-icons">logout</i>
        </a>
      </div>
    </div>
  </div>
</template>

<script>
const urlRefresh = `${window.apiRoot}/auth/token/refresh`;

export default {
  name: 'LoginController',

  data() {
    return {
      urlLoginGoogle: `${window.apiRoot}/login/google?callback=http://${window.location.host}/vue-auth-callback`,
      urlLoginGithub: `${window.apiRoot}/login/github?callback=http://${window.location.host}/vue-auth-callback`,
      username: '.',
    };
  },

  mounted() {
  },

  created() {
    this.refreshToken();
    const currentUrl = window.location.pathname;
    if (currentUrl.includes('callback') || currentUrl.includes('profile')) {
      console.log('no next url');
    } else {
      window.localStorage.setItem('nextUrl', currentUrl);
    }
  },

  methods: {
    refreshToken() { // called by fetchInfo and accept
      fetch(urlRefresh, {
        method: 'POST',
        headers: { Authorization: `Bearer ${window.localStorage.getItem('jwt')}` },
      })
        .then((response) => {
          if (response.ok) return response.json();
          throw new Error('unable to refresh token');
        })
        .then((data) => {
          this.username = data.fullname;
          window.localStorage.setItem('jwt', data.access_token);
          window.localStorage.setItem('renewedOn', (new Date()).toISOString());
        })
        .catch((error) => {
          this.username = '';
          console.error(error);
        });
    },

    logout() {
      window.localStorage.removeItem('jwt');
      setTimeout(() => { window.location.href = '/'; }, 999);
    },
  },
};
</script>

<style scoped>
#login-prompt .btn {
  width: 100%;
  margin-top: 10px;
}
#login-control {
  padding: 30px;
}
</style>
