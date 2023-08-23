<template>
  <!-- eslint-disable max-len -->
  <div id="login-required">

    <div v-if="!activeUser">
      <h3>Authentication required</h3>
      <p>
        Please login<span v-if="adminRequired"> using administrative account</span>.
        <br/>Your login credentials and 2-factor authentications are managed by the OpenId providers below. Your password is never visible to this site.
        <br/>For Microsoft login, your organization might block access and a private Microsoft account shall be used.
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
      <p>{{activeUser}} is authenticated but does not hold administrative privilege.</p>
      <p>Please use left panel to login with different account.</p>
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

  components: {
    LoginController,
  },

  data() {
    return {
      activeUser: window.localStorage.getItem('user'),
      adminRequired: false,
    };
  },

  mounted() {
    this.adminRequired = (new URLSearchParams(window.location.search)).get('adminRequired');
  },
};
</script>
