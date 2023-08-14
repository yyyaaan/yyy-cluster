<template>
  <div id="llm-admin">
    <require-login :require-admin="true" @auth-state="isAuthOk = $event"/>

    <div v-if="isAuthOk">
      <h3>LLM Bot Admin Panel</h3>
      <!-- eslint-disable
      vuejs-accessibility/click-events-have-key-events
      vuejs-accessibility/form-control-has-label-->
      <div id="info" class="row">
        <div id="row-info">
          <div v-if="message" @click="message=''" class="card yellow lighten-5">
            <div class="card-content orange-text">{{message}}<br><small>{{debug}}</small></div>
            <div class="card-action"><a @click="message=''">Close</a></div>
          </div>
        </div>

        <div v-if="isLoading" class="col s12">
          <div class="progress"><div class="indeterminate"></div></div>
        </div>

        <div class="col s12">

          <div class="card">
            <div class="card-content orange-text">
              <div v-for="f in files" :key="f" class="chip">
                {{ f }} &nbsp;&nbsp;&nbsp;
                <i class="tiny material-icons" @click="createCollection(f)">add_to_photos</i>
                &nbsp;
                <i class="tiny material-icons" @click="deleteFile(f)">close</i>
              </div>
            </div>
            <div class="card-action">
              Available Files &nbsp;&nbsp;
              <a v-if="!showUpload" @click="showUpload = 1">upload new</a>
              <a v-if="showUpload" @click="showUpload = 0">collapse</a>
              <div v-if="showUpload" id="upload-file" class="row">
                <div class="file-field input-field">
                  <div class="btn-small">
                    <span>upload</span>
                    <input type="file" @change="handleFileUpload" />
                  </div>
                  <div class="file-path-wrapper">
                    <input class="file-path validate" type="text" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col s12">
          <div class="card">
            <div class="card-content orange-text">
              <div v-for="c in collections" :key="c" class="chip">
                {{ c }} &nbsp;&nbsp;&nbsp;
                <i class="tiny material-icons" @click="deleteCollection(c)">close</i>
              </div>
            </div>
            <div class="card-action">
              Embedded Vector Collections &nbsp;&nbsp;
              <a v-if="!showUpload" @click="showUpload = 1">info</a>
              <a v-if="showUpload" @click="showUpload = 0">collapse</a>
              <blockquote v-if="showUpload">required: <code>aboutme</code></blockquote>
            </div>
          </div>
        </div>

        <div class="col s12">
          <div class="card">
            <div class="card-content orange-text">
              <pre id="log-content">
                {{ logContent.join('\n') }}
              </pre>
            </div>
            <div class="card-action">
              Server log reverse-chronologically &nbsp;&nbsp;
              <a v-if="!showLogFiles" @click="showLogFiles = 1">more logs...</a>
              <a v-if="showLogFiles" @click="showLogFiles = 0">collapse</a>
              <blockquote v-if="showLogFiles" id="log-selection">
                <a v-for="l in logFiles" :key="l" @click="selectedLog = l">
                  {{ l }}
                </a>
              </blockquote>
            </div>
          </div>
        </div>

      </div>
      <!-- eslint-enable
      vuejs-accessibility/click-events-have-key-events
      vuejs-accessibility/form-control-has-label-->

    </div>
  </div>
</template>

<script>
import RequireLogin from '@/components/RequireLogin.vue';

