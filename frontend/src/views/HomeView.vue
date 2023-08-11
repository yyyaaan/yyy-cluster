<template>
<div id="home">
  <div id="main-1" class="row">
    <div id="bgimg">
      <img src="@/assets/theme.png" alt="light theme image background"/>
    </div>

    <div class="row">
      <h1>y...</h1>
    </div>

    <div class="row mainnav-wrapper hide-on-large-only">
      <div class="col s12 m4 xl2">
        <a
          href="#"
          data-target="slide-out"
          class="sidenav-trigger waves-effect waves-light btn-flat"
          ><i class="material-icons">menu</i>menu</a
        >
      </div>

      <div class="col s12 m4">
        <a href="http://yan.fi/vision/" class="waves-effect waves-light btn-flat"
          ><i class="material-icons left">panorama</i>AI Vision</a
        >
      </div>

      <div class="col s12 m4 hide-on-small-only">
        <a class="dropdown-trigger btn-flat" href="#" data-target="mainnavdrop"
          ><i class="material-icons">arrow_drop_down_circle</i>more</a
        >
        <ul id="mainnavdrop" class="dropdown-content" tabindex="0">
          <li tabindex="0">
            <a href="http://yan.fi/shiny/chaos/"
              ><i class="material-icons left">flare</i>Chaos-Theory</a
            >
          </li>

          <li tabindex="0">
            <a href="http://yan.fi/shiny/missingData/"
              ><i class="material-icons left">gradient</i>EM-Algorithm</a
            >
          </li>

          <li tabindex="0">
            <a href="http://yan.fi/my/web/"><i class="material-icons left">web</i>Reader</a>
          </li>

          <li class="divider" tabindex="-1"></li>

          <li tabindex="0">
            <a href="http://yan.fi/vms/"
              ><i class="material-icons">layers</i>Virtual Machines</a
            >
          </li>

          <li tabindex="0">
            <a href="http://yan.fi/ycrawl/"><i class="material-icons">explore</i>API Root</a>
          </li>

          <li tabindex="0">
            <a href="http://yan.fi/msg/"><i class="material-icons">message</i>Messenging</a>
          </li>

          <li tabindex="0">
            <a href="http://yan.fi/sitemap/"><i class="material-icons">map</i>Sitemap</a>
          </li>

          <li class="divider" tabindex="-1"></li>
          <li tabindex="0">
            <a href="#!"><i class="material-icons">undo</i>Back</a>
          </li>
        </ul>
      </div>
    </div>

    <p class="about-me">
      <a href="about/">
        <i class="material-icons">assignment_ind</i>
        Yan Pan - About Me
      </a>
    </p>
  </div>
  <div id="main-2" class="row">
    <div class="col m3 s12 col-hover"></div>

    <div class="col m1 s12"></div>

    <div class="col m4 s6 col-hover">
      <p></p>

      <p class="listview">
        <a href="http://yan.fi/shiny/resources/tvSOBI/">
          <i class="material-icons">school</i>
          tvSOBI - Thesis
        </a>
      </p>

      <p class="listview">
        <a href="http://yan.fi/shiny/chaos/">
          <i class="material-icons">flare</i>
          Chaos Theory
        </a>
      </p>

      <p class="listview">
        <a href="http://yan.fi/shiny/missingData/">
          <i class="material-icons">gradient</i>
          EM Algorithm Visulaized
        </a>
      </p>

      <p class="listview">
        <a href="http://yan.fi/shiny/libs/">
          <i class="material-icons">settings_input_antenna</i>
          Libs Spectrum Seperation
        </a>
      </p>

      <p class="listview" style="margin-top: 33px">
        <a href="http://yan.fi/shiny/web">
          <i class="material-icons">collections_bookmark</i>
          Academic Notebooks
        </a>
      </p>

      <p class="listview">
        <a href="http://yan.fi/shiny/tools/">
          <i class="material-icons">inbox</i>
          Toolbox
        </a>
      </p>
    </div>

    <div class="col m4 s6 col-hover">
      <p></p>

      <p class="listview">
        <a href="http://yan.fi/vision/">
          <i class="material-icons">panorama</i>
          AI Vision
        </a>
      </p>

      <p class="listview">
        <a href="http://yan.fi/my/web/">
          <i class="material-icons">web</i>
          Web Reader
        </a>
      </p>

      <p class="listview">
        <a
          href="https://datastudio.google.com/u/0/reporting/d69d4892-6779-4d66-8b38-2fee9fd00dc1/page/kE3mC"
        >
          <i class="material-icons">dashboard</i>
          Live Dashboard (external)
        </a>
      </p>

      <p class="listview">
        <a href="http://yan.fi/overview/">
          <i class="material-icons">movie_filter</i>
          Job Overview
        </a>
      </p>

      <p class="listview">
        <a href="http://yan.fi/vms/">
          <i class="material-icons">layers</i>
          Virtual Machines
        </a>
      </p>

      <p class="listview">
        <a href="http://yan.fi/ycrawl/">
          <i class="material-icons">explore</i>
          yCrawl API Root
        </a>
      </p>

      <p class="listview">
        <a href="http://yan.fi/msg/">
          <i class="material-icons">message</i>
          Messenging API
        </a>
      </p>
    </div>

    <div id="log-print" class="col container" style="display: none; margin: 9%">
      <pre></pre>
    </div>
  </div>
  <div id="main-3" class="row"></div>
