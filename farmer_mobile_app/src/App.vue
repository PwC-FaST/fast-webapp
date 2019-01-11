<template>
  <f7-app :params="f7params" class="color-theme-green2">
    <f7-statusbar></f7-statusbar>

    <f7-panel left theme-dark>
      <f7-view :ios-swipe-back="false" :md-swipe-back="false">
        <left-panel-page></left-panel-page>
      </f7-view>
    </f7-panel>

    <f7-view id="main-view" url="/" main></f7-view>
  </f7-app>
</template>

<script>
import routes from "@/router/routes.js";

const MobileDetect = require("mobile-detect");

const themeFromUrl = new URL(window.location).searchParams.get("theme");
const themeFromUserAgent =
  new MobileDetect(window.navigator.userAgent).os() === "iOS" ? "ios" : "md";

import LeftPanelPage from "@/components/LeftPanelPage.vue";

export default {
  name: "app-page",
  components: {
    "left-panel-page": LeftPanelPage
  },
  data() {
    return {
      f7params: {
        id: "fast.farmer-mobile-app",
        name: "FaST Farmer App",
        theme: themeFromUrl || themeFromUserAgent,
        routes: routes
      }
    };
  }
};
</script>
