<template>
  <f7-page ptr @ptr:refresh="onPullToRefresh" @page:afterin="scrollToBottom">
    <f7-navbar :title="title" back-link>
      <f7-nav-right>
        <f7-link icon-only icon-f7="person" href="#" class="disabled"></f7-link>
      </f7-nav-right>
    </f7-navbar>

    <f7-messagebar
      :placeholder="placeholder"
      ref="message_bar"
      :attachments-visible="attachmentsVisible"
      :value="newMessage"
      v-on:input="newMessage = $event.target.value"
      :sheet-visible="sheetVisible"
      @send="sendMessage"
    >
      <f7-icon
        ios="f7:arrow_up_fill"
        md="material:send"
        slot="send-link"
        :class="{'disabled': !newMessage}"
      ></f7-icon>
      <f7-messagebar-attachments>
        <f7-messagebar-attachment
          v-for="(image, index) in attachments"
          :key="index"
          :image="image"
          @attachment:delete="deleteAttachment(image)"
        ></f7-messagebar-attachment>
      </f7-messagebar-attachments>
    </f7-messagebar>

    <f7-list media-list ref="messages" class="no-margin-top no-margin-bottom">
      <f7-list-item
        v-for="message in sortedMessages"
        :key="message.id"
        :ref="'message_' + message.id"
        :class="{'message-from-me': message.createdBy.username === 'fast'}"
        :title="message.createdBy.fullName || message.createdBy.username"
        :after="$shortDateTime(message.createdAt)"
        :text="message.content"
      ></f7-list-item>
    </f7-list>
  </f7-page>
</template>

<script>
import queryThread from "./graphql/queryThread.gql";
import mutationCreateMessage from "./graphql/mutationCreateMessage.gql";

export default {
  name: "messaging-thread-page",
  props: {
    threadId: String
  },
  apollo: {
    thread: {
      query: queryThread,
      variables() {
        return {
          threadId: this.threadId
        };
      },
      pollInterval: 60000
    }
  },
  data() {
    return {
      thread: { loading: true },
      newMessage: null,
      sheetVisible: false,
      attachments: []
    };
  },
  activated() {
    this.scrollToBottom();
  },
  computed: {
    title() {
      return this.thread.loading ? "Loading..." : this.thread.subject;
    },
    sortedMessages() {
      if (this.thread.messages instanceof Array) {
        return this.thread.messages
          .slice()
          .sort(x => x.createdAt)
          .reverse();
      } else {
        return [];
      }
    },
    attachmentsVisible() {
      return this.attachments.length > 0;
    },
    placeholder() {
      return this.attachments.length > 0 ? "Add comment or Send" : "Message";
    }
  },
  methods: {
    sendMessage(value, clear) {
      if (!this.newMessage) return;
      const content = this.newMessage.trim();
      this.newMessage = null;
      this.attachments = [];
      this.sheetVisible = false;

      if (content.length) {
        this.$f7.progressbar.show();
        this.$apollo
          .mutate({
            mutation: mutationCreateMessage,
            variables: {
              threadId: this.threadId,
              content: content
            }
          })
          .then(data => {
            this.scrollToBottom();
            return this.$apollo.queries.thread.refetch({
              threadId: this.threadId
            });
          })
          .then(() => {
            this.$f7.progressbar.hide();
            this.scrollToBottom();
          })
          .catch(() => {
            this.$f7.progressbar.hide();
          });
      }
    },
    deleteAttachment() {},
    handleAttachment() {},
    scrollToBottom() {
      let listElement = this.$el.getElementsByClassName("page-content")[0];
      listElement.scrollTop = listElement.scrollHeight;
    },
    onPullToRefresh(e, done) {
      this.$apollo.queries.thread.refetch().then(done);
    }
  }
};
</script>

<style scoped>
.message-from-me {
  background-color: #eeeeee;
}
</style>
