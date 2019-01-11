<template>
  <f7-page ptr @ptr:refresh="onPullToRefresh">
    <fast-navbar :title="title"></fast-navbar>
    <fast-toolbar></fast-toolbar>

    <f7-block-title>My parcels</f7-block-title>
    <f7-block strong>
      <swiper :options="swiperOptions" ref="swiper_parcels" @click="onFarmParcelSwiperClick">
        <swiper-slide
          v-for="parcel in orderedFarmParcels"
          :parcel-id="parcel.id"
          :key="parcel.id"
          class="swiper-slide-parcel"
        >
          <div class="swiper-slide-parcel-header">
            <b>{{ parcel.name }}</b>
          </div>
          <farm-parcel-snapshot
            :svg="parcel.snapshotSvg"
            :width="100"
            :height="100"
            :key="parcel.lpisParcelId"
          ></farm-parcel-snapshot>
          <div
            class="swiper-slide-parcel-footer text-align-right"
          >{{ Math.round(parcel.gisInfo.area / 1000)/10 }} ha</div>
        </swiper-slide>
        <swiper-slide class="swiper-slide-parcel">
          <div class="swiper-slide-add"></div>
        </swiper-slide>
      </swiper>

      <f7-link href="/farm/parcel/add/" class="margin-top">Add or remove a parcel...</f7-link>
    </f7-block>

    <f7-block-title>My livestock</f7-block-title>
    <f7-block strong>
      <swiper ref="swiper_livestock" :options="swiperOptions" @click="onFarmLivestockSwiperClick">
        <swiper-slide
          v-for="livestock in farmLivestockAggregated"
          style="width: 50px"
          :livestock-id="livestock.id"
          :key="livestock.id"
        >
          <svg-image
            :src="'/media/' + livestock.livestockSpecies.icon"
            class="livestock-species-icon"
            :width="50"
            :height="50"
          ></svg-image>
          <h3 class="width-100 text-align-center">{{ livestock.numberOfHeads }}</h3>
        </swiper-slide>
      </swiper>
      <f7-link href="/farm/livestock/">Edit my livestock...</f7-link>
    </f7-block>

    <f7-block-title>My buildings and non agricultural areas</f7-block-title>
    <f7-block strong>
      <f7-swiper ref="swiper_buildings" init :params="swiperOptions">
        <f7-swiper-slide v-for="building in farm.farmBuildings" :key="building.id">
          <div style="width: 100px; height: 100px;">
            <div>{{ building.nameSingular }}</div>
          </div>
        </f7-swiper-slide>
      </f7-swiper>
      <f7-link href="#" style="margin-top: 10px" class="disabled">Add or remove livestock...</f7-link>
    </f7-block>
  </f7-page>
</template>

<script>
import FastToolbar from "@/components/Toolbar.vue";
import FastNavbar from "@/components/Navbar.vue";
import SVGImage from "@/components/SVGImage";
import FarmParcelSnapshot from "./FarmParcelSnapshot";

import queryFarm from "./graphql/queryFarm.gql";
import queryLivestockSpecies from "./graphql/queryLivestockSpecies.gql";

export default {
  name: "farm-page",
  components: {
    FastToolbar,
    FastNavbar,
    "svg-image": SVGImage,
    FarmParcelSnapshot
  },
  apollo: {
    farm: {
      query: queryFarm,
      fetchPolicy: "cache-and-network"
    },
    livestockSpecies: {
      query: queryLivestockSpecies,
      fetchPolicy: "cache-and-network"
    }
  },
  data() {
    return {
      farm: { loading: true },
      livestockSpecies: { loading: true },
      swiperOptions: {
        spaceBetween: 20,
        slidesPerView: "auto",
        freeMode: true,
        simulateTouch: true
      },
      lastSwiperClick: null
    };
  },
  computed: {
    title() {
      return this.farm.loading
        ? "Loading..."
        : this.farm.error
        ? "Error"
        : this.farm.name;
    },
    orderedFarmParcels() {
      if (this.farm.farmParcels) {
        return this.farm.farmParcels
          .slice()
          .sort((x, y) => (x.name > y.name ? 1 : -1));
      } else {
        return [];
      }
    },
    farmLivestockAggregated() {
      if (this.farm.farmLivestock) {
        let agg = {};
        this.farm.farmLivestock.forEach(l => {
          const rootSpeciesId = l.livestockSpecies.rootLivestockSpecies.id;
          if (agg[rootSpeciesId]) {
            agg[rootSpeciesId].numberOfHeads += l.numberOfHeads;
          } else {
            agg[rootSpeciesId] = {
              livestockSpecies: l.livestockSpecies.rootLivestockSpecies,
              numberOfHeads: l.numberOfHeads
            };
          }
        });
        return Object.keys(agg)
          .sort()
          .map(k => agg[k]);
      } else {
        return [];
      }
    }
  },
  methods: {
    onFarmParcelSwiperClick(e) {
      // hack to solve this bug: https://github.com/surmon-china/vue-awesome-swiper/issues/286
      if (!this.lastSwiperClick || new Date() - this.lastSwiperClick > 200) {
        this.lastSwiperClick = new Date();
        if (this.$refs["swiper_parcels"].swiper.clickedSlide) {
          const farmParcelId = this.$refs[
            "swiper_parcels"
          ].swiper.clickedSlide.getAttribute("parcel-id");
          this.$f7router.navigate(`/farm/parcel/${farmParcelId}/`);
        }
      }
    },
    onFarmLivestockSwiperClick(e) {
      // hack to solve this bug: https://github.com/surmon-china/vue-awesome-swiper/issues/286
      if (!this.lastSwiperClick || new Date() - this.lastSwiperClick > 200) {
        this.lastSwiperClick = new Date();
        this.$f7router.navigate(`/farm/livestock/`);
      }
    },
    onPullToRefresh(e, done) {
      Promise.all([
        this.$apollo.queries.farm.refetch(),
        this.$apollo.queries.livestockSpecies.refetch()
      ]).then(done);
    }
  }
};
</script>

<style scoped>
.swiper-slide-parcel {
  width: 100px;
  height: 162px;
}

.swiper-slide-parcel-header {
  height: 42px;
  width: 100px;
  overflow: hidden;
}

.swiper-slide-parcel-footer {
  height: 20px;
}

.swiper-slide-livestock {
  width: 60px;
}

.swiper-slide-add {
  margin-top: 42px;
  height: 100px;
  width: 100px;
  border: 1px dashed silver;
  border-radius: 5px;
}
</style>

<style>
.livestock-species-icon svg path {
  fill: black;
  fill-opacity: 0.7;
}
</style>
