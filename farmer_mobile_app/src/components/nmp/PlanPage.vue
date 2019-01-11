<template>
  <f7-page ptr @ptr:refresh="onPullToRefresh">
    <f7-navbar :title="plan.name || 'Loading...'" back-link>
      <f7-nav-right>
        <f7-link icon-only icon-f7="share" href="#" class="disabled"></f7-link>
      </f7-nav-right>
    </f7-navbar>
    <fast-toolbar></fast-toolbar>

    <template v-if="plan.loading">
      <f7-block>
        <p>Loading...</p>
      </f7-block>
    </template>

    <template v-else>
      <f7-block>
        <p>This is the optimized nutrient plan for your farm for this season.</p>
        <p>You can edit the values or keep the computed values.</p>
      </f7-block>

      <f7-block strong class="bg-color-yellow text-color-orange">
        <p>
          These are demo values and are not the result of a real NMP algorithm.
          Do not use in production.
        </p>
      </f7-block>

      <f7-block-title>Results</f7-block-title>

      <f7-block
        strong
        class="margin-bottom margin-top"
        v-for="need in activeCropNeeds"
        :key="need.id"
      >
        <f7-row>
          <f7-col width="20">
            <farm-parcel-snapshot
              :svg="need.farmParcel.snapshotSvg"
              :width="40"
              :height="40"
              :key="need.farmParcel.lpisParcelId"
            ></farm-parcel-snapshot>
          </f7-col>
          <f7-col width="80">
            <f7-row>
              <f7-col>
                <b>{{ need.farmParcel.name }}</b>
              </f7-col>
              <f7-col
                class="text-align-right text-color-gray"
              >{{ Math.round(need.farmParcel.gisInfo.area / 1000) / 10 + ' ha'}}</f7-col>
            </f7-row>
            <f7-row>
              <f7-col>
                <span>{{ need.farmParcel.cropSpecies ? need.farmParcel.cropSpecies.nameSingular : 'Missing crop species!' }}</span>
              </f7-col>
              <f7-col class="text-align-right">
                <span>{{ need.farmParcel.farmingCommitments.map(x => x.id).join(', ') }}</span>
              </f7-col>
            </f7-row>
            <f7-row v-if="need.nutrientPlanResult">
              <f7-col>
                <f7-list class="no-margin-bottom no-hairline-bottom">
                  <f7-list-input
                    label="Manure"
                    type="text"
                    readonly
                    info="kg/ha"
                    :value="need.nutrientPlanResult.manureQuantity"
                  ></f7-list-input>
                </f7-list>
              </f7-col>
              <f7-col>
                <f7-list class="no-margin-bottom no-hairline-bottom">
                  <f7-list-input
                    :label="need.nutrientPlanResult.chemicalType ? `Mineral (${need.nutrientPlanResult.chemicalType})` : 'No mineral'"
                    type="text"
                    readonly
                    info="kg/ha"
                    :class="{'disabled': !need.nutrientPlanResult.chemicalType}"
                    :value="need.nutrientPlanResult.chemicalQuantity"
                  ></f7-list-input>
                </f7-list>
              </f7-col>
            </f7-row>
          </f7-col>
        </f7-row>
      </f7-block>

      <template v-if="inactiveCropNeeds.length > 0">
        <f7-block-header>Parcels not taken into account in this plan:</f7-block-header>
        <f7-list>
          <f7-list-item
            v-for="need in inactiveCropNeeds"
            :key="need.id"
            :id="need.id"
            :title="need.farmParcel.name"
            :footer="!need.farmParcel.cropSpecies ? 'Missing crop for this parcel' : 'You have excluded this parcel from the nutrient management plan'"
            style="min-height: 58px"
          >
            <farm-parcel-snapshot
              slot="media"
              :svg="need.farmParcel.snapshotSvg"
              :width="42"
              :height="42"
              :key="need.farmParcel.lpisParcelId"
            ></farm-parcel-snapshot>
          </f7-list-item>
        </f7-list>
      </template>

      <f7-list>
        <f7-list-button
          title="Change the settings for this plan"
          :href="`/nmp/plan/${planId}/produced-manure/`"
        ></f7-list-button>
        <f7-list-button title="Delete this plan" color="red" @click="onClickDeletePlan()"></f7-list-button>
        <f7-list-button
          v-if="plan.isActive"
          title="Deactivate this plan"
          color="red"
          @click="onClickActivatePlan(false)"
        ></f7-list-button>
        <f7-list-button v-else title="Activate this plan" @click="onClickActivatePlan(true)"></f7-list-button>
        <f7-list-button class="disabled" title="Send me a copy by email"></f7-list-button>
      </f7-list>
      <f7-block strong>
        <f7-list class="no-margin-top no-hairlines">
          <f7-list-input
            ref="input_name"
            label="Rename this plan"
            type="text"
            clear-button
            :default-value="plan.name"
          ></f7-list-input>
        </f7-list>
        <f7-button fill big @click="onClickSavePlan()">Save this plan</f7-button>
      </f7-block>

      <f7-block>
        <p>Think something is not quite right about this plan or want to propose some enhancements?
          <f7-link class="disabled">Give your feedback on this plan</f7-link>
        </p>
      </f7-block>
    </template>
  </f7-page>
