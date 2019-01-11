import ServicesPage from "@/components/services/ServicesPage.vue";
import ServicePage from "@/components/services/ServicePage.vue";
import { redirectIfNotLoggedIn } from "./authentication";

export default [
  {
    path: "/services/",
    async: redirectIfNotLoggedIn({ component: ServicesPage, keepAlive: true })
  },
  {
    path: "/services/service/:_id/",
    async: redirectIfNotLoggedIn({ component: ServicePage })
  }
];
