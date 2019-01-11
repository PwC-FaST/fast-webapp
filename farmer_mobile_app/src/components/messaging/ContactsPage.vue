<template>
  <f7-page>
    <f7-navbar title="My contacts" back-link>
      <f7-nav-right>
        <f7-link icon-f7="add" href="/messaging/contacts/add/"></f7-link>
      </f7-nav-right>
    </f7-navbar>
    <fast-toolbar></fast-toolbar>

    <f7-list contacts-list>
      <f7-list-group v-for="(group, key) in contactGroups" :key="key">
        <f7-list-item :title="key" :key="key" group-title></f7-list-item>
        <f7-list-item
          v-for="contact in group"
          :key="contact.user.username"
          :link="`/messaging/contact/${contact.id}/`"
          :title="`${contact.user.firstName} ${contact.user.lastName}`"
        ></f7-list-item>
      </f7-list-group>
    </f7-list>

    <f7-block>
      <f7-button big href="/messaging/contacts/add/">Add another contact</f7-button>
    </f7-block>
  </f7-page>
</template>

<script>
import FastToolbar from "@/components/Toolbar";
import queryMyContacts from "./graphql/queryMyContacts.gql";

export default {
  name: "messaging-contacts-page",
  components: {
    FastToolbar
  },
  apollo: {
    myContacts: {
      query: queryMyContacts,
      variables: {},
      fetchPolicy: "cache-and-network"
    }
  },
  data() {
    return {
      myContacts: { loading: true }
    };
  },
  computed: {
    contactGroups() {
      if (!this.myContacts.loading && !this.myContacts.error) {
        let groups = {};
        this.myContacts.forEach(c => {
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
