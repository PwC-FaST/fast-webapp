import NMPPage from "@/components/nmp/NMPPage.vue";
import NewPlanPage from "@/components/nmp/NewPlanPage.vue";
import PlanPage from "@/components/nmp/PlanPage.vue";
import ProducedManurePage from "@/components/nmp/ProducedManurePage.vue";
import ImportedOrExportedManurePage from "@/components/nmp/ImportedOrExportedManurePage.vue";
import CropNeedsPage from "@/components/nmp/CropNeedsPage.vue";
import ManureApplicationPage from "@/components/nmp/ManureApplicationPage.vue";

import { redirectIfNotLoggedIn } from "./authentication";

export default [
  {
    path: "/nmp/",
    async: redirectIfNotLoggedIn({ component: NMPPage, keepAlive: true })
  },
  {
    path: "/nmp/new/",
    async: redirectIfNotLoggedIn({ component: NewPlanPage, keepAlive: true })
  },
  {
    path: "/nmp/plan/:planId/results/",
    async: redirectIfNotLoggedIn({ component: PlanPage, keepAlive: true })
  },
  {
    path: "/nmp/plan/:planId/produced-manure/",
    async: redirectIfNotLoggedIn({
      component: ProducedManurePage,
      keepAlive: true
    })
  },
  {
    path: "/nmp/plan/:planId/import-export-manure/",
    async: redirectIfNotLoggedIn({
      component: ImportedOrExportedManurePage,
      keepAlive: true
    })
  },
  {
    path: "/nmp/plan/:planId/crop-needs/",
    async: redirectIfNotLoggedIn({ component: CropNeedsPage, keepAlive: true })
  },
  {
    path: "/nmp/plan/:planId/manure-application/",
    async: redirectIfNotLoggedIn({
      component: ManureApplicationPage,
      keepAlive: true
    })
  }
];
