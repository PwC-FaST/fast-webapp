<template>
  <l-map
    ref="map"
    :style="{height: height, width: width}"
    :zoom="zoom"
    :center="center"
    @update:zoom="onZoomChanged"
    @update:center="onCenterChanged"
  >
    <l-control-layers ref="layers_control"></l-control-layers>

    <l-tile-layer
      v-if="showGoogleSatelliteLayer"
      :url="googleSatelliteUrl"
      layer-type="base"
      visible
      name="Satellite"
    ></l-tile-layer>
    <l-tile-layer
      v-if="showGoogleSatelliteLayer"
      :url="googleHybridUrl"
      layer-type="base"
      name="Satellite and roads"
    ></l-tile-layer>

    <l-vectorgrid-protobuf
      v-if="showNatura2000Layer"
      ref="natura2000"
      :url="natura2000LayerURL"
      layer-type="overlay"
      name="Natura 2000"
      :options="natura2000LayerOptions"
    ></l-vectorgrid-protobuf>
    <l-vectorgrid-protobuf
      v-if="showHydrologyLayer"
      ref="hydro"
      :url="hydrologyLayerURL"
      layer-type="overlay"
      name="Hydrology"
      :options="hydrologyLayerOptions"
    ></l-vectorgrid-protobuf>
    <l-vectorgrid-protobuf
      v-if="showLpisLayer"
      ref="lpis"
      :visible="lpisLayerVisible"
      :url="lpisLayerURL"
      layer-type="overlay"
      name="LPIS parcels"
      :options="lpisLayerOptions"
      v-on:l-click="onClickLPISLayer"
    ></l-vectorgrid-protobuf>

    <l-circle-marker
      v-if="showGeolocation && geolocationLatLng && geolocationRadius"
      :lat-lng="geolocationLatLng"
      :radius="geolocationRadius"
      fillColor="#EE5158"
      color="#EE5158"
      :opacity="0.5"
      :fill-opacity="0.1"
    ></l-circle-marker>
    <l-circle-marker
      v-if="showGeolocation && geolocationLatLng && geolocationRadius"
      :lat-lng="geolocationLatLng"
      :radius="8"
      fillColor="#EE5158"
      color="#EE5158"
      :opacity="1.0"
      :fill-opacity="0.9"
    ></l-circle-marker>

    <l-control position="bottomright">
      <div class="leaflet-control-zoom leaflet-bar leaflet-control" style="margin: 0">
        <a
          v-if="!farm.loading && !farm.errors"
          class="leaflet-control-zoom-in"
          @click="centerMap('farm')"
        >
          <img src="/static/farmer_mobile_app/img/barn.svg" width="16" height="16">
        </a>
        <a
          v-if="geolocationLatLng"
          class="leaflet-control-zoom-out"
          @click="centerMap('geolocation')"
        >
          <img src="/static/farmer_mobile_app/img/geolocation.svg" width="16" height="16">
        </a>
      </div>
    </l-control>

    <l-control v-if="selectedLpisParcelId && actionButtonText" position="bottomleft">
      <f7-button fill big class="color-yellow" @click="onClickActionButton">{{ actionButtonText }}</f7-button>
    </l-control>
  </l-map>
</template>

<script>
import Vue2LeafletVectorGridProtobuf from "vue2-leaflet-vectorgrid";
import { LControlLayers, LControl, LMap, LCircleMarker } from "vue2-leaflet";
import L from "leaflet";

import queryFarm from "./graphql/queryFarm.gql";
import queryFarmParcel from "./graphql/queryFarmParcel.gql";

import {
  lpisStyleSelected,
  lpisStylePrimary,
  lpisStyleSecondary,
  lpisStyleDefault,
  hydroStyle,
  natura2000Style
} from "./map-styles";

