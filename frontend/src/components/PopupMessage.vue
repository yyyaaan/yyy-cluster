<template>
  <!-- eslint-disable vuejs-accessibility/click-events-have-key-events -->
  <div id="popup-message" v-if="displayMessage">
    <div @click="displayMessage = ''" class="card" :class="this.bgcolor">
      <div class="card-content" :class="this.color">
        Error: {{ displayMessage }}
      </div>
      <div class="card-action"><a @click="displayMessage = ''">Close</a></div>
    </div>
  </div>
  <!-- eslint-enable vuejs-accessibility/click-events-have-key-events -->
</template>

<script>
export default {
  name: 'PopupMessage',

  props: {
    message: String,
    bgcolor: { type: String, default: 'yellow lighten-5' },
    color: { type: String, default: 'orange-text' },
  },

  data() {
    return {
      displayMessage: '',
    };
  },

  mounted() {
    this.displayMessage = this.message;
  },

};
</script>

<style scoped>
#popup-message {
  z-index: 999999;
  position: fixed;
  top: 300px;
  width: 60%;
}
</style>
