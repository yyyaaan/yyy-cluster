<template>
  <div id="llm-admin">
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

      <div class="col s12 right-align">
        <div class="btn-group" role="group">
          <a v-for="(key) in Object.keys(collections)" :key="key"
            :class="key===selectedVectorDatabase ? 'btn btn-large' : 'btn btn-large btn-inactive'"
            @click="selectedVectorDatabase=key"
          >
            {{key}}
          </a>
        </div>
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

      <!-- only show matched database collection -->
      <div class="col s12">
        <div class="card">
          <div class="card-content orange-text">
            <div v-for="c in collections[selectedVectorDatabase]" :key="c" class="chip">
              {{ c }} &nbsp;&nbsp;&nbsp;
              <i class="tiny material-icons" @click="deleteCollection(c)">close</i>
            </div>
          </div>
          <div class="card-action">
            Embedded Vector in <code>{{selectedVectorDatabase}}</code> &nbsp;&nbsp;
            <a v-if="!showUpload" @click="showUpload = 1">more</a>
            <a v-if="showUpload" @click="showUpload = 0">collapse</a>
            <div v-if="showUpload" style="margin-top:20px;">
              <a href="#" @click="createCodebaseVector()">
                Create CodeBase in {{selectedVectorDatabase}}
              </a>
              Create Log Vector in {{selectedVectorDatabase}}: &nbsp; &nbsp;
              <a href="#" @click="createLogVector(1)">1 day</a>
              <a href="#" @click="createLogVector(3)">3 days</a>
              <a href="#" @click="createLogVector(7)">7 days</a>
            </div>
          </div>
        </div>
      </div>

      <div class="col s12">
        <div class="card">
          <div class="card-content orange-text">
            <div v-if="isLoadingElastic" class="progress">
              <div class="indeterminate"></div>
            </div>
            <pre id="elastic-log">
              {{elasticLogContent}}
            </pre>
          </div>

          <div class="card-action">
            <div class="row">
              <div class="col s4">
                <label for="elastic-log-selector">Fluentd Log Indices
                  <select id="elastic-log-selector" class="browser-default"
                    v-model="selectedElasticLog" @change="searchElasticLog">
                      <option v-for="log in elasticLogs" :key="log" :value="log">{{log}}</option>
                  </select>
                </label>
              </div>
              <div class="col s6">
                <label for="elastic-query">Elastic Simple Search Query
                  <input id="elastic-query" type="text"
                    :disabled="isLoadingElastic"
                    v-model="elasticQuery" @keyup.enter="searchElasticLog" />
                </label>
              </div>
              <div v-show="!isLoadingElastic" class="col s2">
                <br/>
                <a class="waves-effect waves-light btn" href="#"
                  @click="searchElasticLog">Query</a>
              </div>
            </div>
          </div>

        </div>
      </div>

      <div class="col s12">
        <div class="card">
          <div class="card-content orange-text">
            <pre id="log-content">
              {{ logContent.join('\n') }}
            </pre>
            <p class="right-align">
              <a class="waves-effect waves-light btn-flat" @click="listLogs()">
                <i class="material-icons right">refresh</i>
                <small>updated {{ logUpdated }} seconds ago</small>
              </a>
            </p>
          </div>
          <div class="card-action">
            Archived log reverse-chronologically &nbsp;&nbsp;
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
</template>

<script>

