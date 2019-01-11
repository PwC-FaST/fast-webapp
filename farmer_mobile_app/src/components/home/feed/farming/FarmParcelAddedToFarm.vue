<template>
  <f7-block strong class="no-margin-top" style="margin-bottom: 10px !important">
    <f7-block-header>
      <f7-row>
        <f7-col>My farm</f7-col>
        <f7-col class="text-align-right">
          <small>{{ $shortDate(feedItem.timestamp) }}</small>
        </f7-col>
      </f7-row>
    </f7-block-header>

    <a :href="`/farm/parcel/${feedItem.farmParcel.id}/`">
      <farm-parcel-snapshot
        style="float: left; margin-right: 20px;"
        :svg="feedItem.farmParcel.snapshotSvg"
        :width="60"
        :height="60"
      ></farm-parcel-snapshot>
    </a>
    <div style="display: inline">
      <p class="no-margin-top">You have added parcel
        <f7-link :href="`/farm/parcel/${feedItem.farmParcel.id}/`">{{ feedItem.farmParcel.name }}</f7-link> to your farm
        <f7-link href="/farm/">{{ feedItem.farmParcel.farm.name }}</f7-link>.
      </p>
      <div class="text-align-right">
        <f7-link :href="`/farm/parcel/${feedItem.farmParcel.id}/`">View parcel</f7-link>
      </div>
    </div>
  </f7-block>
</template>

<script>
import FarmParcelSnapshot from "@/components/farm/FarmParcelSnapshot.vue";

export default {
  name: "farming-farm-parcel-added-to-farm-feed-block",
  components: {
    "farm-parcel-snapshot": FarmParcelSnapshot
  },
  props: {
    feedItem: Object
  },
  data() {
    return {};
  }
};
</script>
