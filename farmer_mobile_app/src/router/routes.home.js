import HomePage from "@/components/home/HomePage.vue";
import { redirectIfNotLoggedIn } from "./authentication";

export default [
  {
    path: "/",
    async: redirectIfNotLoggedIn({ component: HomePage })
  }
];
