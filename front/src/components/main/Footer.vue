<template>
  <v-footer padless absolute >
    <v-card class="flex" flat tile>
      <v-card-text class="p-4 white--text text-center"
      :style='"font-size: 18px; background: " + $route.meta.theme'>
       <strong>©  {{ new Date().getFullYear() }}  MozhaykaTeam</strong>
      </v-card-text>
    </v-card>
  </v-footer>
</template>

<script>
export default {};
</script>