<template>
  <div id="login-callback" class="container">
    <h5>{{msg}}</h5>

  </div>
</template>

<script>
export default {
  name: 'LoginCallbackView',
  data() {
    return {
      msg: 'Processing call back for login...',
    };
  },
  mounted() {
    const params = this.$route.fullPath.split('?').pop();

    fetch(`${window.apiRoot}/auth/token?${params}&callback=${window.location.protocol}//${window.location.host}/vue-auth-callback`)
      .then((response) => {
        if (response.ok) return response.json();
        response.text().then((text) => { this.onFailed(text); });
        throw new Error('failed to login');
      })
      .then((data) => {
        window.localStorage.setItem('jwt', data.access_token);
        window.localStorage.setItem('renewedOn', (new Date()).toISOString());
        this.msg = 'Login ok.';
        this.onSuccessConditionalRedirect(data.access_token);
      })
      .catch((error) => { console.error(error); });
  },
  methods: {
    onFailed(text) {
      this.msg = `Login Failed: ${text}`;
      setTimeout(() => { window.location.href = window.localStorage.getItem('nextUrl') || '/'; }, 5000);
    },

    onSuccessConditionalRedirect(jwt) {
      // new user must go to profile page to accept
      // new user has no access to refresh token but ok to visit profile
      fetch(`${window.apiRoot}/auth/token/refresh`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${jwt}` },
      })
        .then((response) => {
          const nextUrl = response.ok ? window.localStorage.getItem('nextUrl') : '/profile';
          this.msg = response.ok ? 'Welcome back!' : 'Hello new user!';
          setTimeout(() => { window.location.href = nextUrl || '/'; }, 500);
        })
        .catch((error) => { console.error(error); });
    },
  },
};
</script>
