<template>
  <f7-block strong class="no-margin-top" style="margin-bottom: 10px !important">
    <p>Vegetation index !.</p>
    <f7-row>
      <f7-link class="align-items-flex-end" href="/messaging/">Go to my inbox</f7-link>
      <f7-link class="align-items-flex-end" href="/messaging/">Read</f7-link>
    </f7-row>
  </f7-block>
</template>

<script>
export default {
  name: "messaging-feed-new-message",
  props: {
    content: Object
  },
  data() {
    return {};
  }
};
</script>
