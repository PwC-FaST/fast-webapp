<template>
  <f7-page ptr @ptr:refresh="onPullToRefresh">
    <f7-navbar title="Manure imports/exports" back-link>
      <f7-nav-right>
        <f7-link :href="`/nmp/plan/${planId}/crop-needs/`">Next</f7-link>
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
        <p>If you are importing manure to your farm, or exporting manure to other farmers, fill in the inputs below.</p>
        <p>If you are not importing or exporting, you can leave these blank and proceed to next step.</p>
      </f7-block>

      <f7-block-title>Imports</f7-block-title>
      <f7-list v-if="importedLivestockManures && importedLivestockManures.length > 0">
        <f7-list-input
          v-for="manure in importedLivestockManures"
          :id="manure.id"
          :key="manure.id"
          :label="manure.livestockSpecies.nameSingular"
          :default-value="manure.totalQuantity / 1000"
          info="tonnes"
          @change="onChangeImportedOrExportedLivestockManureQuantity(manure, Number($event.target.value) * 1000)"
        >
          <img
            slot="media"
            :src="'/media/' + (manure.livestockSpecies.icon || manure.livestockSpecies.rootLivestockSpecies.icon)"
            style="height: 42px"
          >
          <f7-link
            slot="content-end"
            icon-only
            class="margin-right"
            icon-f7="delete_round_fill"
            :icon-size="18"
            @click="onDeleteImportedOrExportedLivestockManureListItem(manure)"
          ></f7-link>
        </f7-list-input>
      </f7-list>
      <f7-list v-else>
        <f7-list-item-row>
          <p class="margin-left margin-right">No manure imports yet.</p>
        </f7-list-item-row>
      </f7-list>

      <f7-block-title>Exports</f7-block-title>
      <f7-list v-if="exportedLivestockManures && exportedLivestockManures.length > 0">
        <f7-list-input
          v-for="manure in exportedLivestockManures"
          :id="manure.id"
          :key="manure.id"
          :label="manure.livestockSpecies.nameSingular"
          :default-value="-manure.totalQuantity / 1000"
          info="tonnes"
          @change="onChangeImportedOrExportedLivestockManureQuantity(manure, -Number($event.target.value) * 1000)"
        >
          <img
            slot="media"
            :src="'/media/' + (manure.livestockSpecies.icon || manure.livestockSpecies.rootLivestockSpecies.icon)"
            style="height: 42px"
          >
          <f7-link
            slot="content-end"
            icon-only
            class="margin-right"
            icon-f7="delete_round_fill"
            :icon-size="18"
            @click="onDeleteImportedOrExportedLivestockManureListItem(manure)"
          ></f7-link>
        </f7-list-input>
      </f7-list>
      <f7-list v-else>
        <f7-list-item-row>
          <p class="margin-left margin-right">No manure exports yet.</p>
        </f7-list-item-row>
      </f7-list>

      <f7-block-title>Add manure import or export</f7-block-title>
      <f7-list>
        <f7-list-item
          title="Species"
          placeholder="Select a species"
          ref="select_add_livestock_species"
          class="select-add-livestock-species"
          smart-select
          :smart-select-params="{
                        openIn: 'popup',
                        closeOnSelect: true,
                        searchbar: true,
                        searchbarPlaceholder: 'Search species'
                      }"
        >
          <select
            name="species"
            v-if="livestockSpecies instanceof Array"
            v-model="addLivestockSpeciesId"
          >
            <optgroup
              v-for="rootSpecies in livestockSpecies"
              :key="'select_' + rootSpecies.id"
              :label="rootSpecies.namePlural"
            >
              <option
                v-for="species in rootSpecies.children"
                :key="'select_' + species.id"
                :value="species.id"
                :data-option-image="'/media/' + (species.icon || rootSpecies.icon)"
                data-option-class="livestock-species-option"
              >{{ species.namePlural }}</option>
            </optgroup>
          </select>
        </f7-list-item>
        <f7-list-input
          label="Quantity"
          inline-label
          placeholder="Enter manure volume"
          :value="addTotalQuantity"
          @input="addTotalQuantity = $event.target.value"
        >
          <span slot="inner-end" class="text-color-gray4 margin-left">tonnes</span>
        </f7-list-input>
        <f7-list-item-row class="padding-bottom padding-top">
          <f7-row class="width-100">
            <f7-col class="text-align-center">
              <f7-link @click="onClickAddImport">Add import</f7-link>
            </f7-col>
            <f7-col class="text-align-center">
              <f7-link @click="onClickAddExport">Add export</f7-link>
            </f7-col>
          </f7-row>
        </f7-list-item-row>
      </f7-list>

      <f7-block-title>Totals (imports - exports)</f7-block-title>
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
        <f7-button big fill :href="`/nmp/plan/${planId}/crop-needs/`">Next</f7-button>
      </f7-block>
    </template>
  </f7-page>
</template>

<script>
import FastToolbar from "@/components/Toolbar";

