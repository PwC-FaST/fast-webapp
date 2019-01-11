<template>
  <f7-page ptr @ptr:refresh="onPullToRefresh">
    <f7-navbar :title="title" back-link></f7-navbar>
    <fast-toolbar></fast-toolbar>

    <template v-if="farmParcel.soilInfo">
      <f7-block-header>
        <p>
          The following soil values are estimates based on the European
          <f7-link
            external
            href="https://esdac.jrc.ec.europa.eu/content/lucas-2009-topsoil-data"
          >LUCAS 2009 TOPSOIL program</f7-link>. The closest sampling point is
          <b>{{ Math.round(farmParcel.soilInfo.closestSampleDistance /100 ) / 10 }}km</b> away from your parcel.
        </p>
        <p>You can override these values by adding your own soil samples for this parcel.</p>
      </f7-block-header>

      <f7-list>
        <f7-list-item
          header="pH (water)"
          :title="Math.round(farmParcel.soilInfo.pHinH20 * 10) / 10"
        ></f7-list-item>
        <f7-list-item
          header="pH (CaCl2)"
          :title="Math.round(farmParcel.soilInfo.pHinCaCl2 * 10) / 10"
        ></f7-list-item>
        <f7-list-item
          header="Nitrogen content (N)"
          :title="Math.round(farmParcel.soilInfo.nitrogen * 10) / 10"
        >
          <span slot="title" class="text-color-gray4 margin-left">g/kg</span>
        </f7-list-item>
        <f7-list-item
          header="Phosphorus content (P)"
          :title="Math.round(farmParcel.soilInfo.phosphorus * 10) / 10"
        >
          <span slot="title" class="text-color-gray4 margin-left">mg/kg</span>
        </f7-list-item>
        <f7-list-item
          header="Extractable potassium content (K)"
          :title="Math.round(farmParcel.soilInfo.potassium * 10) / 10"
        >
          <span slot="title" class="text-color-gray4 margin-left">mg/kg</span>
        </f7-list-item>
        <f7-list-item
          header="Organic carbon"
          :title="Math.round(farmParcel.soilInfo.organicCarbon * 10) / 10"
        >
          <span slot="title" class="text-color-gray4 margin-left">g/kg</span>
        </f7-list-item>
        <f7-list-item
          header="Cation Exchange Capacity (CEC)"
          :title="Math.round(farmParcel.soilInfo.cationExchangeCapacity * 10) / 10"
        >
          <span slot="title" class="text-color-gray4 margin-left">cmol(+)/kg</span>
        </f7-list-item>
        <f7-list-item
          header="Coarse fragments"
          :title="Math.round(farmParcel.soilInfo.coarse * 10) / 10"
        >
          <span slot="title" class="text-color-gray4 margin-left">%</span>
        </f7-list-item>
        <f7-list-item header="Sand" :title="Math.round(farmParcel.soilInfo.sand * 10) / 10">
          <span slot="title" class="text-color-gray4 margin-left">%</span>
        </f7-list-item>
        <f7-list-item header="Silt" :title="Math.round(farmParcel.soilInfo.silt * 10) / 10">
          <span slot="title" class="text-color-gray4 margin-left">%</span>
        </f7-list-item>
        <f7-list-item header="Clay" :title="Math.round(farmParcel.soilInfo.clay * 10) / 10">
          <span slot="title" class="text-color-gray4 margin-left">%</span>
        </f7-list-item>
      </f7-list>

      <f7-block>
        <f7-button class="disabled" big fill>Add soil sample</f7-button>
      </f7-block>
    </template>
  </f7-page>
</template>

<script>
import FastToolbar from "@/components/Toolbar";

import queryFarmParcel from "./graphql/queryFarmParcel.gql";

export default {
  name: "farm-parcel-soil-page",
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