</div>
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {
      apiRoot: window.apiRoot || 'undefined apiRoot',
    };
  },
  components: {
  },
  mounted() {
  },
};
</script>

<style scoped>
  pre {
    font-size: smaller;
    overflow: auto;
    word-wrap: normal;
  }
  h2 {
    font-size: 2.56rem;
  }
  select {
    display: block;
  }
  .pad-for-sidenav {
    padding-left: 300px;
  }
  @media only screen and (max-width: 992px) {
    .pad-for-sidenav {
      padding-left: 0;
    }
  }
  .col-hover {
    opacity: 0.3;
  }
  .col-hover:hover {
    opacity: 0.8;
  }
  #bgimg {
    position: fixed;
    top: 34%;
    left: 0%;
    width: 100%;
    height: 66%;
    opacity: 0.06;
    z-index: -9999;
  }
  #bgimg > img {
    width: 100%;
    height: 100%;
  }
  #the-menu {
    display: none;
  }
  .mainnav-wrapper {
    /*not on large*/
    margin: 5% 5% 5% 5%;
    border-radius: 6px;
    border: 9px solid #d2fbff;
    background-color: #d2fbff;
    border-radius: 6px;
  }
  .mainnav-wrapper > div.col {
    /*not on large*/
    height: 80px;
    background-color: #d2fbff;
  }
  .mainnav-wrapper > div.col > a {
    /*not on large*/
    height: 100%;
    width: 100%;
    color: #25c0cb;
    padding-top: 15px;
    font-size: 1.2rem;
    font-weight: 600;
  }
  #mainnavdrop {
    /*not on large*/
    width: 220px !important;
  }
  a > i.material-icons {
    margin-right: 8px;
  }
  p.listview {
    margin: 2px;
  }
  p.about-me {
    margin: 0% 5% 9% 5%;
    text-align: right;
  }
  p.about-me > a,
  h1 {
    color: #6ae5ee;
  }
  h1 {
    font-size: 8rem;
    font-weight: 600;
    text-align: right;
    margin: 12% 5% 1% 10%;
    border-bottom: 9px #d2fbff solid;
    padding-bottom: 50px;
  }
  @media only screen and (max-width: 992px) {
    h1 {
      text-align: center;
      margin: 3% 0% 0% 3%;
      color: #6ae5ee;
      font-size: 6rem;
      border-bottom: none;
      padding-bottom: 10px;
    }
    p.about-me {
      text-align: left;
    }
    .col-hover {
      opacity: 0.8;
    }
  }
</style>
