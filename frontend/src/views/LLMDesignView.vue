<template>
  <div id="llm-design-view">
    <h3>LLM Design</h3>
    <ul class="collapsible popout">
      <li id="schema">
        <div class="collapsible-header" tabindex="0">
          <i class="material-icons">table_chart</i>Vector Database Schema
        </div>
        <div class="collapsible-body">
          <table class="striped">
            <thead>
              <tr>
                  <th>Field</th>
                  <th>Properties</th>
                  <th>Description</th>
              </tr>
            </thead>

            <tbody>
              <tr>
                <td>id</td>
                <td><code>id</code></td>
                <td>primary key to identify the record</td>
              </tr>
              <tr>
                <td>Content</td>
                <td><code>string</code> searchable</td>
                <td>the original text, supports semantic search
                  <br/>the content would be stuffed to LLM when necessary</td>
              </tr>
              <tr>
                <td>Vector</td>
                <td><code>vector</code> vector-searchable</td>
                <td>the 1536-dimensional vector representation of <code>Content</code>
                  <br/>supports the similarity search</td>
              </tr>
              <tr>
                <td>SourceId</td>
                <td><code>string</code> filterable</td>
                <td>hex-identifier of a unique source documents</td>
              </tr>
              <tr>
                <td>TokenCount</td>
                <td><code>int</code></td>
                <td>the number of tokens the chunk contains
                  <br/>help check if contents could be stuffed
                </td>
              </tr>
              <tr>
                <td>Category</td>
                <td><code>int/string</code> filterable</td>
                <td>indicates the group of source document
                  <br/>e.g. credibility, visibility, validity</td>
              </tr>
              <tr>
                <td>MetaFields</td>
                <td><code>string</code></td>
                <td>a few fields that stores metadata, e.g. title, filename, etc.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </li>

      <li class="active">
        <div class="collapsible-header" tabindex="0">
          <i class="material-icons">account_tree</i>Chat Flow: Router, Stuff, Map-Reduce
        </div>
        <div class="collapsible-body">
          <iframe
            title="llm-design-chart"
            frameborder="0" style="width:99%;height:60vh;"
            src="https://embeds.onemodel.app/d/iframe/qREurfehzaJuyk4J2bkizeg3CnugQ4mLKuU0TjiPJFJBHZIe0tmj4Ekw8NBp"
          >
          <!-- src="https://viewer.diagrams.net/?tags=%7B%7D&highlight=0000ff&layers=1&nav=1&title=Chat%20Engineering#Uhttps%3A%2F%2Fdrive.google.com%2Fuc%3Fid%3D13eDgugZjlXX9a6HL_2TiYhO2RLZquK75%26export%3Ddownload"> -->
          </iframe>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'LLMDesignView',

  data() {
    return {
      hoveredItem: -1,
      showMermaidGist: 0,
      roadmaps: [],
    };
  },

  beforeMount() {
  },

  mounted() {
    // eslint-disable-next-line no-undef
    M.Collapsible.init(document.querySelector('.collapsible'), {});
  },

  methods: {

  },
};
</script>

<style scoped>
</style>
