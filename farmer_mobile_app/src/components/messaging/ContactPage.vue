<template>
  <f7-page>
    <f7-navbar :title="contact.loading ? 'Loading...' : contact.user.fullName" back-link></f7-navbar>
    <fast-toolbar></fast-toolbar>

    <f7-block strong v-if="!contact.loading && !contact.error">
      <p>Username:
        <b>{{ contact.user.username }}</b>
      </p>
      <f7-button
        v-if="contact.isInMyContacts"
        big
        color="red"
        @click="onClickRemoveContact"
      >Remove from my contacts</f7-button>
      <f7-button v-else big @click="onClickAddContact">Add to my contacts</f7-button>
    </f7-block>
  </f7-page>
</template>

<script>
import FastToolbar from "@/components/Toolbar";

import queryContact from "./graphql/queryContact.gql";
import mutationRemoveContact from "./graphql/mutationRemoveContact.gql";
import mutationAddContact from "./graphql/mutationAddContact.gql";

export default {
  name: "messaging-contact-page",
  components: {
    FastToolbar
  },
  props: {
    contactId: { type: String, required: true }
  },
  apollo: {
    contact: {
      query: queryContact,
      variables() {
        return {
          contactId: this.contactId
        };
      }
    }
  },
  data() {
    return {
      contact: { loading: true }
    };
  },
  computed: {},
  methods: {
    onClickRemoveContact() {
      this.$f7.progressbar.show();
      this.$apollo
        .mutate({
          mutation: mutationRemoveContact,
          variables: {
            contactId: this.contactId
          }
        })
        .then(() => {
          this.$f7.progressbar.hide();
          this.$f7router.navigate("/messaging/contacts/");
        })
        .catch(() => {
          this.$f7.progressbar.hide();
        });
    },
    onClickAddContact() {
      this.$f7.progressbar.show();
      this.$apollo
        .mutate({
          mutation: mutationAddContact,
          variables: {
            contactId: this.contactId
          }
        })
        .then(() => {
          this.$f7.progressbar.hide();
          this.$f7router.navigate("/messaging/contacts/");
        })
        .catch(() => {
          this.$f7.progressbar.hide();
        });
    }
  }
};
</script>
