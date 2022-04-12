<template>
  <div>
    <Header />
    <Navbar />
    <v-container>
      <v-card flat class="main">
        <keep-alive>
          <router-view />
        </keep-alive>
      </v-card>
    </v-container>
    <Footer />
  </div>
</template>

<script>
import Header from "@/components/main/Header.vue";
import Footer from "@/components/main/Footer.vue";
import Navbar from "@/components/main/Navbar.vue";

export default {
  components: {
    Header,
    Footer,
    Navbar,
  },
};
</script>


<style lang="scss">
.main {
  margin-bottom: 60px;
  z-index: 3;
  background: transparent !important;
}
</style>