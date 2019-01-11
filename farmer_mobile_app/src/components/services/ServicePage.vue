<template>
  <f7-page ptr @ptr:refresh="onPullToRefresh">
    <f7-navbar :title="title" back-link></f7-navbar>
    <fast-toolbar></fast-toolbar>

    <f7-block v-if="!service.loading && !service.error" strong class="no-margin-top">
      <p>{{ service.shortDescription || '' }}</p>
      <p>{{ service.subscriptionType.displayName || '' }}</p>

      <f7-row class="margin-bottom margin-top">
        <f7-col>
          <img :src="`/media/${service.provider.logo}`" style="{width: 100px; height: 100px;}">
        </f7-col>
        <f7-col>
          <h4>{{ service.provider.displayName }}</h4>
        </f7-col>
      </f7-row>

      <f7-button v-if="!subscribed" big @click="onClickSubscribe(true)" fill>Subscribe</f7-button>
      <f7-button v-else big @click="onClickSubscribe(false)">Unsubscribe</f7-button>
    </f7-block>
  </f7-page>
</template>

<script>
import FastToolbar from "@/components/Toolbar";
import queryService from "./gql/queryService.gql";
import queryServices from "./gql/queryServices.gql";
import mutationUpdateUserServiceSubscription from "./gql/mutationUpdateUserServiceSubscription.gql";

export default {
  name: "fast-additional-services",
  components: {
    FastToolbar
  },
  props: {
    _id: String
  },
  apollo: {
    service: {
      query: queryService,
      variables() {
        return {
          id: Number(this._id)
        };
      },
      pollInterval: 60000,
      fetchPolicy: "cache-and-network"
    }
  },
  data() {
    return {
      id: Number(this._id),
      service: { loading: true }
    };
  },
  computed: {
    title() {
      return this.service.loading
        ? "Loading..."
        : this.service.error
        ? "Error"
        : this.service.displayName;
    },
    subscribed() {
      return (
        this.service.userSubscriptions &&
        this.service.userSubscriptions.length > 0
      );
    }
  },
  methods: {
    onClickSubscribe(subscribe) {
      this.$f7.progressbar.show();
      this.$apollo
        .mutate({
          mutation: mutationUpdateUserServiceSubscription,
          variables: {
            serviceId: this.id,
            subscribe: subscribe
          },
          refetchQueries: [
            {
              query: queryServices,
              variables: {}
            }
          ]
        })
        .then(() => {
          this.$f7.progressbar.hide();
        })
        .catch(() => {
          this.$f7.progressbar.hide();
        });
    },
    onPullToRefresh(e, done) {
      this.$apollo.queries.service.refetch().then(done);
    }
  }
};
</script>
