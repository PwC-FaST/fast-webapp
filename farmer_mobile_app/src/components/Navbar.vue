<template>
  <f7-navbar v-if="$f7.theme === 'ios'">
    <f7-nav-left>
      <f7-link panel-open="left">
        <img src="/static/farmer_mobile_app/img/logo-no-eu.svg" style="width: 22px; height: 22px;">
      </f7-link>
    </f7-nav-left>
    <f7-nav-title>{{ title }}</f7-nav-title>
    <f7-nav-right>
      <slot name="nav-right"></slot>
    </f7-nav-right>
  </f7-navbar>

  <f7-navbar v-else>
    <f7-nav-title>
      <f7-link panel-open="left" class="no-padding-left no-padding-right">
        <img
          src="/static/farmer_mobile_app/img/logo-no-eu.svg"
          style="width: 22px; height: 22px; vertical-align: top; margin-right: 10px;"
        >
        {{ title }}
      </f7-link>
    </f7-nav-title>
    <f7-nav-right>
      <slot name="nav-right"></slot>
    </f7-nav-right>
  </f7-navbar>
</template>

<script>
export default {
  name: "fast-navbar",
  props: {
    title: { type: String, required: true }
  },
  data() {
    return {};
  },
  computed: {}
};
</script>

<style scoped>
.toolbar img {
  max-width: 22px;
  max-height: 22px;
}
</style>
