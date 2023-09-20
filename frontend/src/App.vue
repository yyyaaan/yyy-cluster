<template>
  <main>
    <ul id="slide-out" class="sidenav sidenav-fixed">
      <div class="user-view" style="height:200px">
        <div class="background">
          <img id="theme-image" src="./assets/theme.png" alt="theme picture">
        </div>
      </div>

      <!-- icons: https://fonts.google.com/icons -->

      <!-- eslint-disable max-len -->
      <!--
      <li><a href="/vision/"><i class="material-icons left">panorama</i>AI Vision</a></li>
      <li><a href="/vms/"><i class="material-icons left">layers</i>Virtual Machines</a></li>
      <li><a href="/my/web/"><i class="material-icons left">web</i>Web Reader</a></li>
      <li class="divider" tabindex="-1"></li>
      <li><a href="/shiny/resources/tvSOBI/"><i class="material-icons">school</i>tvSOBI - Thesis</a></li>
      <li><a href="/shiny/chaos/"><i class="material-icons">flare</i>Chaos Theory</a></li>
      <li><a href="/shiny/missingData/"><i class="material-icons">gradient</i>EM Algorithm Visualized</a></li>
      <li><a href="/shiny/tools/"><i class="material-icons">inbox</i>Toolbox</a></li>
      <li class="divider" tabindex="-1"></li>
      -->
      <li><a href="/about"><i class="material-icons left">assignment_ind</i>About (CV)</a></li>
      <li><a href="/chat-about-yan"><i class="material-icons left">3p</i> Chat about Yan</a></li>

      <li class="divider" tabindex="-1"></li>
      <li><a href="/chat-doc"><i class="material-icons left">question_answer</i> Chat with Document</a></li>
      <li><a href="/code-bot"><i class="material-icons left">auto_fix_high</i> Code Analysis Bot</a></li>
      <li><a href="/chat-codebase"><i class="material-icons left">integration_instructions</i> How am I built</a></li>
      <li><a href="/#gen-ai-tools"><i class="material-icons left">read_more</i> More GenAI Tools</a></li>

      <li class="divider" tabindex="-1"></li>
      <li><a href="/llm-design"><i class="material-icons">account_tree</i> Chat Flow Design</a></li>
      <li><a href="/toolbox"><i class="material-icons left">collections_bookmark</i> Toolbox Catalog</a></li>

      <!-- router-link ? -->

      <li class="divider" tabindex="-1"></li>
      <login-controller @login-updated="verifyLogin" />

      <li class="divider" tabindex="-1"></li>
      <li><a href="/"><i class="material-icons left">pages</i>Home</a></li>
      <li>
        <a onclick="M.toast({html: 'Cheers! I am a toast'})" class="waves-effect" href="#!">
        <i class="material-icons">pets</i>Have a Toast</a>
      </li>
    </ul>

    <div id="open-navbar" class="valign-wrapper">
        <a id="open-navbar-icon" href="#" data-target="slide-out" class="sidenav-trigger">
            <i class="material-icons" style="padding-top:50vh">menu</i>
        </a>
    </div>

    <div id="main-contents" class="pad-for-sidenav">
      <router-view/>
    </div>

  </main>
</template>

<script>
import LoginController from '@/components/LoginController.vue';

export default {
  name: 'IndexPage',
  components: {
    LoginController,
  },
  methods: {
    verifyLogin(name) {
      console.log('login verification', name.length);
    },
  },
};
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  margin-right: 3%;
}
h1, h2, h3, h4, h5 {
  text-align: right;
}
#login-user {
  /* from require-login component */
  display: none;
}
#theme-image {
    z-index: 99999;
    width: 100%;
}
#open-navbar-icon {
  height: 100%;
  position: fixed;
  left: 0;
  top: 0;
  width: 25px;
  color: white !important;
  background-color: #d2fbff;
}
#main-contents {
  margin-left: 30px;
}
.pad-for-sidenav {
  padding-left:300px;
}
@media only screen and (max-width : 992px) {
  .pad-for-sidenav {
    padding-left: 0;
  }
}
</style>
