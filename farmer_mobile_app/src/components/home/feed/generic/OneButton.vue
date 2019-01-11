<template>
  <f7-block strong class="no-margin-top" style="margin-bottom: 10px !important">
    <f7-block-header v-if="feedItem.header">
      <f7-row>
        <f7-col>{{ feedItem.header }}</f7-col>
        <f7-col class="text-align-right">
          <small>{{ $shortDate(feedItem.timestamp) }}</small>
        </f7-col>
      </f7-row>
    </f7-block-header>

    <p class="no-margin-top">{{ feedItem.text }}</p>
    <f7-row>
      <f7-link :href="feedItem.buttonHref">{{ feedItem.buttonText }}</f7-link>
    </f7-row>
    <f7-block-footer>
      <small>{{ $shortDate(feedItem.timestamp) }}</small>
    </f7-block-footer>
  </f7-block>
</template>

<script>
export default {
  name: "generic-one-button-feed-block",
  props: {
    feedItem: Object
  },
  data() {
    return {};
  }
};
</script>
