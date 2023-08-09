<template>
  <main>
    <ul id="slide-out" class="sidenav">
      <div class="user-view" style="height:200px">
          <div class="background">
              <img id="bg-image" src="./assets/theme.png" alt="theme picture">
          </div>
      </div>

      <!-- eslint-disable max-len -->
      <li><a href="/vision/"><i class="material-icons left">panorama</i>AI Vision</a></li>
      <li><a href="/vms/"><i class="material-icons left">layers</i>Virtual Machines</a></li>
      <li><a href="/my/web/"><i class="material-icons left">web</i>Web Reader</a></li>
      <li class="divider" tabindex="-1"></li>
      <li><a href="/shiny/resources/tvSOBI/"><i class="material-icons">school</i>tvSOBI - Thesis</a></li>
      <li><a href="/shiny/chaos/"><i class="material-icons">flare</i>Chaos Theory</a></li>
      <li><a href="/shiny/missingData/"><i class="material-icons">gradient</i>EM Algorithm Visulaized</a></li>
      <li><a href="/shiny/tools/"><i class="material-icons">inbox</i>Toolbox</a></li>

      <li class="divider" tabindex="-1"></li>

      <li><a href="/about"><i class="material-icons left">assignment_ind</i>About Me (CV)</a></li>
      <li><a href="/"><i class="material-icons left">pages</i>Home</a></li>
      <!-- router-link ? -->
      <li>
        <a onclick="M.toast({html: 'Cheers! I am a toast'})" class="waves-effect" href="#!">
        <i class="material-icons">pets</i>Have a Toast</a>
      </li>
      <!-- eslint-disable max-len -->
    </ul>

    <div id="open-sidenav" class="row">
        <div class="col s1">
            <a id="the-menu" href="#" data-target="slide-out" class="sidenav-trigger">
                <i class="material-icons">menu</i>
            </a>
        </div>
        <div class="col s5">
        </div>
    </div>

    <div id="main-contents">
      <router-view/>
    </div>
  </main>
</template>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#bg-image {
    z-index: 99999;
    width: 100%;
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
