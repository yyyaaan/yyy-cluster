<template>
  <div class="about">
    <!-- eslint-disable-next-line max-len -->
    <!-- eslint-disable vuejs-accessibility/alt-text vuejs-accessibility/form-control-has-label vuejs-accessibility/click-events-have-key-events -->
    <div class="row">
      <div id="container-left" class="col s4">
        <div id="cv-info" class="card">
          <div class="card-image" @dblclick="showProfile=1-showProfile;">
            <img src="../assets/theme.png" alt="theme picture">
          </div>
          <div class="card-content">
            <select
              class="browser-default"
              v-if="showProfile"
              v-model="selectedProfile"
              @change="loadAll"
            >
              <option v-for="opt in profiles" :key="opt" :value="opt">{{opt}}</option>
            </select>

            <ul>
              <li v-for="(i, indexPersonalInfo) in personalInfo" :key="indexPersonalInfo">
                <a :href="i.href">
                  <i class="material-icons">{{i.icon}}</i>{{i.text}}
                </a>
              </li>
              <li style="margin-top: 50px">
                <a href="http://chat.yan.fi">
                  <i class="material-icons">record_voice_over</i>&nbsp;chat.yan.fi
                  <br />
                  Experience the New Era, chat about my Experience using LLM.<br />
                </a>
              </li>
            </ul>
          </div>

          <div class="card-action">
            <div class="row">
              <div v-for="(badge, indexBadge) in badges" :key="indexBadge" class="col l1 m2 s3">
                <a target="_blank" :href="badge.href">
                  <img :src="badge.img" style="width: 150%" alt="badge image"/>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div id="container-right" class="col s8">
        <div class="card">
          <div class="card-content">
            <h4 class="right-align">
              Yan Nathan Pan <i class="material-icons">pages</i>
            </h4>
            <div v-html="summaryHTML"></div>
          </div>
        </div>
      </div>

      <div id="container-bottom" class="col s12">
        <div v-for="(one, indexMainContent) in mainContent" :key="indexMainContent" class="card">
          <div class="card-content">
            <h4 class="right-align">
              {{one.title}} <i class="material-icons">{{one.titleIcon}}</i>
            </h4>
            <div class="row" v-for="(item, indexItem) in one.items" :key="indexItem">
              <div class="col s3">
                <p style="margin-top: 20px; font-weight: bold">{{item.company}}</p>
                <p style="margin-top: 10px">{{item.time}}</p>
              </div>
              <div class="col s9 item-box">
                <h5>{{item.title}}</h5>
                <p class="valign-wrapper">
                  <span class="chip" v-for="(x, ix) in item.chips" :key="ix">{{x}}</span>
                </p>
                <p v-if="item.text" class="valign-wrapper">
                  <span v-html="item.text"></span>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div id="certs" class="col s6">
        <ul class="collapsible z-depth-1">
          <li>
            <div class="collapsible-header" tabindex="0">
              <h5>Certifications &amp; Specializations</h5>
            </div>
          </li>
          <li>
            <div class="collapsible-header" tabindex="0">
              <img src="@/assets/logo-microsoft.svg" alt="Microsoft"
              style="height:1.5rem; margin-right:20px;">
              Microsoft Certified Azure Solutions Architect Expert<br/>
              Microsoft Certified Data Scientist<br />
              Microsoft Certified AI Engineer <br />
              Microsoft Certified Azure Administrator <br/>
              Microsoft Certified Azure Data Engineer
            </div>
            <div class="collapsible-body row">
              <div v-for="(badge, indexBadge) in badges" :key="indexBadge">
                <div
                  class="col s4 center-align"
                  v-if="badge.img.includes('azure') || badge.img.includes('image.png')"
                >
                  <a target="_blank" :href="badge.href">
                    <img :src="badge.img" style="width: 80px" alt="badge image" />
                  </a>
                </div>
              </div>
            </div>
          </li>
          <li v-for="(cert, indexCert) in certs" :key="indexCert">
            <div class="collapsible-header" tabindex="0">
              <span v-html="cert.icon_tag"></span>
              {{cert.title}} <small> {{cert.title_extra}}</small>
              <span
                class="badge blue lighten-5"
                v-bind:data-badge-caption="cert.courses.split('|').length > 1? 'courses' : 'course'"
              >
                {{cert.courses.split('|').length}}
              </span>
            </div>

            <div class="collapsible-body row">
              <div class="col s5" @click="openLink(cert.verify_link)">
                <p class="right-align">by <i>{{cert.issuer}}</i></p>
                <p class="center-align">
                  <img
                    style="width: 98%"
                    v-bind:src="'https://yan.fi/static/yancv/thumbnails/' + cert.imgname"
                  />
                  <a target="_blank" v-bind:href="cert.verify_link"
                    ><i class="material-icons tiny">open_in_new</i> Verify</a
                  >
                </p>
              </div>
              <div class="col s7">
                <ul class="browser-default">
                  <li v-for="(course, iC) in cert.courses.split('|')" :key="iC">{{course}}</li>
                </ul>
              </div>
            </div>
          </li>
        </ul>
      </div>
      <!-- end of div id=certs -->

      <div id="education" class="col s6">
        <ul class="collapsible z-depth-1">
          <li>
            <div class="collapsible-header" tabindex="0">
              <h5>Education & Academics</h5>
            </div>
          </li>
          <li class="active">
            <div class="collapsible-header" tabindex="0">
              <i class="material-icons">school</i>M.Sc. Statistics
              <span class="badge deep-orange lighten-4" data-badge-caption="ECTs"
                >122</span
              >
            </div>
            <div class="collapsible-body row" style="display: block">
              <div class="col s9">
                <p>
                  Filosofian maisterin tutkinto - tilastotieteen maisteriohjelma<br />Subject
                  studies completed partially in Finnish
                  <i> (Grade: Very Good/Kiitetävä)</i>
                </p>
                <p>
                  Thesis:
                  <a href="https://jyx.jyu.fi/handle/123456789/68203"
                    >Time-Varying Source Separation by Joint Diagonlization on
                    Autocovariances </a
                  ><i>(Grade: Very Good/Kiitetävä)</i>
                </p>
              </div>
              <div class="col s3">
                <img
                  style="margin-top: 20px; width: 99%"
                  src="https://www.jyu.fi/fi/yliopistopalvelut/viestintapalvelut/logot/jyu-vaaka-kaksikielinen.jpg"
                />
              </div>
            </div>
          </li>
          <li class="active">
            <div class="collapsible-header" tabindex="0">
              <i class="material-icons">business_center</i>M.Sc. Economics and
              Business Administration
              <span class="badge deep-orange lighten-4" data-badge-caption="ECTs"
                >132</span
              >
            </div>
            <div class="collapsible-body row">
              <div class="col s9">
                <p>
                  Master of Science (Economics and Business Administration<br />Subject
                  studies completed in English <i> (Grade: Very Good)</i>
                </p>
                <p>
                  Thesis:
                  <a href="https://jyx.jyu.fi/handle/123456789/60668"
                    >Innovation in Complex Adaptive System: an exploratory study in
                    mobile phone industry </a
                  ><i> (Grade: Good)</i>
                </p>
              </div>
              <div class="col s3">
                <img
                  style="margin-top: 20px; width: 99%"
                  src="https://www.jyu.fi/fi/yliopistopalvelut/viestintapalvelut/logot/jyu-vaaka-kaksikielinen.jpg"
                />
              </div>
            </div>
          </li>

          <li class="active">
            <div class="collapsible-header" tabindex="0">
              <i class="material-icons">library_books</i>Publications and Researches
            </div>
            <div class="collapsible-body">
              <p>
                Pan, Y., Matilainen, M., Taskinen, S., &amp; Nordhausen, K. (2021).
                A review of second‐order blind identification methods.
                <i>Wiley Interdisciplinary Reviews: Computational Statistics</i>,
                e1550.
                <a href="https://onlinelibrary.wiley.com/doi/full/10.1002/wics.1550"
                  >doi:10.1002/wics.1550</a
                >
              </p>
              <p>
                Check out my homepage <a href="http://yan.fi">yan.fi</a> for funny
                real-life projects
              </p>
            </div>
          </li>
        </ul>
      </div>
    </div>
    <!-- eslint-disable-next-line max-len -->
    <!-- eslint-enable vuejs-accessibility/alt-text vuejs-accessibility/form-control-has-label vuejs-accessibility/click-events-have-key-events -->
  </div>
</template>

<script>

export default {
  name: 'AboutView',

  data() {
    return {
      showProfile: 0,
      profiles: ['default', 'scientist', 'engineer', 'architect'],
      selectedProfile: 'default',
      personalInfo: [],
      badges: [],
      summaryHTML: '<i>loading<i>',
      mainContent: [],
      certs: [],
    };
  },

  beforeCreate() {
    document.getElementById('main-contents').classList.remove('pad-for-sidenav');
    document.getElementById('slide-out').classList.remove('sidenav-fixed');
    /* eslint-disable-next-line no-undef */
    M.AutoInit();
  },

  mounted() {
    this.loadAll();
  },

  methods: {
    loadAll() {
      this.loadPersonal();
      this.loadContexts();
      this.loadCerts();
      /* eslint-disable-next-line no-undef */
      M.Collapsible.init(document.querySelectorAll('.collapsible'), { accordion: false });
    },

    loadPersonal() {
      fetch(`${window.apiRoot}/about/personal?profile=${this.selectedProfile}`)
        .then((response) => response.json())
        .then((data) => {
          this.personalInfo = data.personalInfo;
          this.badges = data.badges;
          this.profiles = data.profiles;
        })
        .catch((error) => { console.error(error); });
    },

    loadContexts() {
      fetch(`${window.apiRoot}/about/contexts?profile=${this.selectedProfile}`)
        .then((response) => response.json())
        .then((data) => {
          this.summaryHTML = data.summaryHTML;
          this.mainContent = data.mainContent;
        })
        .catch((error) => { console.error(error); });
    },

    loadCerts() {
      fetch(`${window.apiRoot}/about/certs`)
        .then((response) => response.json())
        .then((data) => {
          this.certs = data.certlist;
        })
        .catch((error) => { console.error(error); });
    },

  },
};
</script>

<style scoped>
  .container {
    width: 99%;
  }
  h3,
  h4,
  h5 {
    color: #039be5;
    text-transform: uppercase;
    font-weight: 500;
  }
  h3 {
    font-size: 2rem;
  }
  h4 {
    font-size: 1.5rem;
  }
  h5 {
    font-size: 1.2rem;
    margin: 0.5rem 0 0.5rem 0;
  }
  div#container-right p {
    margin-bottom: 10px;
    /* font-size: larger; */
  }
  i.material-icons {
    color: #039be5;
  }
  .item-box i.material-icons {
    color: lightgrey;
  }
  #cv-info i.material-icons {
    padding: 1rem 1rem 1rem 0;
  }
  .item-box {
    padding-left: 20px;
    margin: 10px 0px 10px 0px;
    border-left: #d2fbff solid 3px;
  }
  ul.collapsible,
  .badge {
    font-size: smaller;
  }
  div.collapsible-body {
    padding: 0.5rem 1rem 0 1rem;
  }
</style>
