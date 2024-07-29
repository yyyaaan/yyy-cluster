<template>
<!-- eslint-disable vuejs-accessibility/click-events-have-key-events max-len -->
  <div id="llm-config" class="row valign-wrapper">
    <div class="col s6 right-align" @click="showConfig = 1 - showConfig">
      <p class="mute" style="text-decoration: underline">
        <span v-if="showConfig">Close </span>
        <span v-else>Open LLM Options</span>
      </p>
    </div>

    <div v-if="showConfig" class="col s3 right-align">
       <div class="switch">
        <!-- eslint-disable-next-line vuejs-accessibility/label-has-for -->
        <label> Require Sources Info:<br/></label>
        <label for="select-source-required">
          Off
          <input id="select-source-required" type="checkbox" v-model="selectedSourceRequired">
          <span class="lever"></span>
          On
        </label>
      </div>
    </div>

    <!-- script determines if more models will be available -->
    <div v-if="showConfig && (models.length - 1)" class="col s3 right-align">
      <label for="select-model">
        Large Language Model
        <select id="select-model" class="browser-default" v-model="selectedModel">
        <option v-for="m in models" :key="m" :value="m">{{ m }}</option>
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
  },

  data() {
    return {
      showConfig: 0,
      models: ['gpt-4o'],
      selectedModel: 'gpt-4o',
      selectedTemperature: 0.1,
      selectedSourceRequired: false,
      authHeaders: {
        Authorization: `Bearer ${window.localStorage.getItem('jwt')}`,
        Connection: 'keep-alive',
        Accept: 'application/json',
      },
    };
  },

  async mounted() {
    // for admin, add gpt-4 option
    const response = await fetch(`${window.apiRoot}/bot/admin`, { method: 'GET', headers: this.authHeaders });
    if (response.ok) this.models.push('gpt-4');
    this.emitConfig();
  },

  watch: {
    /* eslint-disable no-unused-vars */
    selectedTemperature(_newVal, _oldVal) { this.emitConfig(); },
    selectedModel(_newVal, _oldVal) { this.emitConfig(); },
    selectedSourceRequired(_newVal, _oldVal) { this.emitConfig(); },
    /* eslint-enable no-unused-vars */
  },

  methods: {
    emitConfig() {
      this.$emit('config-updated', {
        selectedTemperature: this.selectedTemperature,
        selectedModel: this.selectedModel,
        selectedSourceRequired: this.selectedSourceRequired,
      });
    },
  },

};
</script>

<style scoped>
select, .mute {
  color: gray;
}
</style>
