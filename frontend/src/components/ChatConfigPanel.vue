<template>
<!-- eslint-disable vuejs-accessibility/click-events-have-key-events max-len -->
  <div id="llm-config" class="row valign-wrapper">
    <div class="col s6 right-align" @click="showConfig = 1 - showConfig">
      <p class="mute" style="text-decoration: underline">
        <span v-if="showConfig">Close </span>
        <span v-else>Open LLM Options</span>
      </p>
    </div>

    <div v-if="showConfig && allowDbSelection" class="col s3 right-align">
      <label for="select-collection">
        Vector Database Selection
        <select id="select-collection" class="browser-default" v-model="selectedCollection">
        <option v-for="c in collections" :key="c" :value="c">{{ c }}</option>
        </select>
      </label>
    </div>

    <div v-if="showConfig" class="col s3 right-align">
      <label for="select-temperature">
        LLM Temperature
        <select id="select-temperature" class="browser-default" v-model="selectedTemperature">
        <option v-for="t in [0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9]" :key="t">{{ t }}</option>
        </select>
      </label>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatConfigPanel',

  props: {
    allowDbSelection: Boolean,
  },

  data() {
    return {
      showConfig: 0,
      collections: ['a', 'b', 'c'],
      selectedCollection: 'default',
      selectedTemperature: 0.1,
      authHeaders: {
        Authorization: `Bearer ${window.localStorage.getItem('jwt')}`,
        Connection: 'keep-alive',
        Accept: 'application/json',
      },
    };
  },

  mounted() {
    if (this.allowDbSelection) {
      fetch(`${window.apiRoot}/bot/list-collections`, { method: 'GET', headers: this.authHeaders })
        .then((response) => {
          if (response.ok) return response.json();
          throw new Error(`failed to list collections ${response.status}`);
        })
        .then((data) => { this.collections = data; })
        .catch((error) => { console.error(error); });
    }
    this.emitConfig();
  },

  watch: {
    /* eslint-disable no-unused-vars */
    selectedCollection(_newVal, _oldVal) { this.emitConfig(); },
    selectedTemperature(_newVal, _oldVal) { this.emitConfig(); },
    /* eslint-enable no-unused-vars */
  },

  methods: {
    emitConfig() {
      this.$emit('config-updated', {
        selectedDb: this.selectedCollection,
        selectedTemperature: this.selectedTemperature,
      });
    },
  },

};
</script>

<style scoped>
select, .mute {
  color: lightgray;
}
</style>
