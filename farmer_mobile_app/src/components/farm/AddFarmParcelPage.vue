<template>
  <f7-page>
    <f7-navbar title="Add or import a parcel" back-link></f7-navbar>
    <fast-toolbar></fast-toolbar>

    <f7-block strong>
      <f7-block-header>Automatic</f7-block-header>

      <template v-if="farm.transferredFarmParcels">
        <p>Import parcels transferred to you by other farmers:</p>
        <f7-list>
          <f7-list-item
            v-for="parcel in farm.transferredFarmParcels"
            checkbox
            :key="parcel.id"
            :checked="true"
            :title="parcel.name"
          ></f7-list-item>
        </f7-list>
        <f7-button fill>Review selected parcels</f7-button>
      </template>

      <p>Import parcels from the national parcel registry:</p>
      <f7-button fill big href="/farm/parcel/add/select-from-map/">Select parcels from a map</f7-button>
    </f7-block>

    <f7-block strong>
      <f7-block-header>Using geolocation</f7-block-header>
      <p>Create a parcel using your own geolocated track:</p>
      <f7-button big class="disabled">Start parcel creation</f7-button>
    </f7-block>

    <f7-block strong>
      <f7-block-header>Manual</f7-block-header>
      <p>Manual editing of parcel boundaries is possible from the FaST web portal, available at
        <f7-link class="disabled">fast-nmp.eu</f7-link>.
      </p>
    </f7-block>
  </f7-page>
</template>

<script>
import FastToolbar from "@/components/Toolbar";

import fragmentFarm from "./graphql/fragmentFarm.gql";
import { provider } from "@/apollo/provider";

export default {
  name: "farm-add-farm-parcel-page",
  components: {
    "fast-toolbar": FastToolbar
  },
  data() {
    return {
      fragmentFarmFromCache: {
        id: "FarmType",
        fragment: fragmentFarm,
        fragmentName: "fragmentFarm"
      }
    };
  },
  computed: {
    farm() {
      return provider.defaultClient.readFragment(this.fragmentFarmFromCache);
    }
  }
};
</script>

<style scoped>
</style>
