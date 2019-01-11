<template>
  <f7-page ptr @ptr:refresh="onPullToRefresh">
    <f7-navbar title="Manure production" back-link>
      <f7-nav-right>
        <f7-link :href="`/nmp/plan/${planId}/import-export-manure/`">Next</f7-link>
      </f7-nav-right>
    </f7-navbar>
    <fast-toolbar></fast-toolbar>

    <template v-if="plan.loading">
      <p>Loading...</p>
    </template>

    <template v-else-if="plan.errors">
      <p>Content could not be retrieved, try to refresh.</p>
    </template>

    <template v-else>
      <f7-block>
        <p>
          These are estimates of manure production based on your livestock inventory and average values for each type
          of animal.
        </p>
        <p>You are free to use the default values or input your own values.</p>
      </f7-block>

      <produced-manure-block
        v-for="manure in plan.producedLivestockManures"
        :id="manure.id"
        :key="manure.id"
        :manure-init="manure"
        @change="onChangeManureBlockValues"
      ></produced-manure-block>

      <f7-block-title>Totals</f7-block-title>
      <f7-list strong>
        <f7-list-input label="Manure" inline-label readonly :value="totalVolumeOfManure">
          <span slot="inner-end" class="text-color-gray4 margin-left">tonnes</span>
        </f7-list-input>
        <f7-list-input label="Nitrogen (N)" inline-label readonly :value="totalNitrogen">
          <span slot="inner-end" class="text-color-gray4 margin-left">kg</span>
        </f7-list-input>
        <f7-list-input label="Phosphorus (P)" inline-label readonly :value="totalPhosporus">
          <span slot="inner-end" class="text-color-gray4 margin-left">kg</span>
        </f7-list-input>
        <f7-list-input label="Potassium (K)" inline-label readonly :value="totalPotassium">
          <span slot="inner-end" class="text-color-gray4 margin-left">kg</span>
        </f7-list-input>
      </f7-list>

      <f7-block>
        <f7-button big fill :href="`/nmp/plan/${planId}/import-export-manure/`">Next</f7-button>
      </f7-block>
    </template>
  </f7-page>
</template>

<script>
import FastToolbar from "@/components/Toolbar.vue";
import ProducedManureBlock from "./ProducedManureBlock.vue";

import queryPlan from "./graphql/queryPlan.gql";

export default {
  name: "nmp-produced-manure-page",
  components: {
    FastToolbar,
    ProducedManureBlock
  },
  props: {
    planId: { type: String, required: true }
  },
  apollo: {
    plan: {
      query: queryPlan,
      variables() {
        return {
          planId: this.planId
        };
      },
      fetchPolicy: "cache-first",
      result({ data, loading, networkStatus }) {
        if (data && this.manures.length === 0) {
          this.manures = data.plan.producedLivestockManures;
          this.recomputeTotals();
        }
      }
    }
  },
  data() {
    return {
      plan: { loading: true },
      manures: [],
      totalVolumeOfManure: null,
      totalNitrogen: null,
      totalPhosporus: null,
      totalPotassium: null
    };
  },
  created() {
    this.$nextTick(() => {
      this.recomputeTotals();
    });
  },
  methods: {
    onPullToRefresh(e, done) {
      this.$apollo.queries.plan.refetch().then(done);
    },
    onChangeManureBlockValues(manure) {
      const idx = this.manures.findIndex(x => x.id === manure.id);
      this.$set(this.manures, idx, manure);
      this.recomputeTotals();
    },
    recomputeTotals() {
      if (this.manures) {
        this.totalVolumeOfManure = 0;
        this.totalNitrogen = 0;
        this.totalPhosporus = 0;
        this.totalPotassium = 0;
        this.manures.forEach(m => {
          let quantity =
            m.numberOfHeads * m.storageDays * m.litersPerHeadPerDay;
          this.totalVolumeOfManure += quantity;
          this.totalNitrogen += quantity * m.purity * m.nitrogenContent;
          this.totalPhosporus += quantity * m.purity * m.phosphorusContent;
          this.totalPotassium += quantity * m.purity * m.potassiumContent;
        });
        this.totalVolumeOfManure =
          Math.round(this.totalVolumeOfManure / 100) / 10;
        this.totalNitrogen = Math.round(this.totalNitrogen * 10) / 10;
        this.totalPhosporus = Math.round(this.totalPhosporus * 10) / 10;
        this.totalPotassium = Math.round(this.totalPotassium * 10) / 10;
      }
    }
  }
};
</script>