export default {
  name: 'LLMAdminView',

  data() {
    return {
      authHeaders: {},
      selectedVectorDatabase: 'elasticsearch',
      files: ['ad.pdf', 'bc.daf'],
      collections: ['a', 'b'],
      logFiles: ['log1', 'log2'],
      logContent: ['line1', 'line2'],
      selectedLog: '',
      showLogFiles: 0,
      elasticQuery: 'error',
      elasticLogs: ['fluent-1', 'fluent-2'],
      selectedElasticLog: '',
      elasticLogContent: '',
      isLoadingElastic: 0,
      logUpdated: 0,
      logPoller: null,
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
    this.listElasticLogs();
    this.listLogs();
    this.searchElasticLog();
  },

  methods: {
    handleResponse(response) {
      if (response.ok) return response.json();
      // if (response.status === 401) this.authFailed = true;
      throw new Error(`${response.status}`);
    },

    createCollection(f) {
      const collectionName = window.prompt('This action may take a few minutes.\nPlease provide a collection name.', f);
      console.log(`from ${f} to create ${collectionName} on ${this.selectedVectorDatabase}`);
      this.isLoading = 1;

      fetch(`${window.apiRoot}/bot/create-vector-collection`, {
        method: 'POST',
        headers: this.authHeaders,
        body: `{"source_file": "${f}", "collection_name": "${collectionName}", "database": "${this.selectedVectorDatabase}"}`,
      })
        .then((response) => {
          if (response.ok) return response.json();
          throw new Error(`${response.status}`);
        })
        .then((data) => {
          // eslint-disable-next-line no-undef
          M.toast({ html: data.message });
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

    createLogVector(days) {
      console.log('create logs', days, 'days', this.selectedVectorDatabase);
      this.isLoading = 1;

      fetch(`${window.apiRoot}/bot/create-vector-log`, {
        method: 'POST',
        headers: this.authHeaders,
        body: `{"days": ${days}, "database": "${this.selectedVectorDatabase}"}`,
      })
        .then((response) => {
          if (response.ok) return response.json();
          throw new Error(`${response.status}`);
        })
        .then((data) => {
          // eslint-disable-next-line no-undef
          M.toast({ html: data.message });
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

    createCodebaseVector() {
      const collectionName = window.prompt('This action may take a few minutes.\nPlease provide a name (it will be prefixed with "codebase" automatically).');
      console.log('create codebase', collectionName, this.selectedVectorDatabase);
      this.isLoading = 1;

      fetch(`${window.apiRoot}/bot/create-vector-codebase`, {
        method: 'POST',
        headers: this.authHeaders,
        body: `{"collection_name": "${collectionName}", "database": "${this.selectedVectorDatabase}", "source_file": ""}`,
      })
        .then((response) => {
          if (response.ok) return response.json();
          throw new Error(`${response.status}`);
        })
        .then((data) => {
          // eslint-disable-next-line no-undef
          M.toast({ html: data.message });
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

    listElasticLogs() {
      fetch(`${window.apiRoot}/elastic/`, { method: 'GET', headers: this.authHeaders })
        .then((response) => {
          if (response.ok) return response.json();
          throw new Error(`${response.status}`);
        })
        .then((data) => {
          if (data.indices.length < 1) return;
          data.indices.sort().reverse();
          this.elasticLogs = data.indices;
          // eslint-disable-next-line prefer-destructuring
          this.selectedElasticLog = data.indices[0];
        })
        .catch((error) => { this.message = error; });
    },

    searchElasticLog() {
      this.isLoadingElastic = 1;
      fetch(`${window.apiRoot}/elastic/query?index=${this.selectedElasticLog}&query=${this.elasticQuery}`, {
        method: 'GET',
        headers: this.authHeaders,
      })
        .then((response) => {
          if (response.ok) return response.json();
          throw new Error(`${response.status}`);
        })
        .then((data) => {
          this.isLoadingElastic = 0;
          data.hits.forEach((val) => {
            this.elasticLogContent += `\n${val.sort}\n${val.fields.log.join('\n')}`;
          });
        })
        .catch((error) => { this.message = error; this.isLoadingElastic = 0; });
    },

    listLogs() {
      clearInterval(this.logPoller);
      this.logUpdated = 0;
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
          this.logPoller = setInterval(() => { this.logUpdated += 5; }, 5000);
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
            // eslint-disable-next-line no-undef
            M.toast({ html: data.message });
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
          body: `{"collection_name": "${c}", "database": "${this.selectedVectorDatabase}"}`,
        })
          .then((response) => {
            if (response.ok) return response.json();
            throw new Error(`${response.status}`);
          })
          .then((data) => {
            // eslint-disable-next-line no-undef
            M.toast({ html: data.message });
            this.listCollections();
            this.isLoading = 0;
          })
          .catch((error) => {
            this.isLoading = 0;
            // eslint-disable-next-line no-undef
            M.toast({ html: data.message });
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
#log-content, #elastic-log {
  color: #999;
  font-size: smaller;
  height: 300px;
  overflow: auto;
}
/* below is for button group */
.btn-group {
  position: relative;
  display: -ms-inline-flexbox;
  display: inline-flex;
  vertical-align: middle;
}

.btn-group>.btn:first-child:not(:last-child) {
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
}

.btn-group>.btn:not(:first-child):not(:last-child) {
  border-radius: 0;
}

.btn-group>.btn:last-child:not(:first-child),
.btn-group>.dropdown-toggle:not(:first-child) {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}

.btn-group>.btn-inactive {
  background-color: #999;
}

.btn-group>.btn {
  -webkit-box-shadow:
  0 0px 0px 0 rgba(0, 0, 0, 0), 0 0px 0px 0px rgba(0, 0, 0, 0), 0 0px 0px 0 rgba(0, 0, 0, 0);
  box-shadow:
  0 0px 0px 0 rgba(0, 0, 0, 0), 0 0px 0px 0px rgba(0, 0, 0, 0), 0 0px 0px 0 rgba(0, 0, 0, 0);
}

.btn-group>.btn-inactive:hover {
  background-color: #999;
}

.btn-group>.btn:hover {
  -webkit-box-shadow:
0 2px 2px 0 rgba(0, 0, 0, 0.14), 0 3px 1px -2px rgba(0, 0, 0, 0.12), 0 1px 5px 0 rgba(0, 0, 0, 0.2);
  box-shadow:
0 2px 2px 0 rgba(0, 0, 0, 0.14), 0 3px 1px -2px rgba(0, 0, 0, 0.12), 0 1px 5px 0 rgba(0, 0, 0, 0.2);
}
</style>
