<template>
  <f7-page ptr @ptr:refresh="onPullToRefresh">
    <f7-navbar :title="title" back-link></f7-navbar>
    <fast-toolbar></fast-toolbar>

    <template v-if="farmParcel.hydroIntersections">
      <template v-if="intersectsWaterBody.length > 0">
        <f7-list>
          <f7-block-title>
            <p>On this parcel</p>
          </f7-block-title>
          <f7-list-item
            v-for="intersection in intersectsWaterBody"
            :key="intersection.id"
            :title="intersection.hydrologyFeature.name || intersection.hydrologyFeature.id"
          >
            <img slot="media" src="/static/farmer_mobile_app/img/river.svg" style="height: 26px">
          </f7-list-item>
        </f7-list>
      </template>

      <template v-if="closeToWaterBody.length > 0">
        <f7-list>
          <f7-block-title>
            <p>Close to this parcel</p>
          </f7-block-title>
          <f7-list-item
            v-for="intersection in closeToWaterBody"
            :key="intersection.id"
            :title="intersection.hydrologyFeature.name || intersection.hydrologyFeature.id"
            :after="`${Math.round(intersection.minimumDistance)}m`"
          >
            <img slot="media" src="/static/farmer_mobile_app/img/river.svg" style="height: 26px">
          </f7-list-item>
        </f7-list>
      </template>
    </template>
  </f7-page>
</template>

<script>
import FastToolbar from "@/components/Toolbar";

import queryFarmParcel from "./graphql/queryFarmParcel.gql";

export default {
  name: "farm-parcel-hydro-page",
  components: {
    "fast-toolbar": FastToolbar
  },
  props: {
    farmParcelId: String
  },
  apollo: {
    farmParcel: {
      query: queryFarmParcel,
      variables() {
        return {
          farmParcelId: this.farmParcelId
        };
      },
      fetchPolicy: "cache-first"
    }
  },
  data() {
    return {
      farmParcel: { loading: true }
    };
  },
  computed: {
    title() {
      return this.farmParcel.name || "Loading...";
    },
    intersectsWaterBody() {
      if (this.farmParcel.hydroIntersections) {
        return this.farmParcel.hydroIntersections.filter(x => x.intersects);
      } else {
        return [];
      }
    },
    closeToWaterBody() {
      if (this.farmParcel.hydroIntersections) {
        return this.farmParcel.hydroIntersections.filter(x => !x.intersects);
      } else {
        return [];
      }
    }
  },
  methods: {
    onPullToRefresh(e, done) {
      Promise.all([this.$apollo.queries.farmParcel.refetch()]).then(done);
    }
  }
};
</script>

<style scoped>
</style>
