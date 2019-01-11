<template>
  <f7-page>
    <f7-navbar title="Select parcel to import" back-link></f7-navbar>
    <fast-toolbar></fast-toolbar>

    <farm-parcel-map
      v-if="!farm.loading"
      :farm-id="farm.id"
      height="100%"
      :center-init="'farm'"
      :lpis-layer-interactive="true"
      :lpis-layer-style-primary="lpisStylePrimary"
      :lpis-layer-style-secondary="lpisStylePrimary"
      action-button-text="Import selected parcel"
      @click-action-button="onClickActionButton"
    ></farm-parcel-map>

    <f7-sheet class="demo-sheet" :opened="popupVisible" @sheet:closed="popupVisible = false">
      <f7-toolbar>
        <div class="left"></div>
        <div class="right">
          <f7-link sheet-close>Close</f7-link>
        </div>
      </f7-toolbar>
      <f7-page-content>
        <f7-block>
          <p v-html="popupHtml"></p>
        </f7-block>
      </f7-page-content>
    </f7-sheet>
  </f7-page>
</template>

<script>
import FastToolbar from "@/components/Toolbar";
import FarmParcelMap from "./FarmParcelMap.vue";

import Vue2LeafletVectorGridProtobuf from "vue2-leaflet-vectorgrid";
import { LControlLayers, LControl } from "vue2-leaflet";

import fragmentFarm from "./graphql/fragmentFarm.gql";
import { provider } from "@/apollo/provider";

import { lpisStylePrimary } from "./map-styles";

export default {
  name: "farm-select-farm-parcel-from-map-page",
  components: {
    "fast-toolbar": FastToolbar,
    "farm-parcel-map": FarmParcelMap,
    "l-vectorgrid-protobuf": Vue2LeafletVectorGridProtobuf,
    "l-control-layers": LControlLayers,
    "l-control": LControl
  },
  data() {
    return {
      zoom: 16,
      selectedParcelLpisId: null,
      selectedParcelCentroid: null,
      popupVisible: false,
      popupHtml: "",
      fragmentFarmFromCache: {
        id: "FarmType",
        fragment: fragmentFarm,
        fragmentName: "fragmentFarm"
      },
      lpisStylePrimary: lpisStylePrimary
    };
  },
  computed: {
    farm() {
      return provider.defaultClient.readFragment(this.fragmentFarmFromCache);
    }
  },
  methods: {
    onClickActionButton({ lpisParcelId, lpisParcelCentroid }) {
      this.$f7router.navigate("/farm/parcel/add/confirm/", {
        props: {
          lpisParcelId: lpisParcelId,
          lpisParcelCentroid: lpisParcelCentroid
        }
      });
    }
  }
};
</script>

<style scoped>
</style>
