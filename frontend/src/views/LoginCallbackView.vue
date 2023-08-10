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
    fetch(`http://localhost:9001/app/auth/token?${params}&redirect=false&callback=http://localhost:8080/vue-auth-callback`)
      .then((response) => {
        if (response.ok) return response.json();
        throw new Error('Login Failed');
      })
      .then((data) => {
        window.localStorage.setItem('jwt', data.access_token);
        window.localStorage.setItem('renewedOn', (new Date()).toISOString());
        this.msg = 'Login ok.';
        this.conditionalRedirect(data.access_token);
      })
      .catch((error) => {
        this.msg = error;
        console.error(error);
      });
  },
  methods: {
    conditionalRedirect(jwt) {
      // new user must go to profile page to accept
      // new user has no access to refresh token but ok to visit profile
      fetch('http://localhost:9001/app/auth/token/refresh', {
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
