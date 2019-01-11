<template>
  <f7-page ptr @ptr:refresh="onPullToRefresh">
    <fast-navbar title="Inbox">
      <template slot="nav-right">
        <f7-link icon-only icon-f7="add" href="#" class="disabled"></f7-link>
        <f7-link icon-only icon-f7="person" href="/messaging/contacts/"></f7-link>
      </template>
    </fast-navbar>
    <fast-toolbar></fast-toolbar>

    <div v-if="threads.loading">Loading...</div>
    <div v-else-if="threads.error">An error occurred</div>

    <template v-else>
  <f7-list media-list class="no-margin-top no-margin-bottom">
    <f7-list-item
      v-for="(thread, index) in sortedThreads"
      :key="index"
      :link="`/messaging/thread/${thread.id}/`"
      :title="thread.createdBy.fullName || thread.createdBy.username"
      :after="$shortDateTime(thread.createdAt)"
      :subtitle="thread.subject"
      :text="thread.messages[0].content"
    ></f7-list-item>
  </f7-list>
</template>

  </f7-page>
</template>

<script>
import FastToolbar from "@/components/Toolbar";
import FastNavbar from "@/components/Navbar.vue";

import queryThreads from "./graphql/queryThreads.gql";

export default {
  name: "messaging-inbox-page",
  components: {
    FastToolbar,
    FastNavbar
  },
  apollo: {
    threads: {
      query: queryThreads,
      fetchPolicy: "cache-first"
    }
  },
  data() {
    return {
      threads: { loading: true }
    };
  },
  computed: {
    sortedThreads() {
      if (this.threads instanceof Array) {
        return this.threads.slice().sort(x => x.createdAt);
      } else {
        return [];
      }
    }
  },
  methods: {
    onPullToRefresh(e, done) {
      this.$apollo.queries.threads.refetch().then(done);
    }
  }
};
</script>
