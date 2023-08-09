<template>
    <div>
        <ul id="slide-out" class="sidenav">
            <div class="user-view" style="height:200px">
                <div class="background">
                    <img id="bg-image" src="../assets/theme.png">
                </div>
            </div>
            <!-- {% include "sidenav.html" %} -->
        </ul>

        <!--open side nav-->
        <div id="open-sidenav" class="row">
            <div class="col s1">
                <a id="the-menu" href="#" data-target="slide-out" class="sidenav-trigger">
                    <i class="material-icons">menu</i>
                </a>
            </div>
            <div class="col s5">
            </div>
        </div>
    </div>
</template>


<script>
export default {
  name: 'SideBar',
  props: {
    msg: String
  }
}
</script>

<style scoped>
#bg-image {
    z-index: 99999;
    width: 100%;
}
</style>>