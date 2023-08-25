<template>
  <div id="ai-toolbox-view">

    <div class="row" v-for="(roadmap, iRoadmap) in roadmaps" :key="iRoadmap">
      <h3>{{ roadmap.title }}</h3>
      <p v-if="roadmap.description.length">{{ roadmap.description }}</p>
      <div class="col s3" v-for="item in roadmap.items" :key="item._id">
        <!-- eslint-disable-next-line vuejs-accessibility/click-events-have-key-events -->
        <div
          @click="openLink(item.href)"
          @mouseenter="hoveredItem=item._id" @mouseout="hoveredItem=-1"
          @focusin="hoveredItem=item._id" @focusout="hoveredItem=-1"
          :class="hoveredItem===item._id ? 'content-box z-depth-1' : 'content-box' "
        >
          <img :src="item.icon" alt="" class="card-img"><br/>
          {{ item.title }}
          <br/>{{ item.description }}
        </div>
      </div>
    </div>
    
  </div>
</template>

<script>

export default {
  name: 'ToolboxView',

  data() {
    return {
      hoveredItem: -1,
      roadmaps: [],
    };
  },

  mounted() {
    this.loadRoadmap();
  },

  methods: {
    openLink(href) {
      window.open(href, '_blank');
    },

    loadRoadmap() {
      fetch(`${window.apiRoot}/roadmap/list`)
        .then((response) => response.json())
        .then((data) => { this.roadmaps = data; })
        .catch((error) => { console.error(error); });
    },
  },
};
</script>

<style scoped>
.content-box {
  border: #eee solid 3px;
  border-radius: 6px;
  padding: 10px;
  margin: 6px 1px 6px 1px;
}
.card-img {
  max-width: 80%;
  max-height: 33px;
}
</style>
