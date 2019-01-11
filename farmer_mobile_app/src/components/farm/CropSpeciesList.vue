<template>
  <f7-list>
    <f7-list-item
      v-for="species in cropSpecies"
      :key="species.id"
      :title="species.nameSingular"
      :footer="species.nameLatin"
      after="Select"
      @click="onClickListItem(species)"
    ></f7-list-item>
  </f7-list>
</template>

<script>
import queryCropSpecies from "./graphql/queryCropSpecies.gql";

export default {
  name: "farm-crop-species-list",
  apollo: {
    cropSpecies: {
      query: queryCropSpecies,
      fetchPolicy: "cache-and-network"
    }
  },
  data() {
    return {
      cropSpecies: { loading: true }
    };
  },
  methods: {
    onClickListItem(species) {
      this.$emit("crop-species-select", species);
    }
  }
};
</script>

<style scoped>
</style>
