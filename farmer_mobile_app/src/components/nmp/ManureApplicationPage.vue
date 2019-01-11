<template>
  <f7-page ptr @ptr:refresh="onPullToRefresh">
    <f7-navbar title="Manure application" back-link>
      <f7-nav-right>
        <f7-link :href="`/nmp/plan/${planId}/results/`">Next</f7-link>
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
      <template v-if="orderedActiveFarmParcelCropNeeds.length > 0">
        <f7-block>
          <p>Your parcels have been automatically prioritized versus their suitability for manure application.</p>
          <p>Use this prioritization or reorder the parcels using the handles on the right.</p>
        </f7-block>
        <f7-list sortable sortable-enabled @sortable:sort="onSort">
          <f7-list-item
            v-for="(need, index) in orderedActiveFarmParcelCropNeeds"
            :key="need.id"
            :id="need.id"
            :title="farmParcels[need.farmParcel.id].name"
            style="min-height: 58px"
            :footer="reasons[index]"
          >
            <farm-parcel-snapshot
              slot="media"
              :svg="farmParcels[need.farmParcel.id].snapshotSvg"
              :width="42"
              :height="42"
              :key="farmParcels[need.farmParcel.id].lpisParcelId"
            ></farm-parcel-snapshot>
          </f7-list-item>
        </f7-list>
      </template>
      <template v-if="inactiveFarmParcelCropNeeds.length > 0">
        <f7-block-header>The following parcels are not taken into account in the nutrient management planning.</f7-block-header>
        <f7-list>
          <f7-list-item
            v-for="need in inactiveFarmParcelCropNeeds"
            :key="need.id"
            :id="need.id"
            :title="farmParcels[need.farmParcel.id].name"
            footer="You have excluded this parcel from the nutrient management plan"
            style="min-height: 58px"
          >
            <farm-parcel-snapshot
              slot="media"
              :svg="farmParcels[need.farmParcel.id].snapshotSvg"
              :width="42"
              :height="42"
              :key="farmParcels[need.farmParcel.id].lpisParcelId"
            ></farm-parcel-snapshot>
          </f7-list-item>
        </f7-list>
      </template>

      <f7-list v-if="plan && plan.farmParcelCropNeeds && plan.farmParcelCropNeeds.length === 0">
        <f7-list-item-row>
          <p class="margin-left margin-right">No farm parcel.</p>
        </f7-list-item-row>
      </f7-list>

      <f7-block>
        <f7-button big fill :href="`/nmp/plan/${planId}/results/`">Next</f7-button>
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
  name: "nmp-manure-application-page",
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
      plan: { loading: true },

      // TODO: this (and the actual ordering) should be calculated by the server based on the
      // GIS data for the parcel: slope, proximity to river, proximity to manure storage, proximity to road, etc
      reasons: [
        "Closest to your manure storage & high nitrogen needs",
        "Closest to your manure storage",
        "High slope and proximity to water body",
        "",
        ""
      ]
    };
  },
  computed: {
    farmParcels() {
      if (
        this.plan &&
        this.plan.farmParcelCropNeeds &&
        this.plan.farmParcelCropNeeds.length > 0
      ) {
        let farmParcels = {};
        this.plan.farmParcelCropNeeds.forEach(n => {
          farmParcels[n.farmParcel.id] = client.readFragment({
            id: "FarmParcelType." + n.farmParcel.id,
            fragment: fragmentFarmParcel,
            fragmentName: "fragmentFarmParcel"
          });
        });
        return farmParcels;
      } else {
        return {};
      }
    },
    orderedActiveFarmParcelCropNeeds() {
      if (
        this.plan &&
        this.plan.farmParcelCropNeeds &&
        this.plan.farmParcelCropNeeds.length > 0
      ) {
        return this.plan.farmParcelCropNeeds
          .slice()
          .filter(x => x.isActive)
          .sort(x => x.priorityOrder)
          .reverse();
      } else {
        return [];
      }
    },
    inactiveFarmParcelCropNeeds() {
      if (
        this.plan &&
        this.plan.farmParcelCropNeeds &&
        this.plan.farmParcelCropNeeds.length > 0
      ) {
        return this.plan.farmParcelCropNeeds.slice().filter(x => !x.isActive);
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
    },
    onSort(e) {
      let newPriorityOrder;
      if (e.detail.to === 0) {
        // first
        newPriorityOrder =
          this.orderedActiveFarmParcelCropNeeds[0].priorityOrder + 1;
      } else if (
        e.detail.to ===
        this.orderedActiveFarmParcelCropNeeds.length - 1
      ) {
        // last
        newPriorityOrder =
          this.orderedActiveFarmParcelCropNeeds[
            this.orderedActiveFarmParcelCropNeeds.length - 1
          ].priorityOrder / 2;
      } else {
        newPriorityOrder =
          (this.orderedActiveFarmParcelCropNeeds[e.detail.to].priorityOrder +
            this.orderedActiveFarmParcelCropNeeds[e.detail.to + 1]
              .priorityOrder) /
          2;
      }

      this.$f7.progressbar.show();
      this.$apollo
        .mutate({
          mutation: mutationUpdateFarmParcelCropNeeds,
          variables: {
            farmParcelCropNeedsId: e.target.id,
            priorityOrder: newPriorityOrder
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
