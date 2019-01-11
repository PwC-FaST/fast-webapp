<template>
  <f7-page ptr @ptr:refresh="onPullToRefresh">
    <f7-navbar title="Crop needs" back-link>
      <f7-nav-right>
        <f7-link :href="`/nmp/plan/${planId}/manure-application/`">Next</f7-link>
      </f7-nav-right>
    </f7-navbar>
    <fast-toolbar></fast-toolbar>

    <template v-if="plan.loading">
      <p>Loading...</p>
    </template>

    <template v-else-if="plan.errors">
      <p>Content could not be retrieved, try to refresh.</p>
    </template>

    <template v-else>
      <f7-block>
        <p>The needs of your crops are computed on estimated values for the complete season.</p>
        <p>Edit the values or keep the default estimates.</p>
      </f7-block>

      <f7-block strong class="bg-color-yellow text-color-orange">
        <p>
          These are demo values and are not the result of a real NMP algorithm.
          Do not use in production.
        </p>
      </f7-block>

      <template v-if="plan && plan.farmParcelCropNeeds && plan.farmParcelCropNeeds.length > 0">
        <f7-block
          v-for="(need, index) in plan.farmParcelCropNeeds"
          strong
          style="min-height: 132px; margin-bottom: 10px; margin-top: 10px;"
          :key="need.id"
        >
          <farm-parcel-snapshot
            :svg="parcels[index].snapshotSvg"
            :width="100"
            :height="100"
            :key="parcels[index].lpisParcelId"
            class="float-left margin-right"
          ></farm-parcel-snapshot>
          <div>
            <f7-row>
              <f7-col>
                <h3 class="no-margin">{{ parcels[index].name }}</h3>
              </f7-col>
              <f7-col class="text-align-right">
                <span>{{ `${Math.round(parcels[index].gisInfo.area / 1000) / 10} ha` }}</span>
              </f7-col>
            </f7-row>
            <f7-row>
              <f7-col>
                <span>{{ parcels[index].cropSpecies ? parcels[index].cropSpecies.nameSingular : 'Missing crop species!'}}</span>
              </f7-col>
              <f7-col class="text-align-right">
                <span>{{ parcels[index].farmingCommitments.map(c => c.id).join(', ') }}</span>
              </f7-col>
            </f7-row>
            <f7-list
              class="no-margin no-hairlines no-item-content-padding"
              style="margin-left: 115px !important"
            >
              <f7-list-input
                label="Target yield"
                :default-value="need.targetYield"
                info="kg/ha"
                clear-button
                @change="onChangeCropNeedTargetYield(need, $event.target.value)"
              ></f7-list-input>
              <f7-list-item
                checkbox
                :checked="parcels[index].cropSpecies ? need.isActive: false"
                :class="{'disabled': !parcels[index].cropSpecies}"
                @change="parcels[index].cropSpecies ? onChangeCropNeedIsActive(need, $event.target.value): null"
              >Include parcel in plan</f7-list-item>
            </f7-list>
          </div>
        </f7-block>
      </template>
      <f7-list v-else>
        <f7-list-item-row>
          <p class="margin-left margin-right">No farm parcel.</p>
        </f7-list-item-row>
      </f7-list>

      <f7-block>
        <f7-button big fill :href="`/nmp/plan/${planId}/manure-application/`">Next</f7-button>
      </f7-block>
    </template>
  </f7-page>
</template>

<script>
import FastToolbar from "@/components/Toolbar";
import FarmParcelSnapshot from "@/components/farm/FarmParcelSnapshot.vue";

import { client } from "@/apollo/client";
import queryPlan from "./graphql/queryPlan.gql";
import fragmentFarmParcel from "@/components/farm/graphql/fragmentFarmParcel.gql";
import mutationUpdateFarmParcelCropNeeds from "./graphql/mutationUpdateFarmParcelCropNeeds.gql";

export default {
  name: "nmp-crop-needs-page",
  components: {
    FastToolbar,
    FarmParcelSnapshot
  },
  props: {
    planId: { type: String, required: true }
  },
  apollo: {
    plan: {
      query: queryPlan,
      variables() {
        return {
          planId: this.planId
        };
      },
      fetchPolicy: "cache-first"
    }
  },
  data() {
    return {
      plan: { loading: true }
    };
  },
  computed: {
    parcels() {
      if (
        this.plan &&
        this.plan.farmParcelCropNeeds &&
        this.plan.farmParcelCropNeeds.length > 0
      ) {
        return this.plan.farmParcelCropNeeds.map(n => {
          return client.readFragment({
            id: "FarmParcelType." + n.farmParcel.id,
            fragment: fragmentFarmParcel,
            fragmentName: "fragmentFarmParcel"
          });
        });
      } else {
        return [];
      }
    }
  },
  methods: {
    onPullToRefresh(e, done) {
      this.$apollo.queries.plan.refetch().then(done);
    },
    onChangeCropNeedTargetYield(need, value) {
      value = Number(value);
      this.$f7.progressbar.show();
      this.$apollo
        .mutate({
          mutation: mutationUpdateFarmParcelCropNeeds,
          variables: {
            farmParcelCropNeedsId: need.id,
            targetYield: value
          }
        })
        .then(() => {
          this.$f7.progressbar.hide();
        })
        .catch(() => {
          this.$f7.progressbar.hide();
        });
    },
    onChangeCropNeedIsActive(need, value) {
      this.$f7.progressbar.show();
      this.$apollo
        .mutate({
          mutation: mutationUpdateFarmParcelCropNeeds,
          variables: {
            farmParcelCropNeedsId: need.id,
            isActive: value
          }
        })
        .then(() => {
          this.$f7.progressbar.hide();
        })
        .catch(() => {
          this.$f7.progressbar.hide();
        });
    }
  }
};
</script>

<style>
.no-item-content-padding .item-content {
  padding-left: 0 !important;
}
</style>
