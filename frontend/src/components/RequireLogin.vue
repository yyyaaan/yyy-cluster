<template>
  <!-- eslint-disable max-len -->
  <div id="login-required">

    <div v-if="!activeUser">
      <h3>Authentication required</h3>
      <p>
        Please use the side navigation panel to login.
        <pre>Admin required = {{ requireAdmin }}</pre>
      </p>
      <blockquote style="margin-top: 100px">
          Why login is required?<br/>
          In short, it is to promote fair and responsible use of AI tools. <br/><br/>
          AI can be used to create fake content, spread misinformation, and harass people.
          Anonymous usage tends to sacrifice responsible usage, and thus have a negative impact on the safety and security of the internet.
      </blockquote>
    </div>

    <div v-else-if="!isAdmin">
      <h3> Unauthorized - admin required</h3>
      <p> {{activeUser}} is authenticated but does not hold administrative privilege.</p>
    </div>

   <div v-else>
      <p> Welcome {{activeUser}} </p>
    </div>

  </div>
  <!-- eslint-enable max-len -->
</template>

<script>
// does not check from API if admin is not necessary, otherwise POST

export default {
  name: 'RequireLogin',
  props: {
    requireAdmin: Boolean,
  },
  data() {
    return {
      activeUser: window.localStorage.getItem('user'),
      isAdmin: true, // always true if admin not required
    };
  },
  mounted() {
    if (this.requireAdmin) {
      fetch(`${window.apiRoot}/bot/admin`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${window.localStorage.getItem('jwt')}` },
      })
        .then((response) => {
          if (response.ok) {
            this.$emit('auth-state', true);
            return NaN;
          }
          throw new Error('Admin required, but user is not.');
        })
        .catch((error) => {
          this.isAdmin = false;
          this.$emit('auth-state', false);
          console.error(error);
        });
    } else {
      this.$emit('auth-state', Boolean(this.activeUser));
    }

    // emit status
  },
};
</script>
