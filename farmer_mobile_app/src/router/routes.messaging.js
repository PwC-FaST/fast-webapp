import InboxPage from "@/components/messaging/InboxPage.vue";
import ThreadPage from "@/components/messaging/ThreadPage.vue";
import ContactsPage from "@/components/messaging/ContactsPage.vue";
import ContactPage from "@/components/messaging/ContactPage.vue";
import AddContactPage from "@/components/messaging/AddContactPage.vue";
import { redirectIfNotLoggedIn } from "./authentication";

export default [
  {
    path: "/messaging/",
    async: redirectIfNotLoggedIn({ component: InboxPage, keepAlive: true })
  },
  {
    path: "/messaging/thread/:threadId/",
    async: redirectIfNotLoggedIn({ component: ThreadPage })
  },
  {
    path: "/messaging/contacts/",
    async: redirectIfNotLoggedIn({ component: ContactsPage, keepAlive: true })
  },
  {
    path: "/messaging/contact/:contactId/",
    async: redirectIfNotLoggedIn({ component: ContactPage })
  },
  {
    path: "/messaging/contacts/add/",
    async: redirectIfNotLoggedIn({ component: AddContactPage })
  }
];
