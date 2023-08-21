<template>
  <!-- eslint-disable max-len -->
  <div id="login-required">

    <div v-if="!activeUser">
      <h3>Authentication required</h3>
      <p>
        Please login<span v-if="requireAdmin"> using administrative account</span>.
        <login-controller/>
      </p>
      <blockquote style="margin-top: 50px">
        Why login is required?<br/>
        In short, it is to promote fair and responsible use of AI tools. <br/><br/>
        AI can be used to create fake content, spread misinformation, and harass people.
        Anonymous usage tends to sacrifice responsible usage, and thus have a negative impact on the safety and security of the internet. Kindly note that <code>Elastic Search</code> might have access your proxy or real IP address through <code>nginx</code> logging.
      </blockquote>
    </div>

    <div v-else-if="!isAdmin">
      <h3> Unauthorized - admin required</h3>
      <p>Please use left panel to login with different account.</p>
      <div id="login-user">
        {{activeUser}} is authenticated but does not hold administrative privilege.
      </div>
    </div>

   <div v-else id="login-user">
      <p> Welcome {{activeUser}} </p>
    </div>

  </div>
  <!-- eslint-enable max-len -->
</template>

<script>
import LoginController from '@/components/LoginController.vue';
// does not check from API if admin is not necessary, otherwise POST

export default {
  name: 'RequireLogin',

  props: {
    allowAnonymous: Boolean,
    requireAdmin: Boolean,
  },

  components: {
    LoginController,
  },

  data() {
    return {
      activeUser: window.localStorage.getItem('user'),
      isAdmin: true, // always true if admin not required
    };
  },

  mounted() {
    if (this.allowAnonymous) {
      this.activeUser = 'anonymous';
      this.$emit('auth-state', true);
    }

    if (this.requireAdmin) {
      fetch(`${window.apiRoot}/bot/admin`, {
        method: 'GET',
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
          setTimeout(() => {
            this.activeUser = window.localStorage.getItem('user');
          }, 1500); // read storage needs delay
          console.error(error);
        });
    } else {
      this.$emit('auth-state', Boolean(this.activeUser));
    }
  },
};
</script>
