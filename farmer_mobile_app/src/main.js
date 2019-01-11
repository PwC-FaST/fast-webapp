// Will be inserted by webpack DefinePlugin
window.FAST_ENVIRONMENT = FAST_ENVIRONMENT;

import babelPolyfill from "babel-polyfill";

// Library to generate assets for PWA on all platforms
// https://github.com/GoogleChromeLabs/pwacompat
require("pwacompat");

// Import Vue
import Vue from "vue";

// Import Framework7
import Framework7 from "framework7/framework7.esm.bundle.js";
import Framework7Vue from "framework7-vue/framework7-vue.esm.bundle.js";
import FastFramework7Styles from "./css/framework7.css";
Framework7.use(Framework7Vue);

// Import global app styles
import IconsStyles from "./css/icons.css";
import AppStyles from "./css/main.css";

// Import the Apollo client
import { provider } from "@/apollo/provider";
import { persistor } from "@/apollo/cache";

// Import Vue-moment
import VueMomentLib from "vue-moment-lib";
import moment from "moment";
Vue.use(VueMomentLib);

// Import Leaflet component
import { L, LMap, LTileLayer, LMarker } from "vue2-leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet-geotiff";

Vue.component("l-map", LMap);
Vue.component("l-tile-layer", LTileLayer);
Vue.component("l-marker", LMarker);

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png")
});

// Import another swiper to replace the one from Framework7 that has some glitches
import VueAwesomeSwiper from "vue-awesome-swiper";
import "swiper/dist/css/swiper.css";
Vue.use(VueAwesomeSwiper);

// Inject Apollo into Vue components
import VueApollo from "vue-apollo";
Vue.use(VueApollo);

// Activate Vue verbose mode only in development
Vue.config.performance = FAST_ENVIRONMENT !== "production";
Vue.config.devtools = FAST_ENVIRONMENT !== "production";
Vue.config.debug = FAST_ENVIRONMENT !== "production";
Vue.config.silent = FAST_ENVIRONMENT === "production";

// If in production, register the service worker that will cache the data and make the app available offline
if (FAST_ENVIRONMENT === "production" && "serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("/static/farmer_mobile_app/service-worker.js")
      .then(registration => {
        console.log("SW registered: ", registration);
      })
      .catch(registrationError => {
        console.log("SW registration failed: ", registrationError);
      });
  });
}

// Some momentjs shorthands used in the templates
Vue.mixin({
  methods: {
    $shortDate(datetime) {
      const m = moment(datetime);
      if (m.isSame(moment(new Date()), "day")) {
        return "today";
      } else if (m.isSame(moment(new Date()), "year")) {
        return m.format("MMM DD");
      } else {
        return m.format("MMM DD, YYYY");
      }
    },
    $shortDateTime(datetime) {
      const m = moment(datetime);
      if (m.isSame(moment(new Date()), "day")) {
        return m.format("HH:mm");
      } else if (m.isSame(moment(new Date()), "year")) {
        return m.format("MMM DD");
      } else {
        return m.format("MMM DD, YYYY");
      }
    }
  }
});

// Start the app
import App from "./App.vue";

persistor.restore().then(() => {
  window.__APPOLLO_CACHE_HAS_INITIALIZED__ = true;
  // The app is instantiated only when the Apollo provider is ready (ie when the cache has been restored)
  new Vue({
    el: "#app",
    template: "<app/>",
    apolloProvider: provider,
    components: {
      app: App
    }
  });
});
