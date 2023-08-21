<template>
  <div id="login-controller">

    <!-- v-show applied over v-if for Tooltip to be initialized -->
    <div v-show="!username" id="login-prompt" class="row">
      <div class="col s12">
        Sign in with
      </div>
      <div class="col s4 tooltipped" data-position="bottom" data-tooltip="Sign in with Google">
        <a :href="urlLoginGoogle" class="btn white cyan-text">
          <img src="@/assets/logo-google.svg" alt="Sign in with Google">
        </a>
      </div>
      <div class="col s4 tooltipped" data-position="bottom" data-tooltip="Sign in with Github">
        <a :href="urlLoginGithub" class="btn white cyan-text">
          <!-- <i class="fab fa-github"></i> git -->
          <img src="@/assets/logo-github.svg" alt="Sign in with Github">
        </a>
      </div>
      <div class="col s4 tooltipped" data-position="bottom" data-tooltip="Sign in with Microsoft">
        <a :href="urlLoginMicrosoft" class="btn white cyan-text">
          <img src="@/assets/logo-microsoft.svg" alt="Sign in with Microsoft">
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
const callbackParam = `callback=${window.location.protocol}//${window.location.host}/vue-auth-callback`;

export default {
  name: 'LoginController',

  data() {
    return {
      urlLoginGoogle: `${window.apiRoot}/login/google?${callbackParam}`,
      urlLoginGithub: `${window.apiRoot}/login/github?${callbackParam}`,
      urlLoginMicrosoft: `${window.apiRoot}/login/microsoft?${callbackParam}`,
      username: '.',
    };
  },

  created() {
    this.refreshToken();
    const currentUrl = window.location.pathname;
    if (currentUrl.match('callback|profile|login')) {
      console.log('no next url');
    } else {
      window.localStorage.setItem('nextUrl', currentUrl);
    }
  },

  methods: {
    emitLoginData() {
      // called in refreshToken
      if (this.username) {
        window.localStorage.setItem('user', this.username);
      } else {
        window.localStorage.removeItem('user');
      }
      this.$emit('login-updated', this.username);
    },

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
          this.emitLoginData();
        })
        .catch((error) => {
          this.username = '';
          this.emitLoginData();
          console.error(error);
        });
    },

    logout() {
      window.localStorage.removeItem('jwt');
      window.localStorage.removeItem('user');
      window.localStorage.removeItem('renewedOn');
      setTimeout(() => { window.location.href = '/'; }, 999);
    },
  },
};
</script>

<style scoped>
#login-prompt .btn {
  width: 100%;
  margin-top: 10px;
  padding: 6px 6px;
}
#login-prompt {
  padding: 20px;
  text-align: center;
  text-transform: uppercase;
  font-size: 0.8rem;
}
#login-control{
  padding: 30px;
}
a.btn > img {
  height: 100%;
}
</style>
