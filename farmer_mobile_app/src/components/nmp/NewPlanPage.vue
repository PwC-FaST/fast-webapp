<template>
  <f7-page>
    <f7-navbar title="New plan" back-link></f7-navbar>
    <fast-toolbar></fast-toolbar>

    <f7-block class="text-align-center">
      <p
        class="margin-bottom"
      >You will be guided through the creation of a new nutrient management plan.</p>
      <img src="/static/farmer_mobile_app/img/nmp-compute.svg">
    </f7-block>

    <f7-block>
      <f7-button
        fill
        big
        @click="onClickComputeAutomatically"
        class="margin-bottom"
      >Compute automatically</f7-button>
      <f7-button fill big @click="onClickComputeStepByStep">Compute step-by-step</f7-button>
    </f7-block>
  </f7-page>
</template>

<script>
import FastToolbar from "@/components/Toolbar.vue";

import gql from "graphql-tag";
import mutationCreatePlan from "./graphql/mutationCreatePlan.gql";

export default {
  name: "nmp-new-plan-page",
  components: {
    FastToolbar
  },
  apollo: {
    farm: {
      query: gql`
        {
          farm {
            id
          }
        }
      `,
      fetchPolicy: "cache-first"
    }
  },
  data() {
    return {
      newPlanName: null,
      farm: { loading: true }
    };
  },
  computed: {},
  methods: {
    createPlan() {
      return this.$apollo.mutate({
        mutation: mutationCreatePlan,
        variables: {
          farmId: this.farm.id
        }
      });
    },
    onClickComputeAutomatically() {
      this.$f7.progressbar.show();
      this.createPlan()
        .then(({ data }) => {
          this.$f7.progressbar.hide();
          this.$f7router.navigate(
            `/nmp/plan/${data.createPlan.plan.id}/results/`
          );
        })
        .catch(() => {
          this.$f7.progressbar.hide();
        });
    },
    onClickComputeStepByStep() {
      this.$f7.progressbar.show();
      this.createPlan()
        .then(({ data }) => {
          this.$f7.progressbar.hide();
          this.$f7router.navigate(
            `/nmp/plan/${data.createPlan.plan.id}/produced-manure/`
          );
        })
        .catch(() => {
          this.$f7.progressbar.hide();
        });
    }
  }
};
</script>
