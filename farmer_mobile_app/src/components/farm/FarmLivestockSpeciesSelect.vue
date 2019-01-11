<template>
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
    <select name="species" v-if="livestockSpecies instanceof Array" v-model="livestockSpeciesId">
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
</template>

<script>
import queryLivestockSpecies from "./graphql/queryLivestockSpecies.gql";

export default {
  name: "farm-livestock-species-select",
  apollo: {
    livestockSpecies: {
      query: queryLivestockSpecies,
      fetchPolicy: "cache-first"
    }
  },
  data() {
    return {
      livestockSpecies: { loading: true },
      livestockSpeciesId: null
    };
  },
  methods: {
    onClose() {
      this.$emit("selected", this.livestockSpeciesId);
    }
  }
};
</script>

<style scoped>
</style>

<style>
.select-add-livestock-species .item-inner {
  justify-content: flex-start !important;
}

.select-add-livestock-species .item-after {
  margin-left: 10px !important;
}
</style>