</template>

<script>
import FastToolbar from "@/components/Toolbar.vue";
import FarmParcelSnapshot from "@/components/farm/FarmParcelSnapshot.vue";

import { client } from "@/apollo/client";
import queryPlan from "./graphql/queryPlan.gql";
import fragmentFarmParcel from "@/components/farm/graphql/fragmentFarmParcel.gql";
import mutationUpdatePlan from "./graphql/mutationUpdatePlan.gql";
import mutationDeletePlan from "./graphql/mutationDeletePlan.gql";

export default {
  name: "nmp-plan-page",
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
      isSaving: false
    };
  },
  computed: {
    activeCropNeeds() {
      if (this.plan.farmParcelCropNeeds) {
        return this.plan.farmParcelCropNeeds
          .map(n => {
            let farmParcel = client.readFragment({
              id: "FarmParcelType." + n.farmParcel.id,
              fragment: fragmentFarmParcel,
              fragmentName: "fragmentFarmParcel"
            });
            n.farmParcel = farmParcel;
            return n;
          })
          .filter(n => n.isActive && n.farmParcel.cropSpecies);
      } else {
        return [];
      }
    },
    inactiveCropNeeds() {
      if (this.plan.farmParcelCropNeeds) {
        return this.plan.farmParcelCropNeeds
          .map(n => {
            let farmParcel = client.readFragment({
              id: "FarmParcelType." + n.farmParcel.id,
              fragment: fragmentFarmParcel,
              fragmentName: "fragmentFarmParcel"
            });
            n.farmParcel = farmParcel;
            return n;
          })
          .filter(n => !n.isActive || !n.farmParcel.cropSpecies);
      } else {
        return [];
      }
    },
    farmParcels() {
      if (this.activeCropNeeds) {
        return this.activeCropNeeds.map(n => {});
      } else {
        return [];
      }
    }
  },
  methods: {
    onPullToRefresh(e, done) {
      this.$apollo.queries.plan.refetch({ planId: this.planId }).then(done);
    },
    onClickSavePlan() {
      this.$f7.progressbar.show();
      this.$apollo
        .mutate({
          mutation: mutationUpdatePlan,
          variables: {
            planId: this.planId,
            name: this.$refs["input_name"].inputHasValue
          }
        })
        .then(() => {
          this.$f7.progressbar.hide();
        })
        .catch(() => {
          this.$f7.progressbar.hide();
        });
    },
    onClickActivatePlan(isActive) {
      this.$f7.progressbar.show();
      this.$apollo
        .mutate({
          mutation: mutationUpdatePlan,
          variables: {
            planId: this.planId,
            isActive: isActive
          }
        })
        .then(() => {
          this.$f7.progressbar.hide();
        })
        .catch(() => {
          this.$f7.progressbar.hide();
        });
    },
    onClickDeletePlan() {
      this.$f7.dialog.confirm(
        `Do you wish to delete plan ${this.plan.name}?`,
        "Delete plan",
        () => {
          this.$f7.progressbar.show();
          this.$apollo
            .mutate({
              mutation: mutationDeletePlan,
              variables: {
                planId: this.planId
              }
            })
            .then(() => {
              this.$f7.progressbar.hide();
              this.$f7router.navigate("/nmp/");
            })
            .catch(() => {
              this.$f7.progressbar.hide();
            });
        }
      );
    }
  }
};
</script>
