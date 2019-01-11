<template>
  <f7-page ptr @ptr:refresh="onPullToRefresh">
    <f7-navbar title="My livestock" back-link></f7-navbar>
    <fast-toolbar></fast-toolbar>

    <f7-block-title>My livestock</f7-block-title>
    <f7-list>
      <f7-block-header>Swipe left to delete an item.</f7-block-header>
      <f7-list-item
        v-for="livestock in farm.farmLivestock"
        :key="livestock.id"
        class="livestock-item"
        swipeout
        @swipeout:delete="onDeleteLivestockListItem(livestock)"
        :title="livestock.livestockSpecies.rootLivestockSpecies.namePlural"
        :footer="livestock.livestockSpecies.namePlural"
      >
        <img
          :src="'/media/' + (livestock.livestockSpecies.icon || livestock.livestockSpecies.rootLivestockSpecies.icon)"
          slot="media"
          class="livestock-species-icon"
          style="height: 42px"
        >
        <h3
          class="no-margin-top no-margin-bottom margin-right"
          slot="before-title"
        >{{ livestock.numberOfHeads }}</h3>
        <f7-stepper
          :buttons-only="true"
          small
          raised
          slot="after"
          :value="livestock.numberOfHeads"
          @stepper:change="value => setNumberOfHeads(livestock, value)"
        ></f7-stepper>
        <f7-swipeout-actions right>
          <f7-swipeout-button delete>Delete</f7-swipeout-button>
        </f7-swipeout-actions>
      </f7-list-item>
    </f7-list>

    <f7-block-title>Add more livestock</f7-block-title>
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
        label="# of heads"
        inline-label
        clear-button
        placeholder="Enter number of heads"
        :value="addNumberOfHeads"
        @input="addNumberOfHeads = $event.target.value"
      ></f7-list-input>
      <f7-list-button @click="onClickAddLivestock">Add to my farm</f7-list-button>
    </f7-list>
  </f7-page>
</template>

<script>
import FastToolbar from "@/components/Toolbar.vue";
import SVGImage from "@/components/SVGImage";

import queryFarm from "./graphql/queryFarm.gql";
import queryLivestockSpecies from "./graphql/queryLivestockSpecies.gql";
import queryFarmOnlyLivestock from "./graphql/queryFarmOnlyLivestock.gql";
import mutationUpdateFarmLivestock from "./graphql/mutationUpdateFarmLivestock.gql";
import mutationRemoveFarmLivestock from "./graphql/mutationRemoveFarmLivestock.gql";

export default {
  name: "farm-livestock-page",
  components: {
    FastToolbar,
    "svg-image": SVGImage
  },
  apollo: {
    farm: {
      query: queryFarm,
      fetchPolicy: "cache-first"
    },
    livestockSpecies: {
      query: queryLivestockSpecies,
      fetchPolicy: "cache-first"
    },
    farmOnlyLivestock: {
      query: queryFarmOnlyLivestock,
      fetchPolicy: "cache-first",
      update(data) {
        return data.farm;
      }
    }
  },
  data() {
    return {
      farm: { loading: true },
      livestockSpecies: { loading: true },
      farmOnlyLivestock: { loading: true },
      addNumberOfHeads: null,
      addLivestockSpeciesId: null
    };
  },
  computed: {},
  methods: {
    onDeleteLivestockListItem(livestock) {
      this.$f7.progressbar.show();
      this.$apollo
        .mutate({
          mutation: mutationRemoveFarmLivestock,
          variables: {
            farmId: this.farm.id,
            livestockSpeciesId: livestock.livestockSpecies.id
          }
        })
        .then(() => {
          return this.$apollo.queries.farmOnlyLivestock.refetch({
            fetchPolicy: "network-only"
          });
        })
        .then(() => {
          this.$f7.progressbar.hide();
        })
        .catch(() => {
          this.$f7.progressbar.hide();
        });
    },
    setNumberOfHeads(livestock, value) {
      // Prevent the progressbar getting stuck
      if (!document.querySelector(".progressbar-infinite")) {
        this.$f7.progressbar.show();
      }
      this.$apollo
        .mutate({
          mutation: mutationUpdateFarmLivestock,
          variables: {
            farmId: this.farm.id,
            livestockSpeciesId: livestock.livestockSpecies.id,
            numberOfHeads: value
          }
        })
        .then(() => {
          this.$f7.progressbar.hide();
        })
        .catch(() => {
          this.$f7.progressbar.hide();
        });
    },
    onClickAddLivestock(e) {
      if (this.addLivestockSpeciesId && this.addNumberOfHeads > 0) {
        this.$f7.progressbar.show();
        this.$apollo
          .mutate({
            mutation: mutationUpdateFarmLivestock,
            variables: {
              farmId: this.farm.id,
              livestockSpeciesId: this.addLivestockSpeciesId,
              numberOfHeads: this.addNumberOfHeads
            }
          })
          .then(({ data }) => {
            if (data.updateFarmLivestock.created) {
              return this.$apollo.queries.farmOnlyLivestock.refetch({
                fetchPolicy: "network-only"
              });
            } else {
              return Promise.resolve();
            }
          })
          .then(() => {
            this.$f7.progressbar.hide();
          })
          .catch(() => {
            this.$f7.progressbar.hide();
          });
      }
    },
    onPullToRefresh(e, done) {
      Promise.all([
        this.$apollo.queries.farm.refetch({ fetchPolicy: "network-only" }),
        this.$apollo.queries.livestockSpecies.refetch({
          fetchPolicy: "network-only"
        })
      ]).then(done);
    }
  }
};
</script>

<style scoped>
</style>

<style>
.livestock-species-icon svg path {
  fill: black;
  fill-opacity: 0.7;
}

.livestock-item .item-inner {
  justify-content: left !important;
}

.livestock-species-option .item-media img {
  height: 44px;
}

.select-add-livestock-species .item-inner {
  justify-content: flex-start !important;
}

.select-add-livestock-species .item-after {
  margin-left: 10px !important;
}
</style>