import queryPlan from "./graphql/queryPlan.gql";
import queryLivestockSpecies from "@/components/farm/graphql/queryLivestockSpecies.gql";
import mutationCreateImportedOrExportedLivestockManure from "./graphql/mutationCreateImportedOrExportedLivestockManure.gql";
import mutationDeleteImportedOrExportedLivestockManure from "./graphql/mutationDeleteImportedOrExportedLivestockManure.gql";
import mutationUpdateImportedOrExportedLivestockManure from "./graphql/mutationUpdateImportedOrExportedLivestockManure.gql";

export default {
  name: "nmp-imported-or-exported-manure-page",
  components: {
    FastToolbar
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
          this.manures = data.plan.importedOrExportedLivestockManures;
          this.recomputeTotals();
        }
      }
    },
    livestockSpecies: {
      query: queryLivestockSpecies,
      fetchPolicy: "cache-first"
    }
  },
  data() {
    return {
      plan: { loading: true },
      livestockSpecies: { loading: true },
      manures: [],
      totalVolumeOfManure: null,
      totalNitrogen: null,
      totalPhosporus: null,
      totalPotassium: null,
      addLivestockSpeciesId: null,
      addTotalQuantity: null
    };
  },
  created() {
    this.$nextTick(() => {
      this.recomputeTotals();
    });
  },
  computed: {
    importedLivestockManures() {
      if (this.plan && this.plan.importedOrExportedLivestockManures.length) {
        return this.plan.importedOrExportedLivestockManures.filter(
          m => m.totalQuantity >= 0
        );
      } else {
        return null;
      }
    },
    exportedLivestockManures() {
      if (this.plan && this.plan.importedOrExportedLivestockManures.length) {
        return this.plan.importedOrExportedLivestockManures.filter(
          m => m.totalQuantity < 0
        );
      } else {
        return null;
      }
    }
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
    onClickAddImport() {
      if (this.addLivestockSpeciesId && this.addTotalQuantity) {
        this.$f7.progressbar.show();
        this.$apollo
          .mutate({
            mutation: mutationCreateImportedOrExportedLivestockManure,
            variables: {
              planId: this.plan.id,
              livestockSpeciesId: this.addLivestockSpeciesId,
              totalQuantity: Number(this.addTotalQuantity) * 1000
            }
          })
          .then(() => {
            return this.$apollo.queries.plan.refetch();
          })
          .then(() => {
            this.recomputeTotals();
            this.addLivestockSpeciesId = null;
            this.addTotalQuantity = null;
            this.$f7.progressbar.hide();
          })
          .catch(() => {
            this.$f7.progressbar.hide();
          });
      }
    },
    onClickAddExport() {
      if (this.addLivestockSpeciesId && this.addTotalQuantity) {
        this.$f7.progressbar.show();
        this.$apollo
          .mutate({
            mutation: mutationCreateImportedOrExportedLivestockManure,
            variables: {
              planId: this.plan.id,
              livestockSpeciesId: this.addLivestockSpeciesId,
              totalQuantity: -Number(this.addTotalQuantity) * 1000
            }
          })
          .then(() => {
            return this.$apollo.queries.plan.refetch();
          })
          .then(() => {
            this.recomputeTotals();
            this.addLivestockSpeciesId = null;
            this.addTotalQuantity = null;
            this.$f7.progressbar.hide();
          })
          .catch(() => {
            this.$f7.progressbar.hide();
          });
      }
    },
    onDeleteImportedOrExportedLivestockManureListItem(manure) {
      this.$f7.dialog.confirm(
        `Please confirm you wish to remove this import/export from this plan`,
        "Remove this import/export?",
        () => {
          this.$f7.progressbar.show();
          this.$apollo
            .mutate({
              mutation: mutationDeleteImportedOrExportedLivestockManure,
              variables: {
                importedOrExportedLivestockManureId: manure.id
              }
            })
            .then(() => {
              return this.$apollo.queries.plan.refetch();
            })
            .then(() => {
              this.recomputeTotals();
              this.$f7.progressbar.hide();
            })
            .catch(() => {
              this.$f7.progressbar.hide();
            });
        }
      );
    },
    onChangeImportedOrExportedLivestockManureQuantity(manure, quantity) {
      if (quantity) {
        this.$f7.progressbar.show();
        this.$apollo
          .mutate({
            mutation: mutationUpdateImportedOrExportedLivestockManure,
            variables: {
              importedOrExportedLivestockManureId: manure.id,
              totalQuantity: quantity
            }
          })
          .then(() => {
            this.$f7.progressbar.hide();
            this.recomputeTotals();
          })
          .catch(() => {
            this.$f7.progressbar.hide();
          });
      }
    },
    recomputeTotals() {
      if (this.manures) {
        this.totalVolumeOfManure = 0;
        this.totalNitrogen = 0;
        this.totalPhosporus = 0;
        this.totalPotassium = 0;
        this.manures.forEach(m => {
          this.totalVolumeOfManure += m.totalQuantity;
          this.totalNitrogen += m.totalQuantity * m.purity * m.nitrogenContent;
          this.totalPhosporus +=
            m.totalQuantity * m.purity * m.phosphorusContent;
          this.totalPotassium +=
            m.totalQuantity * m.purity * m.potassiumContent;
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
