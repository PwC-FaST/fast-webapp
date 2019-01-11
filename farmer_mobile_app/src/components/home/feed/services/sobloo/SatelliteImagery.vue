<template>
  <f7-block strong class="no-margin-top" style="margin-bottom: 10px !important">
    <f7-block-header>
      <f7-row>
        <f7-col width="75">Sentinel 2&nbsp;|&nbsp;Latest cloudless image</f7-col>
        <f7-col width="25" class="text-align-right">
          <small
            v-if="servicesSoblooLatestSentinel2Layer.collectedAt"
          >{{ $shortDate(servicesSoblooLatestSentinel2Layer.collectedAt) }}</small>
        </f7-col>
      </f7-row>
    </f7-block-header>

    <l-map
      ref="map"
      :style="{height: '300px', width: '100%'}"
      :zoom="zoom"
      :center="center"
      :crs="crs"
      @click="onClickMap"
    >
      <l-tile-layer
        v-if="servicesSoblooLatestSentinel2Layer.wmtsLayerUrl"
        :url="servicesSoblooLatestSentinel2Layer.wmtsLayerUrl"
        ref="sentinel"
        layer-type="base"
        attribution="EU Copernicus | Sentinel"
        :crs="crs"
        name="Sentinel 2"
      >∏</l-tile-layer>
    </l-map>

    <f7-block-footer v-if="feedItem.service">
      <f7-row>
        <f7-col>
          <small>{{ servicesSoblooLatestSentinel2Layer.missionName }}</small>
        </f7-col>
        <f7-col class="text-align-right">
          <f7-link :href="`/services/service/${feedItem.service.id}/`">
            <small>{{ feedItem.service.provider.shortName }}</small>
            <img
              v-if="feedItem.service.provider.logo"
              height="17"
              :src="`/media/${feedItem.service.provider.logo}`"
              style="margin-left: 5px"
            >
          </f7-link>
        </f7-col>
      </f7-row>
    </f7-block-footer>

    <f7-popup :opened="popupOpened" @popup:closed="popupOpened = false">
      <f7-page>
        <f7-navbar :title="$shortDate(servicesSoblooLatestSentinel2Layer.collectedAt)">
          <f7-nav-right>
            <f7-link popup-close>Close</f7-link>
          </f7-nav-right>
        </f7-navbar>
        <l-map
          ref="map-popup"
          :style="{height: '100%', width: '100%'}"
          :zoom="zoom"
          :center="center"
          :crs="crs"
        >
          <l-tile-layer
            v-if="servicesSoblooLatestSentinel2Layer.wmtsLayerUrl"
            :url="servicesSoblooLatestSentinel2Layer.wmtsLayerUrl"
            ref="sentinel-popup"
            layer-type="base"
            attribution="EU Copernicus | Sentinel"
            :crs="crs"
            name="Sentinel"
          >∏</l-tile-layer>
          <l-control v-show="servicesSoblooLatestSentinel2Layer.loading" position="bottomright">
            <span class="bg-color-blue1 text-color-blue3 padding">Loading...</span>
          </l-control>
        </l-map>
      </f7-page>
    </f7-popup>
  </f7-block>
</template>

<script>
import { LControlLayers, LControl, LMap, LCircleMarker } from "vue2-leaflet";

import queryFarm from "@/components/farm/graphql/queryFarm.gql";
import queryServicesSoblooLatestSentinel2Layer from "./queryServicesSoblooLatestSentinel2Layer.gql";

export default {
  name: "services-sobloo-satellite-image",
  components: { LControl },
  props: {
    feedItem: Object
  },
  apollo: {
    farm: {
      query: queryFarm,
      fetchPolicy: "cache-first"
    },
    servicesSoblooLatestSentinel2Layer: {
      query: queryServicesSoblooLatestSentinel2Layer,
      variables() {
        return {
          latitude: this.farmCenterEPSG4326[0],
          longitude: this.farmCenterEPSG4326[1],
          maxCloudCover: 0.5
        };
      },
      fetchPolicy: "cache-first",
      skip() {
        return !this.farmCenterEPSG4326;
      },
      result({ data, loading, networkStatus }) {
        this.recomputeCenter();
        this.$nextTick(() => {
          this.$refs["sentinel"].mapObject.getContainer().style.filter =
            "brightness(200%)";
        });
      }
    }
  },
  data() {
    return {
      popupOpened: false,
      farm: { loading: true },
      servicesSoblooLatestSentinel2Layer: { loading: true },
      zoom: 14,
      center: [0, 0],
      crs: L.CRS.EPSG4326
    };
  },
  mounted() {},
  computed: {
    farmCenterEPSG4326() {
      if (this.farm.gisInfo) {
        let centroids = this.farm.gisInfo.centroid;
        let epsg4326Index = centroids.findIndex(
          x => x.coordinateReferenceSystem === "EPSG:4326"
        );
        return [centroids[epsg4326Index].y, centroids[epsg4326Index].x];
      } else {
        return null;
      }
    },
    farmParcelLpisIds() {
      if (this.farm.farmParcels) {
        return this.farm.farmParcels.map(p => p.lpisParcelId);
      } else {
        return [];
      }
    }
  },
  methods: {
    recomputeCenter() {
      this.center = this.farmCenterEPSG4326;
    },
    onClickMap() {
      this.popupOpened = true;
      this.$nextTick(() => {
        this.$refs["sentinel-popup"].mapObject.getContainer().style.filter =
          "brightness(200%)";
        this.$refs["map-popup"].mapObject.invalidateSize();
      });
    }
  }
};
</script>
