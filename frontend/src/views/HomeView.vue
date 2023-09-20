<template>
<div id="home">
  <div id="main-1" class="row">
    <div id="bg-img">
      <img src="@/assets/theme.png" alt="light theme image background"/>
    </div>

    <div class="row">
      <h1>y...</h1>
    </div>

    <!-- eslint-disable max-len -->
    <div class="row main-nav-wrapper hide-on-large-only">
      <div class="col s12 m4 xl2">
        <a href="#" data-target="slide-out" class="sidenav-trigger waves-effect waves-light btn-flat">
          <i class="material-icons">menu</i>menu
        </a>
      </div>

      <div class="col s12 m4">
        <a href="/chat-about-yan" class="waves-effect waves-light btn-flat">
          <i class="material-icons left">3p</i>Chat-About-Me
        </a>
      </div>

      <div class="col s12 m4 hide-on-small-only">
        <a class="dropdown-trigger btn-flat" href="#" data-target="main-nav-dropdown">
          <i class="material-icons">arrow_drop_down_circle</i>more
        </a>

        <ul id="main-nav-dropdown" class="dropdown-content" tabindex="0">
          <li tabindex="0">
            <a href="/chat-doc"><i class="material-icons left">question_answer</i>Chat with document</a>
          </li>
          <li tabindex="0">
            <a href="http://yan.fi/vision/"><i class="material-icons left">panorama</i>AI Vision</a>
          </li>

          <li class="divider" tabindex="-1"></li>
          <li tabindex="0">
            <a href="#!"><i class="material-icons">undo</i>Back</a>
          </li>
        </ul>
      </div>
    </div>

    <p class="about-me">
      <a href="about/"><i class="material-icons">assignment_ind</i>Yan Pan - About Me</a>
    </p>
  </div>

  <div id="main-2" class="row">
    <div class="col m3 s12 col-hover">
      <!-- empty -->
    </div>

    <div class="col m1 s12">
      <!-- column divider -->
    </div>

    <div class="col m4 s6 col-hover">
      <p><a href="http://yan.fi/shiny/resources/tvSOBI/"><i class="material-icons">school</i>tvSOBI - Thesis</a></p>
      <p><a href="http://yan.fi/vision/"><i class="material-icons">panorama</i>AI Vision</a></p>
      <p style="margin:2rem"></p>
      <p><a href="/llm-design"><i class="material-icons">account_tree</i> Chat Flow Design</a></p>
      <p><a href="/toolbox"><i class="material-icons left">collections_bookmark</i> Toolbox Catalog</a></p>
    </div>

    <div class="col m4 s6 col-hover" id="gen-ai-tools">
      <p><a href="/chat-log"><i class="material-icons left">biotech</i> Smart Log Analyzer</a></p>
      <p><a href="/llm-admin"><i class="material-icons left">admin_panel_settings</i> LLM Admin</a></p>
      <p style="margin:2rem"></p>
      <p><a href="/chat-doc"><i class="material-icons left">question_answer</i> Chat with Document</a></p>
      <p><a href="/code-bot"><i class="material-icons left">auto_fix_high</i> Code Analysis Bot</a></p>
      <p><a href="/chat-codebase"><i class="material-icons left">integration_instructions</i> How am I built</a></p>

    </div>

  </div>
  <!-- eslint-enable max-len -->
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
  .col-hover > p {
    line-height: 2rem;
    margin: 2px;
  }
  #bg-img {
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
  .main-nav-wrapper {
    /*not on large*/
    margin: 5% 5% 5% 5%;
    border-radius: 6px;
    border: 9px solid #d2fbff;
    background-color: #d2fbff;
    border-radius: 6px;
  }
  .main-nav-wrapper > div.col {
    /*not on large*/
    height: 80px;
    background-color: #d2fbff;
  }
  .main-nav-wrapper > div.col > a {
    /*not on large*/
    height: 100%;
    width: 100%;
    color: #25c0cb;
    padding-top: 15px;
    font-size: 1.2rem;
    font-weight: 600;
  }
  #main-nav-dropdown {
    /*not on large*/
    width: 220px !important;
  }
  a > i.material-icons {
    margin-right: 8px;
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
