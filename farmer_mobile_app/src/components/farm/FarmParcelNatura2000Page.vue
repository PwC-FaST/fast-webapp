<template>
  <f7-page ptr @ptr:refresh="onPullToRefresh">
    <f7-navbar :title="title" back-link></f7-navbar>
    <fast-toolbar></fast-toolbar>

    <template v-if="farmParcel.natura2000Intersections">
      <template v-if="intersectsNatura2000.length > 0">
        <f7-list>
          <f7-block-title>
            <p>On this parcel</p>
          </f7-block-title>
          <f7-list-item
            v-for="intersection in intersectsNatura2000"
            :key="intersection.id"
            :header="$shortDate(intersection.natura2000Feature.releasedAt)"
            :title="intersection.natura2000Feature.siteName"
            :footer="intersection.natura2000Feature.siteTypes.join(', ')"
          >
            <img
              slot="media"
              src="/static/farmer_mobile_app/img/natura2000.svg"
              style="height: 26px"
            >
          </f7-list-item>
        </f7-list>
      </template>

      <template v-if="closeToNatura2000.length > 0">
        <f7-list>
          <f7-block-title>
            <p>Close to this parcel</p>
          </f7-block-title>
          <f7-list-item
            v-for="intersection in closeToNatura2000"
            :key="intersection.id"
            :header="$shortDate(intersection.natura2000Feature.releasedAt)"
            :title="intersection.natura2000Feature.siteName"
            :footer="intersection.natura2000Feature.siteTypes.join(', ')"
            :after="`${Math.round(intersection.minimumDistance / 100) / 10}km`"
          >
            <img
              slot="media"
              src="/static/farmer_mobile_app/img/natura2000.svg"
              style="height: 26px"
            >
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
  name: "farm-parcel-natura2000-page",
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
          farmParcelId: Number(this.farmParcelId)
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
    intersectsNatura2000() {
      if (this.farmParcel.natura2000Intersections) {
        return this.farmParcel.natura2000Intersections.filter(
          x => x.intersects
        );
      } else {
        return [];
      }
    },
    closeToNatura2000() {
      if (this.farmParcel.natura2000Intersections) {
        return this.farmParcel.natura2000Intersections.filter(
          x => !x.intersects
        );
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
