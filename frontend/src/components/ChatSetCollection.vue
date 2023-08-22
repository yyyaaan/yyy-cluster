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
          <p v-for="(key) in Object.keys(collections)" v-bind:key="key" class="collection-item">
            Choose from <code>{{key}}</code> database: <br/>
            <a v-for="c in collections[key]" :key="c" class="chip" @click="selectedCollection=c">
              {{ c }} &nbsp;&nbsp; <i class="tiny material-icons">arrow_forward</i>
            </a>
          </p>
          <p v-if="collections.length === 0">no existing docs found</p>
          <!-- <label for="select-collection">
            Choose an existing document:
            <select id="select-collection" class="browser-default" v-model="selectedCollection">
            <option v-for="c in collections" :key="c" :value="c">{{ c }}</option>
            </select>
          </label> -->
        </div>

        <div v-else class="row" style="white-space: pre-wrap">
          <div class="col s8">
              <input v-model="inputURL" id="input-url" placeholder="paste the web URL here" />
          </div>
          <div class="col s2">
            <label for="select-model">
              <select id="select-model" class="browser-default" v-model="selectedVectorDatabase">
                <option v-for="v in vectorDatabases" :key="v" :value="v">{{ v }}</option>
              </select>
            </label>
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
      collections: { 'db-1': ['a', 'b', 'c'], 'db-2': ['x', 'y', 'z'] },
      selectedCollection: 'default',
      vectorDatabases: ['chroma', 'elasticsearch'],
      selectedVectorDatabase: 'chroma',
      userPrefix: `${(window.localStorage.getItem('user') || 'unknown').toLowerCase().replace(' ', '_')}_u_`,
      authHeaders: {
        Authorization: `Bearer ${window.localStorage.getItem('jwt')}`,
        Connection: 'keep-alive',
        'Content-Type': 'application/json',
      },
    };
  },

  async mounted() {
    let isAdmin = false;
    const resAdmin = await fetch(`${window.apiRoot}/bot/admin`, { method: 'GET', headers: this.authHeaders });
    if (resAdmin.ok) isAdmin = true;

    fetch(`${window.apiRoot}/bot/list-collections`, { method: 'GET', headers: this.authHeaders })
      .then((response) => {
        if (response.ok) return response.json();
        throw new Error(`failed to list collections ${response.status}`);
      })
      .then((data) => {
        this.collections = {};
        // this.vectorDatabases = [];
        Object.keys(data).forEach((key) => {
          // this.vectorDatabases.push(key);
          const filteredArray = data[key].filter((val) => (isAdmin ? true : (val.startsWith(this.userPrefix) || val.startsWith('public'))));
          if (filteredArray.length > 0) this.collections[key] = filteredArray;
        });
      })
      .catch((error) => { this.emitError(error); });
    // eslint-disable-next-line prefer-destructuring
    this.selectedVectorDatabase = this.vectorDatabases[0];
  },

  watch: {
    /* eslint-disable no-unused-vars */
    selectedCollection(_newVal, _oldVal) { this.emitConfig(); },
    /* eslint-enable no-unused-vars */
  },

  methods: {
    emitError(message) { this.$emit('on-error', `ChatSetCollection: ${message}`); },

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
      let collectionName = this.userPrefix;
      collectionName += window.prompt('This action may take a few minutes.\nPlease provide a collection name.');
      collectionName = collectionName.replaceAll(' ', '_');

      fetch(`${window.apiRoot}/bot/create-vector-collection`, {
        method: 'POST',
        headers: this.authHeaders,
        body: `{"source_file": "${theUrl.href}", "collection_name": "${collectionName}", "database": "${this.selectedVectorDatabase}","is_web_url": 1}`,
      })
        .then((response) => {
          if (response.ok) { return response.json(); }
          throw new Error(`failed to create vector collection ${response.status}`);
        })
        .then((data) => {
          this.isLoading = 0;
          this.selectedCollection = collectionName;
          // eslint-disable-next-line no-undef
          M.toast({ html: data.message });
        })
        .catch((error) => { this.isLoading = 0; this.emitError(error); });
    },
  },

};
</script>

<style scoped>
select, .mute {
  color: lightgray;
}
</style>
