<template>
  <f7-page ptr @ptr:refresh="onPullToRefresh">
    <f7-navbar :title="title" back-link></f7-navbar>
    <fast-toolbar></fast-toolbar>

    <template v-if="farmParcel.gisInfo">
      <farm-parcel-map
        v-if="!farmParcel.loading"
        :farm-parcel-id="farmParcel.id"
        :farm-id="farm.id"
        :lpis-layer-style-default="lpisStyleHidden"
      ></farm-parcel-map>

      <f7-block class="no-margin-top" strong>
        <f7-row>
          <f7-col width="50" class="text-align-left">City:&nbsp;
            <b>{{ city }}</b>
          </f7-col>
          <f7-col width="50" class="text-align-right">
            <span class="text-color-gray2">ID:</span>&nbsp;
            <span>
              <b>{{ displayParcelId }}</b>
            </span>
          </f7-col>
        </f7-row>
        <f7-row class="text-align-left">
          <f7-col width="50" class="text-align-left">Area:
            <b>{{ area }} ha</b>
          </f7-col>
        </f7-row>
      </f7-block>

      <f7-block-title>Constraints</f7-block-title>
      <p v-if="!constraints || constraints.length === 0">No constraint detected</p>
      <f7-list v-else>
        <f7-list-item
          v-for="(constraint, index) in constraints"
          :title="constraint.text"
          :link="constraint.href"
          :key="index"
        >
          <img slot="media" :src="constraint.icon" style="height: 26px">
        </f7-list-item>
      </f7-list>

      <template v-if="!farmingCommitments.loading && !farmParcel.loading">
        <template v-if="farmingCommitments.length > 0">
          <f7-block-title>Commitments</f7-block-title>
          <f7-list>
            <f7-list-item
              v-for="commitment in farmingCommitments"
              checkbox
              :key="commitment.id"
              :checked="!!farmParcel.farmingCommitments.find(x => x.id === commitment.id)"
              :title="commitment.name"
              @change="onChangeFarmingCommitment(commitment.id)"
            ></f7-list-item>
          </f7-list>
        </template>

        <template v-else>
          <f7-block-title>Commitments</f7-block-title>
          <f7-block strong>
            <p>No commitment</p>
          </f7-block>
        </template>
      </template>

      <f7-block-title>Crops</f7-block-title>
      <f7-list>
        <f7-list-item
          v-if="farmParcel.cropSpecies"
          :title="farmParcel.cropSpecies.nameSingular"
          :footer="farmParcel.cropSpecies.nameLatin"
          after="Remove"
          @click="onCropSpeciesRemove"
        >
          <img
            slot="media"
            src="/static/farmer_mobile_app/img/toolbar/icon-leaves-ios.svg"
            style="height: 26px"
          >
        </f7-list-item>
        <f7-list-item
          v-else
          title="Add a crop to this parcel"
          popup-open=".crop-select-popup"
          link="#"
        ></f7-list-item>
      </f7-list>

      <f7-block-title>Soil properties</f7-block-title>
      <f7-list>
        <f7-list-item
          header="pH (water)"
          :title="Math.round(farmParcel.soilInfo.pHinH20 * 10) / 10"
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
        <f7-list-button :href="`/farm/parcel/${farmParcelId}/soil/`">View soil details</f7-list-button>
        <f7-list-button class="disabled">Add soil sample</f7-list-button>
      </f7-list>

      <f7-list>
        <f7-list-button class="disabled">Report an issue</f7-list-button>
        <f7-list-button @click="onClickRenameParcel()">Rename this parcel</f7-list-button>
        <f7-list-button class="disabled">Transfer to another farmer</f7-list-button>
        <f7-list-button color="red" @click="onClickRemoveParcel()">Remove this parcel from my farm</f7-list-button>
      </f7-list>
    </template>

    <f7-popup class="crop-select-popup" ref="crop_species_popup">
      <f7-page>
        <f7-navbar title="Select crop">
          <f7-nav-right>
            <f7-link popup-close>Close</f7-link>
          </f7-nav-right>
        </f7-navbar>
        <crop-species-list @crop-species-select="onCropSpeciesSelected"></crop-species-list>
      </f7-page>
    </f7-popup>
  </f7-page>
