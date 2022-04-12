<template>
  <div class="mb-6">
    <v-toolbar dark flat class='transparent-navbar'>
      <v-tabs fixed-tabs>
        <v-tab :to="{ name: 'page1' }"> page1 </v-tab>
        <v-tab :to="{ name: 'page2' }"> page2 </v-tab>
        <v-tab :to="{ name: 'page3' }"> page3 </v-tab>
        <v-tab :to="{ name: 'page4' }"> page4 </v-tab>
      </v-tabs>
    </v-toolbar>

    <div
      class="color-row"
      :style="'background: ' + $route.meta.theme"
    ></div>
  </div>
</template>


<script>
export default {};
</script>


<style lang="scss" scoped >
$navbar-height: 64px;

.color-row {
  height: 500px;
  width: 100%;
  position: absolute;
  margin-top: -$navbar-height;
  z-index: 1;
}

.transparent-navbar {
  background: transparent !important;
  z-index: 2;
  height: $navbar-height;
}
</style>