export default {
  name: 'LLMAdminView',

  components: {
    RequireLogin,
  },

  data() {
    return {
      isAuthOk: false,
      authHeaders: {},
      files: ['ad.pdf', 'bc.daf'],
      collections: ['a', 'b'],
      logFiles: ['log1', 'log2'],
      logContent: ['line1', 'line2'],
      selectedLog: '',
      showLogFiles: 0,
      showUpload: 0,
      isLoading: 0,
      message: '',
      debug: '',
    };
  },

  watch: {
    selectedLog(preLog, newLog) {
      this.message = `Set log to ${newLog} was ${preLog}`;
      this.listLogs();
      setTimeout(() => { this.message = ''; }, 2600);
    },
  },

  mounted() {
    this.authHeaders = {
      accept: 'application/json',
      Authorization: `Bearer ${window.localStorage.getItem('jwt')}`,
      'Content-Type': 'application/json',
    };
    this.listCollections();
    this.listFiles();
    this.listLogs();
  },

  methods: {
    handleResponse(response) {
      if (response.ok) return response.json();
      // if (response.status === 401) this.authFailed = true;
      throw new Error(`${response.status}`);
    },

    createCollection(f) {
      const collectionName = window.prompt('This action may take a few minutes.\nPlease provide a collection name.', f);
      console.log(`from ${f} to create ${collectionName}`);
      this.isLoading = 1;

      fetch(`${window.apiRoot}/bot/create-vector-collection`, {
        method: 'POST',
        headers: this.authHeaders,
        body: `{"source_file": "${f}", "collection_name": "${collectionName}"}`,
      })
        .then((response) => {
          if (response.ok) return response.json();
          throw new Error(`${response.status}`);
        })
        .then((data) => {
          this.message = data.message;
          this.listFiles();
          this.listCollections();
          this.isLoading = 0;
        })
        .catch((error) => {
          this.isLoading = 0;
          error.json().then((json) => {
            this.message = `Creation failed! ${json.detail}`;
          });
        });
    },

    listFiles() {
      fetch(`${window.apiRoot}/bot/list-uploaded-files`, { method: 'GET', headers: this.authHeaders })
        .then((response) => {
          if (response.ok) return response.json();
          throw new Error(`${response.status}`);
        })
        .then((data) => { this.files = data; })
        .catch((error) => { this.message = error; });
    },

    listCollections() {
      fetch(`${window.apiRoot}/bot/list-collections`, { method: 'GET', headers: this.authHeaders })
        .then((response) => {
          if (response.ok) return response.json();
          throw new Error(`${response.status}`);
        })
        .then((data) => { this.collections = data; })
        .catch((error) => { this.message = error; });
    },

    listLogs() {
      fetch(`${window.apiRoot}/bot/log?filename=${this.selectedLog}`, {
        method: 'GET',
        headers: this.authHeaders,
      })
        .then((response) => {
          if (response.ok) return response.json();
          throw new Error(`${response.status}`);
        })
        .then((data) => {
          this.logFiles = data.available;
          this.logContent = data.log.reverse();
        })
        .catch((error) => { this.message = error; });
    },

    deleteFile(f) {
      if (window.confirm(`Are your sure to permanently delete '${f}'`)) {
        this.isLoading = 1;
        fetch(`${window.apiRoot}/bot/delete-file`, {
          method: 'POST',
          headers: this.authHeaders,
          body: `{"filename": "${f}"}`,
        })
          .then((response) => {
            if (response.ok) return response.json();
            throw new Error(`${response.status}`);
          })
          .then((data) => {
            this.message = data.message;
            this.listFiles();
            this.isLoading = 0;
          })
          .catch((error) => {
            this.isLoading = 0;
            this.message = error;
          });
      }
    },

    deleteCollection(c) {
      if (window.confirm(`Are your sure to permanently delete vector database "${c}"`)) {
        this.isLoading = 1;
        fetch(`${window.apiRoot}/bot/delete-vector-collection`, {
          method: 'POST',
          headers: this.authHeaders,
          body: `{"collection_name": "${c}"}`,
        })
          .then((response) => {
            if (response.ok) return response.json();
            throw new Error(`${response.status}`);
          })
          .then((data) => {
            this.message = data.message;
            this.listCollections();
            this.isLoading = 0;
          })
          .catch((error) => {
            this.isLoading = 0;
            this.message = error;
          });
      }
    },

    handleFileUpload(event) {
      const file = event.target.files[0];
      const formData = new FormData();
      formData.append('file', file);

      fetch(`${window.apiRoot}/bot/upload`, { method: 'POST', body: formData })
        .then((response) => {
          if (response.status === 413) {
            this.message = 'Fail! file size too large!';
          } else if (response.status < 300) {
            this.message = 'upload completed ok.';
          } else {
            this.message = 'Warning: unknown exception';
          }
          this.listFiles();
          this.listCollections();
        })
        // .then(data => this.message = data)
        .catch((error) => { this.message = error; });
    },
  },
};
</script>

<style scoped>
.chip {
  font-size: larger;
}
#log-selection {
  overflow: auto;
  height: 3rem;
}
#log-content {
  font-size: smaller;
  height: 300px;
  overflow: auto;
}

</style>