</template>

<script>
import FastToolbar from "@/components/Toolbar";
import FarmParcelMap from "./FarmParcelMap.vue";
import CropSpeciesList from "./CropSpeciesList.vue";

import { lpisStyleHidden } from "./map-styles";

import fragmentFarm from "./graphql/fragmentFarm.gql";
import queryFarm from "./graphql/queryFarm.gql";
import queryFarmParcel from "./graphql/queryFarmParcel.gql";
import queryFarmingCommitments from "./graphql/queryFarmingCommitments.gql";
import mutationRemoveFarmParcelFromFarm from "./graphql/mutationRemoveFarmParcelFromFarm.gql";
import mutationUpdateFarmParcel from "./graphql/mutationUpdateFarmParcel.gql";

export default {
  name: "farm-parcel-page",
  components: {
    "fast-toolbar": FastToolbar,
    "farm-parcel-map": FarmParcelMap,
    "crop-species-list": CropSpeciesList
  },
  props: {
    farmParcelId: String
  },
  apollo: {
    farm: {
      query: queryFarm,
      fetchPolicy: "cache-first"
    },
    farmParcel: {
      query: queryFarmParcel,
      variables() {
        return {
          farmParcelId: Number(this.farmParcelId)
        };
      },
      fetchPolicy: "cache-first"
    },
    farmingCommitments: {
      query: queryFarmingCommitments,
      fetchPolicy: "cache-first"
    }
  },
  data() {
    return {
      farmParcel: { loading: true },
      farmingCommitments: { loading: true },
      farm: { loading: true },
      zoom: 16,
      fragmentFarmFromCache: {
        id: "FarmType",
        fragment: fragmentFarm,
        fragmentName: "fragmentFarm"
      },
      lpisStyleHidden: lpisStyleHidden
    };
  },
  computed: {
    displayParcelId() {
      if (this.farmParcel.lpisParcelId) {
        let tokens = this.farmParcel.lpisParcelId.split(":");
        return tokens[tokens.length - 1];
      } else {
        return null;
      }
    },
    title() {
      return this.farmParcel.name || "Loading...";
    },
    city() {
      return this.farmParcel.address
        ? this.farmParcel.address.city.toUpperCase()
        : "...";
    },
    area() {
      return this.farmParcel.gisInfo
        ? Math.round(this.farmParcel.gisInfo.area / 1000) / 10
        : "...";
    },
    constraints() {
      let constraints = [];
      if (this.farmParcel.hydroIntersections) {
        const intersectsWaterBody =
          this.farmParcel.hydroIntersections.filter(x => x.intersects).length >
          0;
        if (intersectsWaterBody) {
          constraints.push({
            text: "Water body on parcel",
            href: `/farm/parcel/${this.farmParcel.id}/hydro/`,
            icon: "/static/farmer_mobile_app/img/river.svg"
          });
        } else if (this.farmParcel.hydroIntersections.length > 0) {
          const closestWaterBody = Math.round(
            Math.min(
              ...this.farmParcel.hydroIntersections.map(x => x.minimumDistance)
            )
          );
          constraints.push({
            text: `Water body close to parcel (${closestWaterBody}m)`,
            href: `/farm/parcel/${this.farmParcel.id}/hydro/`,
            icon: "/static/farmer_mobile_app/img/river.svg"
          });
        }
        if (this.farmParcel.natura2000Intersections) {
          const intersectsNatura2000 =
            this.farmParcel.natura2000Intersections.filter(x => x.intersects)
              .length > 0;
          if (intersectsNatura2000) {
            constraints.push({
              text: "Natura2000 area on this parcel",
              href: `/farm/parcel/${this.farmParcel.id}/natura2000/`,
              icon: "/static/farmer_mobile_app/img/natura2000.svg"
            });
          } else if (this.farmParcel.natura2000Intersections.length > 0) {
            let closestNatura2000 = Math.round(
              Math.min(
                ...this.farmParcel.natura2000Intersections.map(
                  x => x.minimumDistance
                )
              )
            );
            closestNatura2000 = Math.round(closestNatura2000 / 100) / 10;
            constraints.push({
              text: `Natura2000 close to parcel (${closestNatura2000}km)`,
              href: `/farm/parcel/${this.farmParcel.id}/natura2000/`,
              icon: "/static/farmer_mobile_app/img/natura2000.svg"
            });
          }
        }
        return constraints;
      }
    }
  },
  methods: {
    onClickRemoveParcel() {
      this.$f7.dialog.confirm(
        `Please confirm you wish to remove parcel ${
          this.farmParcel.lpisParcelId
        } from your farm`,
        "Remove this parcel?",
        () => {
          this.$f7.progressbar.show();
          this.$apollo
            .mutate({
              mutation: mutationRemoveFarmParcelFromFarm,
              variables: {
                farmParcelId: this.farmParcel.id
              },
              refetchQueries: [
                {
                  query: queryFarm,
                  fetchPolicy: "network-only"
                }
              ]
            })
            .then(() => {
              this.$f7.progressbar.hide();
              this.$f7router.navigate("/farm/");
            })
            .catch(() => {
              this.$f7.progressbar.hide();
            });
        },
        () => {}
      );
    },
    onClickRenameParcel() {
      this.$f7.dialog.prompt(
        "Enter a new name",
        this.farmParcel.name,
        value => {
          this.$f7.progressbar.show();
          this.$apollo
            .mutate({
              mutation: mutationUpdateFarmParcel,
              variables: {
                farmParcelId: this.farmParcel.id,
                name: value
              }
            })
            .then(() => {
              this.$f7.progressbar.hide();
              this.$forceUpdate();
            })
            .catch(() => {
              this.$f7.progressbar.hide();
            });
        }
      );
    },
    onChangeFarmingCommitment(commitmentId) {
      const idx = this.farmParcel.farmingCommitments.findIndex(
        x => x.id === commitmentId
      );
      let newCommitments = JSON.parse(
        JSON.stringify(this.farmParcel.farmingCommitments.map(x => x.id))
      );
      if (idx >= 0) {
        newCommitments.splice(idx, 1);
      } else {
        newCommitments.push(commitmentId);
      }
      this.$f7.progressbar.show();
      this.$apollo
        .mutate({
          mutation: mutationUpdateFarmParcel,
          variables: {
            farmParcelId: this.farmParcel.id,
            farmingCommitmentIds: newCommitments
          }
        })
        .then(() => {
          this.$f7.progressbar.hide();
          this.$forceUpdate();
        })
        .catch(() => {
          this.$f7.progressbar.hide();
        });
    },
    onCropSpeciesRemove() {
      this.$f7.progressbar.show();
      this.$apollo
        .mutate({
          mutation: mutationUpdateFarmParcel,
          variables: {
            farmParcelId: this.farmParcel.id,
            cropSpeciesId: -1
          }
        })
        .then(() => {
          this.$f7.progressbar.hide();
          this.$forceUpdate();
        })
        .catch(() => {
          this.$f7.progressbar.hide();
        });
    },
    onCropSpeciesSelected(cropSpecies) {
      this.$refs["crop_species_popup"].close();
      this.$f7.progressbar.show();
      this.$apollo
        .mutate({
          mutation: mutationUpdateFarmParcel,
          variables: {
            farmParcelId: this.farmParcel.id,
            cropSpeciesId: cropSpecies.id
          }
        })
        .then(() => {
          this.$f7.progressbar.hide();
          this.$forceUpdate();
        })
        .catch(() => {
          this.$f7.progressbar.hide();
        });
    },
    onPullToRefresh(e, done) {
      Promise.all([
        this.$apollo.queries.farmParcel.refetch(),
        this.$apollo.queries.farmingCommitments.refetch()
      ]).then(done);
    }
  }
};
</script>

<style scoped>
</style>