export default {
  name: "farm-parcel-map",
  components: {
    "l-vectorgrid-protobuf": Vue2LeafletVectorGridProtobuf,
    "l-control-layers": LControlLayers,
    "l-control": LControl,
    "l-circle-marker": LCircleMarker,
    "l-map": LMap
  },
  props: {
    width: {
      type: String,
      default: (window.innerWidth || window.clientWidth) + "px"
    },
    height: {
      type: String,
      default: (window.innerWidth || window.clientWidth) + "px"
    },
    centerInit: { type: String, default: "primary" }, // either 'farm', 'primary', 'coords', 'geolocation'
    centerInitCoords: {
      type: Array,
      default() {
        return null;
      }
    },
    farmId: { type: String, default: null },
    farmParcelId: { type: String, default: null },
    showGeolocation: { type: Boolean, default: true },
    showGoogleSatelliteLayer: { type: Boolean, default: true },
    showLpisLayer: { type: Boolean, default: true },
    showHydrologyLayer: { type: Boolean, default: true },
    showNatura2000Layer: { type: Boolean, default: true },
    lpisLayerInteractive: { type: Boolean, default: false },
    preSelectedLpisParcelId: { type: String, default: null },
    lpisLayerStyleSelected: {
      type: Object,
      default() {
        return lpisStyleSelected;
      }
    },
    lpisLayerStylePrimary: {
      type: Object,
      default() {
        return lpisStylePrimary;
      }
    },
    lpisLayerStyleSecondary: {
      type: Object,
      default() {
        return lpisStyleSecondary;
      }
    },
    lpisLayerStyleDefault: {
      type: Object,
      default() {
        return lpisStyleDefault;
      }
    },
    hydrologyLayerStyle: {
      type: Object,
      default() {
        return hydroStyle;
      }
    },
    natura2000LayerStyle: {
      type: Object,
      default() {
        return natura2000Style;
      }
    },
    actionButtonText: { type: String, default: null }
  },
  apollo: {
    farmParcel: {
      query: queryFarmParcel,
      variables() {
        return {
          farmParcelId: Number(this.farmParcelId)
        };
      },
      fetchPolicy: "cache-first",
      skip() {
        return !this.farmParcelId;
      },
      result(r) {
        this.centerMap(this.centerInit, this.centerInitCoords);
      }
    },
    farm: {
      query: queryFarm,
      variables() {
        return {
          farmParcelId: Number(this.farmId)
        };
      },
      fetchPolicy: "cache-first",
      skip() {
        return !this.farmId;
      },
      result(r) {
        this.centerMap(this.centerInit, this.centerInitCoords);
      }
    }
  },
  data() {
    return {
      farm: { loading: true },
      farmParcel: { loading: true },
      selectedLpisParcelId: this.preSelectedLpisParcelId,
      googleSatelliteUrl:
        "http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}",
      googleHybridUrl:
        "http://www.google.cn/maps/vt?lyrs=y@189&gl=cn&x={x}&y={y}&z={z}",
      lpisLayerURL: "https://map.fast.sobloo.io/layer/lpis/{z}/{x}/{y}.pbf",
      lpisLayerVisible: this.showLpisLayer,
      hydrologyLayerURL:
        "https://map.fast.sobloo.io/layer/hydro/{z}/{x}/{y}.pbf",
      hydrologyLayerVisible: this.showHydrologyLayer,
      natura2000LayerURL:
        "https://map.fast.sobloo.io/layer/natura2000/{z}/{x}/{y}.pbf",
      natura2000LayerVisible: this.showNatura2000Layer,
      zoom: 16,
      center: [46.2276, 2.2137], // center of France,
      geolocationPosition: null,
      geolocationLatLng: null,
      geolocationRadius: null,
      geolocationWatchHandle: null
    };
  },
  mounted() {
    this.$nextTick(() => {
      // Leaflet map object is only available on next tick after the component is mounted
      this.centerMap(this.centerInit, this.centerInitCoords);

      const map = this.$refs["layers_control"].mapObject;
      const layersControl = this.$refs["layers_control"].mapObject;
      const lpisLayer = this.$refs["lpis"].mapObject;
      const hydrologyLayer = this.$refs["hydro"].mapObject;
      const natura2000Layer = this.$refs["natura2000"].mapObject;

      // Register the layers into the layers control
      // must be in this order to ensure correct zIndex
      if (this.showNatura2000Layer) {
        layersControl.addOverlay(natura2000Layer, "Natura 2000");
      }
      if (this.showHydrologyLayer) {
        layersControl.addOverlay(hydrologyLayer, "Hydrology");
      }
      if (this.showLpisLayer) {
        // Register callbacks for the selectable LPIS layer
        // (the @click callbacks directly on the Vue component do not seem to work)
        lpisLayer.on("click", this.onClickLPISLayer);
        if (this.preSelectedLpisParcelId) {
          lpisLayer.redraw();
        }
        layersControl.addOverlay(lpisLayer, "LPIS parcels");
      }

      if (navigator.geolocation && this.showGeolocation) {
        // Plug the geolocation callbacks into an asynchronous call, as it seems navigator.geolocation.watchPosition
        // might sometimes block the render thread
        window.setTimeout(() => {
          // Force get current position at least once before running watchPosition
          navigator.geolocation.getCurrentPosition(position => {
            this.geolocationPosition = position;
            this.updateGeolocationMarker();
          });
          // Register a callback to update the current position marker every time the GPS coordinates change
          this.geolocationWatchHandle = navigator.geolocation.watchPosition(
            position => {
              this.geolocationPosition = position;
              this.updateGeolocationMarker();
            }
          );
        }, 0);
      }
    });
  },
  beforeDestroy() {
    if (navigator.geolocation && this.showGeolocation) {
      navigator.geolocation.clearWatch(this.geolocationWatchHandle);
      this.geolocationWatchHandle = null;
      this.geolocationPosition = null;
      this.geolocationLatLng = null;
      this.geolocationRadius = null;
    }
  },
  computed: {
    primaryParcelLpisId() {
      if (this.farmParcel.lpisParcelId) {
        return this.farmParcel.lpisParcelId;
      } else {
        return null;
      }
    },
    secondaryParcelsLpisIds() {
      if (this.farm.farmParcels) {
        return this.farm.farmParcels.map(fp => fp.lpisParcelId);
      } else {
        return [];
      }
    },
    lpisLayerOptions() {
      return {
        zIndex: 10,
        rendererFactory: L.svg.tile,
        vectorTileLayerStyles: {
          lpis: (properties, zoom) => {
            if (properties.id === this.selectedLpisParcelId) {
              return this.lpisLayerStyleSelected;
            } else if (properties.id === this.primaryParcelLpisId) {
              return this.lpisLayerStylePrimary;
            } else if (
              this.secondaryParcelsLpisIds.indexOf(properties.id) > -1
            ) {
              return this.lpisLayerStyleSecondary;
            } else {
              return this.lpisLayerStyleDefault;
            }
          }
        },
        interactive: this.lpisLayerInteractive,
        getFeatureId: function(feat) {
          return feat.id;
        },
        attribution: '&copy; <a href="http://www.fast.eu">FaST</a>'
      };
    },
    hydrologyLayerOptions() {
      return {
        rendererFactory: L.svg.tile,
        vectorTileLayerStyles: {
          hydro: hydroStyle
        },
        interactive: false,
        getFeatureId: function(feat) {
          return feat.id;
        },
        attribution: '&copy; <a href="http://www.fast.eu">FaST</a>'
      };
    },
    natura2000LayerOptions() {
      return {
        rendererFactory: L.svg.tile,
        vectorTileLayerStyles: {
          natura2000: natura2000Style
        },
        interactive: false,
        getFeatureId: function(feat) {
          return feat.id;
        },
        attribution: '&copy; <a href="http://www.fast.eu">FaST</a>'
      };
    }
  },
  methods: {
    updateGeolocationMarker() {
      if (this.geolocationPosition) {
        const map = this.$refs["map"].mapObject;
        const metresPerPixel =
          (40075016.686 *
            Math.abs(
              Math.cos(
                (this.geolocationPosition.coords.latitude * 180) / Math.PI
              )
            )) /
          Math.pow(2, map.getZoom() + 8);
        this.geolocationLatLng = L.latLng(
          this.geolocationPosition.coords.latitude,
          this.geolocationPosition.coords.longitude
        );
        this.geolocationRadius =
          this.geolocationPosition.coords.accuracy / metresPerPixel;
      }
    },
    centerMap(centerOn, centerCoords) {
      if (centerOn === "primary" && this.farmParcel.gisInfo) {
        let centroids = this.farmParcel.gisInfo.centroid;
        let epsg4326Index = centroids.findIndex(
          x => x.coordinateReferenceSystem === "EPSG:4326"
        );
        this.center = [centroids[epsg4326Index].y, centroids[epsg4326Index].x];
      } else if (centerOn === "farm" && this.farm.gisInfo) {
        let centroids = this.farm.gisInfo.centroid;
        let epsg4326Index = centroids.findIndex(
          x => x.coordinateReferenceSystem === "EPSG:4326"
        );
        this.center = [centroids[epsg4326Index].y, centroids[epsg4326Index].x];
      } else if (centerOn === "coords" && centerCoords) {
        this.center = centerCoords;
      } else if (centerOn === "geolocation" && this.geolocationLatLng) {
        this.center = this.geolocationLatLng;
      } else {
        this.center = [46.2276, 2.2137]; // center of France
      }
    },
    onClickActionButton() {
      this.$emit("click-action-button", {
        lpisParcelId: this.selectedLpisParcelId,
        lpisParcelCentroid: this.selectedParcelCentroid
      });
    },
    onClickLPISLayer(e) {
      const parcelId = e.layer.properties.id;
      if (this.secondaryParcelsLpisIds.indexOf(parcelId) === -1) {
        this.selectedLpisParcelId =
          parcelId === this.selectedLpisParcelId ? null : parcelId;
        this.selectedParcelCentroid = [e.latlng.lat, e.latlng.lng];
        this.$refs["lpis"].mapObject.redraw();
      }
    },
    onZoomChanged(e) {
      this.updateGeolocationMarker();
    },
    onCenterChanged(e) {
      this.updateGeolocationMarker();
    }
  }
};
</script>

<style scoped>
</style>
