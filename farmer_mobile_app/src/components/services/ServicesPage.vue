<template>
  <f7-page ptr @ptr:refresh="onPullToRefresh">
    <fast-navbar title="Additional services"></fast-navbar>
    <fast-toolbar></fast-toolbar>

    <template v-if="!services.loading && services.some(s => s.userSubscriptions.length > 0)">
      <f7-block-title>Subscribed services</f7-block-title>
      <f7-list media-list>
        <f7-list-item
          v-for="service in subscribedServices"
          :key="service.id"
          :link="`/services/service/${service.id}/`"
          :title="service.displayName"
          :header="'subscribed: ' + $shortDate(service.userSubscriptions[0].subscribedAt)"
          :subtitle="service.provider.shortName"
          :text="service.shortDescription"
        >
          <img slot="media" :src="`/media/${service.provider.logo}`" width="60">
        </f7-list-item>
      </f7-list>
    </template>

    <f7-block-title>Additional services</f7-block-title>
    <f7-list v-if="!services.loading" media-list>
      <f7-list-item
        v-for="service in notSubscribedServices"
        :key="service.id"
        :link="`/services/service/${service.id}/`"
        :title="service.displayName"
        :after="service.subscriptionType.displayName"
        :subtitle="service.provider.shortName"
        :text="service.shortDescription"
      >
        <img slot="media" :src="`/media/${service.provider.logo}`" width="60">
      </f7-list-item>
    </f7-list>
  </f7-page>
</template>

<script>
import FastToolbar from "@/components/Toolbar.vue";
import FastNavbar from "@/components/Navbar.vue";

import queryServices from "./gql/queryServices.gql";

export default {
  name: "fast-additional-services",
  components: {
    FastToolbar,
    FastNavbar
  },
  props: {
    _id: String
  },
  apollo: {
    services: {
      query: queryServices,
      fetchPolicy: "cache-and-network"
    }
  },
  data() {
    return {
      services: { loading: true }
    };
  },
  computed: {
    subscribedServices() {
      if (this.services instanceof Array) {
        return this.services.filter(s => s.userSubscriptions.length > 0);
      } else {
        return [];
      }
    },
    notSubscribedServices() {
      if (this.services instanceof Array) {
        return this.services.filter(s => s.userSubscriptions.length === 0);
      } else {
        return [];
      }
    }
  },
  methods: {
    onPullToRefresh(e, done) {
      this.$apollo.queries.services.refetch().then(done);
    }
  }
};
</script>
