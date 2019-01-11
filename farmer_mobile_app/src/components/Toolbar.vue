<template>
  <f7-toolbar :bottom-md="true">
    <f7-row style="width: 100%">
      <f7-col width="20" class="text-align-center">
        <f7-link href="/">
          <img :src="`/static/farmer_mobile_app/img/toolbar/${icons.home}.svg`">
        </f7-link>
      </f7-col>
      <f7-col width="20" class="text-align-center">
        <f7-link href="/farm/">
          <img :src="`/static/farmer_mobile_app/img/toolbar/${icons.farm}.svg`">
        </f7-link>
      </f7-col>
      <f7-col width="20" class="text-align-center">
        <f7-link href="/nmp/">
          <img :src="`/static/farmer_mobile_app/img/toolbar/${icons.nmp}.svg`">
        </f7-link>
      </f7-col>
      <f7-col width="20" class="text-align-center">
        <f7-link href="/messaging/">
          <img :src="`/static/farmer_mobile_app/img/toolbar/${icons.messaging}.svg`">
        </f7-link>
      </f7-col>
      <f7-col width="20" class="text-align-center">
        <f7-link href="/services/">
          <img :src="`/static/farmer_mobile_app/img/toolbar/${icons.services}.svg`">
        </f7-link>
      </f7-col>
    </f7-row>
  </f7-toolbar>
</template>

<script>
export default {
  name: "fast-toolbar",
  computed: {
    icons() {
      let result = {
        home: "icon-activity",
        farm: "icon-barn",
        nmp: "icon-leaves",
        services: "icon-add-round",
        messaging: "icon-email"
      };

      result.home += "-" + this.$f7.theme;
      result.farm += "-" + this.$f7.theme;
      result.nmp += "-" + this.$f7.theme;
      result.services += "-" + this.$f7.theme;
      result.messaging += "-" + this.$f7.theme;

      if (this.$f7router.currentRoute.path) {
        let route = this.$f7router.currentRoute.path;

        if (route !== "/") {
          result.home += "-dim";
        }
        if (!route.startsWith("/farm/")) {
          result.farm += "-dim";
        }
        if (!route.startsWith("/nmp/")) {
          result.nmp += "-dim";
        }
        if (!route.startsWith("/services/")) {
          result.services += "-dim";
        }
        if (!route.startsWith("/messaging/")) {
          result.messaging += "-dim";
        }
      }
      return result;
    }
  }
};
</script>

<style scoped>
.toolbar img {
  max-width: 22px;
  max-height: 22px;
}
</style>
