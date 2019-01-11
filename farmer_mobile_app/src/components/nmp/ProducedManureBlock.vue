<template>
  <div>
    <f7-list v-if="Object.keys(manure).length > 0" :class="{'no-margin-bottom': detailsVisible}">
      <f7-list-item :title="manure.livestockSpecies.namePlural">
        <img
          slot="media"
          :src="'/media/' + (manure.livestockSpecies.icon || manure.livestockSpecies.rootLivestockSpecies.icon)"
          style="height: 42px"
        >
      </f7-list-item>
      <f7-list-input
        label="Head count"
        :value="manure.numberOfHeads"
        @input="updateData(Number($event.target.value), 'numberOfHeads')"
        @change="saveData(Number($event.target.value), 'numberOfHeads')"
        inline-label
        clear-button
      ></f7-list-input>
      <f7-list-input
        label="Storage"
        :value="manure.storageDays"
        @input="updateData(Number($event.target.value), 'storageDays')"
        @change="saveData(Number($event.target.value), 'storageDays')"
        inline-label
        clear-button
      ></f7-list-input>
      <f7-list-input
        label="Manure/head"
        :value="manure.litersPerHeadPerDay"
        @input="updateData(Number($event.target.value), 'litersPerHeadPerDay')"
        @change="saveData(Number($event.target.value), 'litersPerHeadPerDay')"
        inline-label
        clear-button
      ></f7-list-input>
      <f7-list-input
        label="Purity"
        :value="manure.purity"
        @input="updateData(Number($event.target.value), 'purity')"
        @change="saveData(Number($event.target.value), 'purity')"
        inline-label
        clear-button
      ></f7-list-input>

      <f7-list-item-row class="padding" @click.native="detailsVisible = !detailsVisible">
        <f7-row class="width-100">
          <f7-col width="50" class="text-align-left">
            <f7-icon f7="chevron_down"></f7-icon>Total
          </f7-col>
          <f7-col width="50" class="text-align-right">{{ totalQuantity }}&nbsp;tonnes</f7-col>
        </f7-row>
      </f7-list-item-row>
    </f7-list>

    <f7-list v-if="detailsVisible" class="no-margin-top no-hairlines">
      <f7-list-input
        label="N"
        :value="manure.nitrogenContent"
        @input="updateData(Number($event.target.value), 'nitrogenContent')"
        @change="saveData(Number($event.target.value), 'nitrogenContent')"
        inline-label
        clear-button
        class="bg-color-gray6"
      >
        <span slot="inner-end" class="margin-left">{{ nitrogenTotalQuantity }}&nbsp;tonnes</span>
      </f7-list-input>
      <f7-list-input
        label="P"
        :value="manure.phosphorusContent"
        @input="updateData(Number($event.target.value), 'phosphorusContent')"
        @change="saveData(Number($event.target.value), 'phosphorusContent')"
        inline-label
        clear-button
        class="bg-color-gray6"
      >
        <span slot="inner-end" class="margin-left">{{ phosphorusTotalQuantity }}&nbsp;tonnes</span>
      </f7-list-input>
      <f7-list-input
        label="K"
        :value="manure.potassiumContent"
        @input="updateData(Number($event.target.value), 'potassiumContent')"
        @change="saveData(Number($event.target.value), 'potassiumContent')"
        inline-label
        clear-button
        class="bg-color-gray6"
      >
        <span slot="inner-end" class="margin-left">{{ potassiumTotalQuantity }}&nbsp;tonnes</span>
      </f7-list-input>
    </f7-list>
  </div>
</template>

<script>
import mutationUpdateProducedLivestockManure from "./graphql/mutationUpdateProducedLivestockManure.gql";

export default {
  name: "nmp-produced-manure-block",
  props: {
    manureInit: Object
  },
  data() {
    return {
      manure: {},
      detailsVisible: false
    };
  },
  mounted() {
    this.manure = this.manureInit;
  },
  computed: {
    totalQuantity() {
      return (
        Math.round(
          (this.manure.numberOfHeads *
            this.manure.storageDays *
            this.manure.litersPerHeadPerDay) /
            100
        ) / 10
      );
    },
    nitrogenTotalQuantity() {
      return (
        Math.round(
          this.totalQuantity *
            this.manure.purity *
            this.manure.nitrogenContent *
            10
        ) / 10
      );
    },
    phosphorusTotalQuantity() {
      return (
        Math.round(
          this.totalQuantity *
            this.manure.purity *
            this.manure.phosphorusContent *
            10
        ) / 10
      );
    },
    potassiumTotalQuantity() {
      return (
        Math.round(
          this.totalQuantity *
            this.manure.purity *
            this.manure.potassiumContent *
            10
        ) / 10
      );
    }
  },
  methods: {
    updateData(value, field) {
      this.manure[field] = value;
      this.$emit("change", this.manure);
    },
    saveData(value, field) {
      this.$f7.progressbar.show();
      let variables = {};
      variables[field] = value;
      variables.producedLivestockManureId = this.manure.id;
      this.$apollo
        .mutate({
          mutation: mutationUpdateProducedLivestockManure,
          variables
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

<style scoped>
</style>
