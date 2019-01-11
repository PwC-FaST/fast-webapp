<template>
  <f7-page>
    <f7-navbar title="Import parcel" back-link></f7-navbar>
    <fast-toolbar></fast-toolbar>
    <f7-block class="no-margin-bottom">
      <p>You are about to import an existing parcel to your farm.</p>
    </f7-block>

    <f7-block strong class="no-margin-bottom no-hairlines-bottom">
      <f7-row>
        <f7-col>
          <span>ID:</span>&nbsp;
          <b>{{ displayParcelId }}</b>
        </f7-col>
      </f7-row>
    </f7-block>

    <farm-parcel-map
      :lpis-layer-interactive="false"
      :pre-selected-lpis-parcel-id="lpisParcelId"
      center-init="coords"
      :center-init-coords="center"
      height="200px"
    ></farm-parcel-map>

    <f7-block>
      <p>Please select a justification for why you are adding this parcel to your farm inventory.</p>
    </f7-block>
    <f7-list class="no-margin-top no-hairlines no-hairlines-between">
      <f7-list-item smart-select title="Justification:" class="no-hairlines">
        <select name="Justification">
          <option value="apple" selected>Reason 1</option>
          <option value="pineapple">Reason 2</option>
        </select>
      </f7-list-item>
    </f7-list>
    <f7-block class="no-margin-top">
      <f7-button fill big @click="onClickConfirm()">Add this parcel to my farm</f7-button>
    </f7-block>
  </f7-page>
</template>

<script>
import FastToolbar from "@/components/Toolbar";
import FarmParcelMap from "./FarmParcelMap.vue";

import { provider } from "@/apollo/provider";
import fragmentFarm from "./graphql/fragmentFarm.gql";
import mutationAddFarmParcelToFarm from "./graphql/mutationAddFarmParcelToFarm.gql";

export default {
  name: "farm-confirm-add-parcel-page",
  components: {
    "fast-toolbar": FastToolbar,
    "farm-parcel-map": FarmParcelMap
  },
  props: {
    lpisParcelId: String,
    lpisParcelCentroid: Array
  },
  data() {
    return {
      zoom: 16,
      fragmentFarmFromCache: {
        id: "FarmType",
        fragment: fragmentFarm,
        fragmentName: "fragmentFarm"
      }
    };
  },
  computed: {
    width() {
      return window.innerWidth || window.clientWidth;
    },
    farm() {
      return provider.defaultClient.readFragment(this.fragmentFarmFromCache);
    },
    center() {
      return this.lpisParcelCentroid;
    },
    displayParcelId() {
      let tokens = this.lpisParcelId.split(":");
      return tokens[tokens.length - 1];
    }
  },
  methods: {
    onClickConfirm() {
      let preloader = this.$f7.dialog.preloader(
        "Loading parcel information..."
      );
      this.$apollo
        .mutate({
          mutation: mutationAddFarmParcelToFarm,
          variables: {
            farmId: this.farm.id,
            lpisParcelId: this.lpisParcelId
          }
        })
        .then(data => {
          //this.$apollo.queries.farm.refetch({fetchPolicy: 'network-only'})
          preloader.close();
          this.$f7router.navigate("/farm/");
        })
        .catch(error => {
          preloader.close();
        });
    }
  }
};
</script>

<style scoped>
</style>
