import NotFoundPage from "@/components/NotFoundPage.vue";

import loginRoutes from "./routes.login";
import homeRoutes from "./routes.home";
import messagingRoutes from "./routes.messaging";
import nmpRoutes from "./routes.nmp";
import farmRoutes from "./routes.farm";
import servicesRoutes from "./routes.services";

export default [
  ...loginRoutes,
  ...homeRoutes,
  ...farmRoutes,
  ...nmpRoutes,
  ...servicesRoutes,
  ...messagingRoutes,
  {
    path: "(.*)",
    component: NotFoundPage
  }
];
