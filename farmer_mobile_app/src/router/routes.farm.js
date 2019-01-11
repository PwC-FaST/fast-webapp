import { redirectIfNotLoggedIn } from "./authentication";

import FarmPage from "@/components/farm/FarmPage.vue";
import FarmParcelPage from "@/components/farm/FarmParcelPage.vue";
import FarmParcelSoilPage from "@/components/farm/FarmParcelSoilPage.vue";
import FarmParcelHydroPage from "@/components/farm/FarmParcelHydroPage.vue";
import FarmParcelNatura2000Page from "@/components/farm/FarmParcelNatura2000Page.vue";
import AddFarmParcelPage from "@/components/farm/AddFarmParcelPage.vue";
import SelectFarmParcelFromMapPage from "@/components/farm/SelectFarmParcelFromMapPage.vue";
import ConfirmAddFarmParcelPage from "@/components/farm/ConfirmAddFarmParcelPage.vue";
import FarmLivestockPage from "@/components/farm/FarmLivestockPage.vue";

export default [
  {
    path: "/farm/",
    async: redirectIfNotLoggedIn({ component: FarmPage, keepAlive: true })
  },
  {
    path: "/farm/parcel/add/",
    async: redirectIfNotLoggedIn({ component: AddFarmParcelPage })
  },
  {
    path: "/farm/parcel/add/confirm/",
    async: redirectIfNotLoggedIn({ component: ConfirmAddFarmParcelPage })
  },
  {
    path: "/farm/parcel/add/select-from-map/",
    async: redirectIfNotLoggedIn({ component: SelectFarmParcelFromMapPage })
  },
  {
    path: "/farm/parcel/:farmParcelId/",
    async: redirectIfNotLoggedIn({ component: FarmParcelPage })
  },
  {
    path: "/farm/parcel/:farmParcelId/soil/",
    async: redirectIfNotLoggedIn({ component: FarmParcelSoilPage })
  },
  {
    path: "/farm/parcel/:farmParcelId/hydro/",
    async: redirectIfNotLoggedIn({ component: FarmParcelHydroPage })
  },
  {
    path: "/farm/parcel/:farmParcelId/natura2000/",
    async: redirectIfNotLoggedIn({ component: FarmParcelNatura2000Page })
  },
  {
    path: "/farm/livestock/",
    async: redirectIfNotLoggedIn({ component: FarmLivestockPage })
  }
];
