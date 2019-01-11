<template>
  <f7-page ptr @ptr:refresh="onPullToRefresh">
    <fast-navbar title="Nutrient management"></fast-navbar>
    <fast-toolbar></fast-toolbar>

    <template v-if="plans.loading">
      <p>Loading...</p>
    </template>

    <template v-else></template>

    <f7-block-title>
      <img
        src="/static/farmer_mobile_app/img/toolbar/icon-leaves-ios.svg"
        style="height: 16px; margin-right: 10px;"
      >
      Active plan
    </f7-block-title>

    <f7-list>
      <f7-list-item
        v-for="plan in activePlans"
        :key="plan.id"
        :title="plan.name"
        :footer="`Last updated: ${$shortDate(plan.updatedAt || plan.createdAt)}`"
        @click.native="onClickPlanItem(plan, $event)"
        swipeout
        @swipeout:delete="onDeletePlan(plan)"
      >
        <span slot="after">
          <f7-icon f7="gear" @click.native="onClickPlanSettings(plan)" class="margin-right"></f7-icon>
          <f7-icon f7="favorites" @click.native="onClickPlan(plan)"></f7-icon>
        </span>
        <f7-swipeout-actions right>
          <f7-swipeout-button
            delete
            :confirm-text="`Do you wish to delete plan ${plan.name}?`"
          >Delete</f7-swipeout-button>
        </f7-swipeout-actions>
      </f7-list-item>

      <f7-list-item v-if="activePlans.length === 0" title="No active plan"></f7-list-item>
    </f7-list>

    <template v-if="inactivePlans.length > 0">
      <f7-block-title>
        <img
          src="/static/farmer_mobile_app/img/toolbar/icon-leaves-ios-dim.svg"
          style="height: 16px; margin-right: 10px;"
        >
        Inactive plans
      </f7-block-title>
      <f7-list>
        <f7-list-item
          v-for="plan in inactivePlans"
          :key="plan.id"
          :title="plan.name"
          :footer="`Last updated: ${$shortDate(plan.updatedAt || plan.createdAt)}`"
          @click.native="onClickPlanItem(plan, $event)"
          swipeout
          @swipeout:delete="onDeletePlan(plan)"
        >
          <span slot="after">
            <f7-icon f7="gear" @click.native="onClickPlanSettings(plan)" class="margin-right"></f7-icon>
            <f7-icon f7="favorites" @click.native="onClickPlan(plan)"></f7-icon>
            <f7-swipeout-actions right>
              <f7-swipeout-button
                delete
                :confirm-text="`Do you wish to delete plan ${plan.name}?`"
              >Delete</f7-swipeout-button>
            </f7-swipeout-actions>
          </span>
        </f7-list-item>
      </f7-list>
    </template>

    <f7-block>
      <f7-button fill big href="/nmp/new/">Create a new plan</f7-button>
    </f7-block>
  </f7-page>
</template>

<script>
import FastToolbar from "@/components/Toolbar.vue";
import FastNavbar from "@/components/Navbar.vue";

import queryPlans from "./graphql/queryPlans.gql";
import mutationDeletePlan from "./graphql/mutationDeletePlan.gql";

export default {
  name: "nmp-page",
  components: {
    FastToolbar,
    FastNavbar
  },
  apollo: {
    plans: {
      query: queryPlans,
      fetchPolicy: "cache-and-network"
    }
  },
  data() {
    return {
      plans: { loading: true }
    };
  },
  computed: {
    activePlans() {
      return this.plans instanceof Array
        ? this.plans.filter(x => x.isActive)
        : [];
    },
    inactivePlans() {
      return this.plans instanceof Array
        ? this.plans.filter(x => !x.isActive)
        : [];
    }
  },
  methods: {
    onPullToRefresh(e, done) {
      this.$apollo.queries.plans.refetch().then(done);
    },
    onClickPlanItem(plan, e) {
      if (
        e.target.tagName !== "I" &&
        !e.target.classList.contains("swipeout-delete")
      ) {
        this.onClickPlan(plan);
      }
    },
    onClickPlan(plan) {
      this.$f7router.navigate(`/nmp/plan/${plan.id}/results/`);
    },
    onClickPlanSettings(plan) {
      this.$f7router.navigate(`/nmp/plan/${plan.id}/produced-manure/`);
    },
    onDeletePlan(plan) {
      this.$f7.progressbar.show();
      this.$apollo
        .mutate({
          mutation: mutationDeletePlan,
          variables: {
            planId: plan.id
          }
        })
        .then(() => {
          return this.$apollo.queries.plans.refetch();
        })
        .then(() => {
          this.$f7.progressbar.hide();
        })
        .catch(() => {
          this.$f7.progressbar.hide();
        });
    }
  }
};
</script>
