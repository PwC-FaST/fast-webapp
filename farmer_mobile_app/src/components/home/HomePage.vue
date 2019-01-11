<template>
  <f7-page ptr @ptr:refresh="onPullToRefresh">
    <fast-navbar title="FaST"></fast-navbar>
    <fast-toolbar></fast-toolbar>

    <f7-block v-if="feed.loading">
      <p>Loading...</p>
    </f7-block>

    <!-- Add an fake element to push the user to install the PWA -->
    <template v-if="!isStandalone">
      <f7-block strong class="bg-color-green2 text-color-white">
        <template v-if="$f7.theme === 'ios'">
          <p>
            You can install the FaST prototype app to your smartphone:
            first click
            <i>Share</i> then
            <i>Add to Home Screen</i>.
          </p>
          <p class="text-align-center">
            <img
              src="/static/farmer_mobile_app/img/ios-screenshot-share.png"
              style="max-height: 60px; vertical-align: middle; max-width: 40%"
            >
            <span style="font-size: 20px">&rarr;</span>
            <img
              src="/static/farmer_mobile_app/img/ios-screenshot-add-to-home-screen.png"
              style="max-height: 60px; vertical-align: middle; max-width: 40%"
            >
          </p>
        </template>
        <template v-else>
          <p>
            You can install the FaST prototype app to your smartphone:
            click on
            <i>Add to Home Screen</i>.
          </p>
          <p class="text-align-center">
            <img
              src="/static/farmer_mobile_app/img/md-screenshot-add-to-home-screen.png"
              style="max-height: 60px; max-width: 90%"
            >
          </p>
        </template>
      </f7-block>
    </template>

    <template v-if="todayFeedItems && todayFeedItems.length > 0">
      <f7-block-title>Today</f7-block-title>
      <template v-for="(feedItem, index) in todayFeedItems">
        <component :is="feedItem.component" :key="'today-' + index" :feed-item="feedItem"></component>
      </template>
    </template>

    <template v-if="yesterdayFeedItems && yesterdayFeedItems.length > 0">
      <f7-block-title>Yesterday</f7-block-title>
      <template v-for="(feedItem, index) in yesterdayFeedItems">
        <component :is="feedItem.component" :key="'yesterday-' + index" :feed-item="feedItem"></component>
      </template>
    </template>

    <template v-if="earlierFeedItems && earlierFeedItems.length > 0">
      <f7-block-title>Earlier</f7-block-title>
      <component
        v-for="(feedItem, index) in earlierFeedItems"
        :is="feedItem.component"
        :key="'earlier-' + index"
        :feed-item="feedItem"
      ></component>
    </template>
  </f7-page>
</template>

<script>
import FastToolbar from "@/components/Toolbar.vue";
import FastNavbar from "@/components/Navbar.vue";

import queryFeed from "./graphql/queryFeed.gql";
import queryFarm from "@/components/farm/graphql/queryFarm.gql";
import queryWhoAmI from "@/components/core/graphql/queryWhoAmI.gql";

// Feed block components
import GenericOneButtonFeedBlock from "./feed/generic/OneButton.vue";
import MessagingNewMessagesInThreadFeedBlock from "./feed/messaging/NewMessagesInThread.vue";
import MessagingNewThreadFeedBlock from "./feed/messaging/NewThread.vue";
import FarmingFarmParcelAddedToFarmFeedBlock from "./feed/farming/FarmParcelAddedToFarm.vue";
import WeatherForecastFeedBlock from "./feed/weather/Forecast.vue";
import ServicesSatelliteImageryFeedBlock from "./feed/services/SatelliteImagery.vue";
import ServicesSoblooSatelliteImageryFeedBlock from "./feed/services/sobloo/SatelliteImagery.vue";

export default {
  name: "home-page",
  components: {
    FastToolbar,
    FastNavbar,
    GenericOneButtonFeedBlock,
    MessagingNewMessagesInThreadFeedBlock,
    MessagingNewThreadFeedBlock,
    FarmingFarmParcelAddedToFarmFeedBlock,
    WeatherForecastFeedBlock,
    ServicesSatelliteImageryFeedBlock,
    ServicesSoblooSatelliteImageryFeedBlock
  },
  apollo: {
    feed: {
      query: queryFeed,
      fetchPolicy: "cache-and-network"
    },
    farm: {
      query: queryFarm,
      fetchPolicy: "cache-and-network",
      skip() {
        return this.feed.loading;
      }
    },
    whoAmI: {
      query: queryWhoAmI
    }
  },
  data() {
    return {
      feed: { loading: true },
      farm: { loading: true },
      whoAmI: { loading: true }
    };
  },
  methods: {
    onPullToRefresh(e, done) {
      Promise.all([
        this.$apollo.queries.feed.refetch({ fetchPolicy: "network-only" }),
        this.$apollo.queries.farm.refetch({ fetchPolicy: "network-only" }),
        this.$apollo.queries.whoAmI.refetch({ fetchPolicy: "network-only" })
      ]).then(done);
    }
  },
  computed: {
    todayFeedItems() {
      return this.feed instanceof Array
        ? this.feed
            .filter(i => i.timegroup === "today")
            .slice()
            .sort((x, y) => (x.timestamp > y.timestamp ? 1 : -1))
            .reverse()
        : null;
    },
    yesterdayFeedItems() {
      return this.feed instanceof Array
        ? this.feed
            .filter(i => i.timegroup === "yesterday")
            .slice()
            .sort((x, y) => (x.timestamp > y.timestamp ? 1 : -1))
            .reverse()
        : null;
    },
    earlierFeedItems() {
      return this.feed instanceof Array
        ? this.feed
            .filter(i => i.timegroup === "earlier")
            .slice()
            .sort((x, y) => (x.timestamp > y.timestamp ? 1 : -1))
            .reverse()
        : null;
    },
    theme() {
      return this.$f7.theme;
    },
    isStandalone() {
      return window.matchMedia("(display-mode: standalone)").matches;
    }
  }
};
</script>
