<template>
  <f7-page>
    <f7-navbar title="Add a contact" back-link></f7-navbar>
    <fast-toolbar></fast-toolbar>

    <f7-list contacts-list>
      <f7-list-group v-for="(group, key) in contactGroups" :key="key">
        <f7-list-item :title="key" :key="key" group-title></f7-list-item>
        <f7-list-item
          v-for="contact in group"
          :key="contact.user.username"
          :link="`/messaging/contact/${contact.id}/`"
          :title="`${contact.user.fullName}`"
        ></f7-list-item>
      </f7-list-group>
    </f7-list>
  </f7-page>
</template>

<script>
import FastToolbar from "@/components/Toolbar";
import queryContacts from "./graphql/queryContacts.gql";

export default {
  name: "messaging-add-contact-page",
  components: {
    FastToolbar
  },
  apollo: {
    contacts: {
      query: queryContacts,
      variables: {},
      fetchPolicy: "cache-and-network"
    }
  },
  data() {
    return {
      contacts: { loading: true }
    };
  },
  computed: {
    contactGroups() {
      if (!this.contacts.loading && !this.contacts.error) {
        let groups = {};
        this.contacts
          .filter(c => !c.isInMyContacts)
          .forEach(c => {
            let key = c.user.username.charAt(0).toUpperCase();
            if (!groups[key]) {
              groups[key] = [];
            }
            groups[key].push(c);
          });
        return groups;
      } else {
        return {};
      }
    }
  }
};
</script>
