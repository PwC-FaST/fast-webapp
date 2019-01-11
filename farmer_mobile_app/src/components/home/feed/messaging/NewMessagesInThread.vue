<template>
  <f7-block strong class="no-margin-top" style="margin-bottom: 10px !important">
    <f7-block-header>
      <f7-row>
        <f7-col>Messaging</f7-col>
        <f7-col class="text-align-right">
          <small>{{ $shortDate(feedItem.timestamp) }}</small>
        </f7-col>
      </f7-row>
    </f7-block-header>

    <p class="no-margin-top">
      You have
      <b>{{ numberOfNewMessages }} message{{ feedItem.numberOfNewMessages > 1 ? 's' : '' }}</b>
      from
      <b>{{ fromLastUser }}</b>
      {{ hasMoreUsers }}
      in your conversation
      <f7-link :href="`/messaging/thread/${feedItem.thread.id}/`">{{ feedItem.thread.subject }}</f7-link>.
    </p>
    <f7-row>
      <f7-col class="text-align-left">
        <f7-link href="/messaging/">Go to my inbox</f7-link>
      </f7-col>
      <f7-col class="text-align-right">
        <f7-link :href="`/messaging/thread/${feedItem.thread.id}/`">Read</f7-link>
      </f7-col>
    </f7-row>
  </f7-block>
</template>

<script>
export default {
  // do not write 'messages' in the name as otherwise F7 picks it up and adds extra classes on the main page
  name: "messaging-new-in-thread-feed-block",
  props: {
    feedItem: Object
  },
  computed: {
    numberOfNewMessages() {
      return this.feedItem.numberOfNewMessages === 1
        ? "a"
        : this.feedItem.numberOfNewMessages;
    },
    users() {
      let users = this.feedItem.thread.messages.slice(
        0,
        this.feedItem.numberOfNewMessages
      );
      users = users.map(x => x.createdBy.fullName);
      return users.filter((item, pos) => users.indexOf(item) === pos); // deduplication
    },
    fromLastUser() {
      return this.users.length > 0 ? this.users[0] : "";
    },
    hasMoreUsers() {
      return this.users.length > 1 ? `and ${this.users.length - 1} more` : "";
    }
  }
};
</script>
