<template>
  <!-- eslint-disable max-len vuejs-accessibility/click-events-have-key-events -->
  <div id="profile" class="container row">

    <div id="msg-info" class="col s12">
      <div v-if="message" @click="message=''" class="card yellow lighten-5">
          <div class="card-content orange-text">System Message<br/>{{message}}</div>
          <div class="card-action"><a @click="message=''">Close</a></div>
      </div>
    </div>

    <!-- handle first ever login -->
    <div class="col s12">
      <h3>Welcome! {{me.full_name}}</h3>
      <p v-if="!me.accepted">
        It is the first time you logged in, and we need your confirmation.
        <br/><br/>
        Below is all the info we are collecting, you can choose to agree or delete my profile
      </p>
      <p class="center-align">
        <a v-if="!me.accepted" class="waves-effect waves-light btn-large" @click="agreeNewUser">
          Agree & Continue
        </a>
        &nbsp;&nbsp;
        <a class="waves-effect waves-light btn-large red lighten-3" @click="deleteProfile">
          <i class="material-icons">delete_sweep</i> Delete My Profile
        </a>
      </p>
    </div>

    <p v-if="nextUrl && me.accepted" style="font-size: larger">You will be redirected to {{ nextUrl }} within 10 seconds...</p>

    <ul class="collection with-header" style="margin-top:60px">
      <!-- conditional: only NOT new user -->
      <li class="collection-header">
        Your Information
        <br/><small>below is all info concerned with you.</small>
      </li>

      <!-- always -->
      <li v-for="(key) in Object.keys(me)" v-bind:key="key" class="collection-item">
        <span :class="key == 'origin' ? 'grey-text' : ''">{{ me[key] }}</span>
        <br/><span class="grey-text">{{ key }}</span>
        <div class="secondary-content">
          <i class="material-icons">face</i>
        </div>
      </li>
    </ul>
  </div>
<!-- eslint-enable max-len vuejs-accessibility/click-events-have-key-events -->
</template>

<script>
const urlMe = `${window.apiRoot}/admin/user/me`;

export default {
  name: 'ProfileView',
  data() {
    return {
      headers: {},
      message: 'loading',
      nextUrl: '',
      me: {},
    };
  },

  created() {
  },

  mounted() {
    this.message = 'still loading...';
    this.headers = {
      Authorization: `Bearer ${window.localStorage.getItem('jwt')}`,
      Accept: 'application/json',
    };
    this.fetchInfoAboutMe();
  },

  methods: {
    promptError(error) {
      this.message = error;
      console.error(error);
    },

    fetchInfoAboutMe() {
      fetch(urlMe, { method: 'GET', headers: this.headers })
        .then((response) => {
          if (response.ok) return response.json();
          throw new Error(`Login Failed ${response.status}`);
        })
        .then((data) => {
          this.me = data;
          this.message = '';
        })
        .catch((error) => { this.promptError(error); });
    },

    agreeNewUser() {
      fetch(urlMe, { method: 'POST', headers: this.headers })
        .then((response) => response.json())
        .then((data) => {
          this.me = data;
          this.message = '';
          setTimeout(() => { window.location.href = window.localStorage.getItem('nextUrl') || '/'; }, 500);
        })
        .catch((error) => { this.promptError(error); });
    },

    deleteProfile() {
      // eslint-disable-next-line
      if (confirm('Do you really want to delete your profile?')) {
        fetch(urlMe, { method: 'DELETE', headers: this.headers })
          .then((response) => {
            this.message = 'Profile Deleted. ';
            this.me = {};
            window.localStorage.removeItem('jwt');
            setTimeout(() => { window.location.href = window.localStorage.getItem('nextUrl') || '/'; }, 500);
            if (!response.ok) console.error(response);
          })
          .catch((error) => { this.promptError(error); });
      }
    },
  },
};
</script>
