<template>
<!-- eslint-disable vuejs-accessibility/click-events-have-key-events max-len -->
  <div id="chat-set-doc" class="row">
    <div class="col s9 push-s3">
      <div  class="card-panel grey lighten-5" >
        <div v-if="isLoading" class="col s12">
          <div class="progress"><div class="indeterminate"></div></div>
          <p>reading webpage and embedding the words... please wait</p>
        </div>

        <div v-else-if="!showSetURL">
          <p>Choose existing document</p>
          <a v-for="c in collections" :key="c" class="chip" @click="selectedCollection=c">
            {{ c }} &nbsp;&nbsp; <i class="tiny material-icons">close</i>
          </a>
          <!-- <label for="select-collection">
            Choose an existing document:
            <select id="select-collection" class="browser-default" v-model="selectedCollection">
            <option v-for="c in collections" :key="c" :value="c">{{ c }}</option>
            </select>
          </label> -->
        </div>

        <div v-else class="row" style="white-space: pre-wrap">
          <div class="col s10">
              <input v-model="inputURL" id="input-url" placeholder="paste the web URL here" />
          </div>
          <div class="col s2 btn-small" @click="retrieveFromURL">set</div>
        </div>

        <p class="right-align" style="margin-bottom:0px">
          <a  @click="showSetURL=1-showSetURL">
            <span v-if="showSetURL">or, choose from existing documents</span>
            <span v-else>or, use a new webpage/document</span>
          </a>
        </p>

      </div>
    </div>
  </div>

</template>

<script>
export default {
  name: 'ChatSetCollection',

  data() {
    return {
      isLoading: 0,
      inputURL: '',
      showSetURL: 0,
      collections: ['a', 'b', 'c'],
      selectedCollection: 'default',
      authHeaders: {
        Authorization: `Bearer ${window.localStorage.getItem('jwt')}`,
        Connection: 'keep-alive',
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    };
  },

  mounted() {
    fetch(`${window.apiRoot}/bot/list-collections`, { method: 'GET', headers: this.authHeaders })
      .then((response) => {
        if (response.ok) return response.json();
        throw new Error(`failed to list collections ${response.status}`);
      })
      .then((data) => { this.collections = data; })
      .catch((error) => { console.error(error); });
  },

  watch: {
    /* eslint-disable no-unused-vars */
    selectedCollection(_newVal, _oldVal) { this.emitConfig(); },
    /* eslint-enable no-unused-vars */
  },

  methods: {
    emitConfig() {
      this.$emit('collection-updated', {
        selectedCollection: this.selectedCollection,
        selectedCollectionOrigin: this.inputURL,
      });
    },

    retrieveFromURL() {
      let theUrl = null;
      try {
        document.getElementById('input-url').classList.remove('invalid');
        theUrl = new URL(this.inputURL);
      } catch (err) {
        document.getElementById('input-url').classList.add('invalid');
        return;
      }

      this.isLoading = 1;
      let collectionName = window.localStorage.getItem('user') || 'unknown';
      collectionName = `${collectionName.toLowerCase()}_u_`;
      collectionName += window.prompt('This action may take a few minutes.\nPlease provide a collection name.');
      collectionName = collectionName.replaceAll(' ', '_');

      fetch(`${window.apiRoot}/bot/create-vector-collection`, {
        method: 'POST',
        headers: this.authHeaders,
        body: `{"source_file": "${theUrl.href}", "collection_name": "${collectionName}", "is_web_url": 1}`,
      })
        .then((response) => {
          if (response.ok) { return response.json(); }
          throw new Error(`failed to create vector collection ${response.status}`);
        })
        .then((data) => {
          console.log(data);
          this.isLoading = 0;
          this.selectedCollection = collectionName;
        })
        .catch((error) => { this.isLoading = 0; console.error(error); });
    },
  },

};
</script>

<style scoped>
select, .mute {
  color: lightgray;
}
</style>
