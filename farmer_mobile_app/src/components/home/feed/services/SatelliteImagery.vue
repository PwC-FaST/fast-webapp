<template>
  <f7-block strong class="no-margin-top" style="margin-bottom: 10px !important">
    <f7-block-header>
      <f7-row>
        <f7-col width="75">Satellite Imagery&nbsp;|&nbsp;{{ feedItem.title }}</f7-col>
        <f7-col width="25" class="text-align-right">
          <small>{{ $shortDate(feedItem.timestamp) }}</small>
        </f7-col>
      </f7-row>
    </f7-block-header>

    <l-map
      ref="map"
      :style="{height: '300px', width: '100%'}"
      :zoom="zoom"
      :center="center"
    >
      <l-tile-layer :url="googleSatelliteUrl" layer-type="base" visible name="Satellite"></l-tile-layer>
      <l-vectorgrid-protobuf
        ref="lpis"
        :url="lpisLayerURL"
        layer-type="overlay"
        name="LPIS parcels"
        :options="lpisLayerOptions"
      ></l-vectorgrid-protobuf>
    </l-map>

    <f7-block-footer>
      <f7-row>
        <f7-col>
          <small>Demo imagery</small>
        </f7-col>
        <f7-col class="text-align-right">
          <f7-link :href="`/services/service/${feedItem.service.id}/`">
            <small>{{ feedItem.service.provider.displayName }}</small>
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
  </f7-block>
</template>

<script>
import Vue2LeafletVectorGridProtobuf from "vue2-leaflet-vectorgrid";
import "leaflet.vectorgrid";
import { LControlLayers, LControl, LMap, LCircleMarker } from "vue2-leaflet";

const plotty = require("plotty");

L.LeafletGeotiff.Plotty = L.LeafletGeotiffRenderer.extend({
  options: {
    colorScale: "viridis",
    clampLow: true,
    clampHigh: true,
    displayMin: 0,
    displayMax: 1
  },

  initialize: function(options) {
    if (typeof plotty === "undefined") {
      throw new Error("plotty not defined");
    }
    this.name = "Plotty";

    L.setOptions(this, options);

    this._preLoadColorScale();
  },

  setColorScale: function(colorScale) {
    this.options.colorScale = colorScale;
    this.parent._reset();
  },

  setDisplayRange: function(min, max) {
    this.options.displayMin = min;
    this.options.displayMax = max;
    this.parent._reset();
  },

  _preLoadColorScale: function() {
    var canvas = document.createElement("canvas");
    var plot = new plotty.plot({
      canvas: canvas,
      data: [0],
      width: 1,
      height: 1,
      domain: [this.options.displayMin, this.options.displayMax],
      colorScale: this.options.colorScale,
      clampLow: this.options.clampLow,
      clampHigh: this.options.clampHigh
    });
    this.colorScaleData = plot.colorScaleCanvas.toDataURL();
  },

  render: function(raster, canvas, ctx, args) {
    var plottyCanvas = document.createElement("canvas");
    var plot = new plotty.plot({
      data: raster.data,
      width: raster.width,
      height: raster.height,
      domain: [this.options.displayMin, this.options.displayMax],
      colorScale: this.options.colorScale,
      clampLow: this.options.clampLow,
      clampHigh: this.options.clampHigh,
      canvas: plottyCanvas,
      useWebGL: false
    });
    plot.setNoDataValue(-9999);
    plot.render();

    this.colorScaleData = plot.colorScaleCanvas.toDataURL();

    var rasterImageData = plottyCanvas
      .getContext("2d")
      .getImageData(0, 0, plottyCanvas.width, plottyCanvas.height);
    var imageData = this.parent.transform(rasterImageData, args);
    ctx.putImageData(imageData, args.xStart, args.yStart);
  }
});

L.LeafletGeotiff.plotty = function(options) {
  return new L.LeafletGeotiff.Plotty(options);
};

import {
  lpisStyleSelected,
  lpisStylePrimary,
  lpisStyleSecondary,
  lpisStyleDefault,
  hydroStyle,
  natura2000Style
} from "@/components/farm/map-styles";

import queryFarm from "@/components/farm/graphql/queryFarm.gql";

export default {
  name: "services-satellite-image",
  components: {
    "l-vectorgrid-protobuf": Vue2LeafletVectorGridProtobuf
  },
  props: {
    feedItem: Object
  },
  apollo: {
    farm: {
      query: queryFarm,
      fetchPolicy: "cache-first",
      result({ data, loading, networkStatus }) {
        this.loadGeoTiffs();
        this.recomputeCenter();
      }
    }
  },
  data() {
    return {
      farm: { loading: true },
      zoom: 15,
      center: [0, 0],
      googleSatelliteUrl:
        "http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}",
      lpisLayerURL: "https://map.fast.sobloo.io/layer/lpis/{z}/{x}/{y}.pbf",
      lpisStylePrimary: lpisStylePrimary,
      hasLoaded: false
    };
  },
  mounted() {},
  computed: {
    lpisLayerOptions() {
      return {
        rendererFactory: L.svg.tile,
        vectorTileLayerStyles: {
          lpis: (properties, zoom) => {
            return this.lpisLayerStylePrimary;
          }
        },
        interactive: false,
        getFeatureId: function(feat) {
          return feat.id;
        }
      };
    }
  },
  methods: {
    loadGeoTiffs() {
      if (this.hasLoaded) return;
      this.hasLoaded = true;
      this.$nextTick(() => {
        const map = this.$refs["map"].mapObject;
        // const layersControl = this.$refs['layers_control'].mapObject
        //
        // const lpisLayer = L.vectorGrid.protobuf(
        //   this.lpisLayerURL,
        //   {
        //     visible: true,
        //     rendererFactory: L.svg.tile,
        //     vectorTileLayerStyles: {
        //       lpis: (properties, zoom) => {
        //         return this.lpisLayerStylePrimary
        //       }
        //     },
        //     layerType: 'overlay',
        //     name: 'LPIS parcels',
        //     interactive: false,
        //     getFeatureId: function (feat) {
        //       return feat.id
        //     }
        //   }
        // )
        // map.addLayer(lpisLayer)
        //layersControl.addOverlay(lpisLayer, 'LPIS parcels')

        const url = `/static/geotiffs/${this.farm.id}/${
          this.feedItem.band
        }.tif`;

        const layer = L.leafletGeotiff(url, {
          name: this.feedItem.band,
          visible: true,
          layerType: "base",
          name: "LPIS parcels",
          renderer: L.LeafletGeotiff.plotty({
            displayMin: 0,
            displayMax: 255,
            colorScale: this.feedItem.colorScale
          })
        });
        map.addLayer(layer);
        //layersControl.addBaseLayer(layer, this.feedItem.title)
      });
    },
    recomputeCenter() {
      let centroids = this.farm.gisInfo.centroid;
      let epsg4326Index = centroids.findIndex(
        x => x.coordinateReferenceSystem === "EPSG:4326"
      );
      this.center = [centroids[epsg4326Index].y, centroids[epsg4326Index].x];
    }
  }
};
</script>
