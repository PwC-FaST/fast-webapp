<template>
  <f7-page>
    <f7-block>
      <f7-button @click="onClickLogout" class="color-red">Logout</f7-button>
    </f7-block>

    <f7-block-title>About FaST</f7-block-title>
    <f7-block strong>
      <p>
        This
        <b>Farm Sustainability Tool</b> prototype was built in 2018-2019 by
        <a
          href="https://www.pwc.fr/"
          title="PwC France"
          target="_blank"
        >PwC France</a>
        for the
        <a
          href="https://www.pwc.fr/"
          title="European Commission"
          target="_blank"
        >European Commission</a>.
      </p>
      <f7-row>
        <f7-col class="text-align-center">
          <img src="/static/farmer_mobile_app/img/european-commission.svg" style="height: 60px">
        </f7-col>
        <f7-col class="text-align-center">
          <img
            src="/static/farmer_mobile_app/img/pwc-white.svg"
            style="height: 50px; margin-top: 5px;"
          >
        </f7-col>
      </f7-row>

      <p>
        The source code of the platform and client interfaces is fully open source and available on the
        <a
          href="https://github.com/PwC-FaST"
          title="FaST Github repository"
          target="_blank"
        >FaST Github repository</a>.
      </p>
    </f7-block>

    <f7-block-title>Data sources</f7-block-title>
    <f7-block-header>The following data sources have been loaded in the FaST platform:</f7-block-header>
    <f7-list class="no-margin-top" style="margin-top: 10px !important;">
      <f7-list-item
        v-for="(source, index) in dataSources"
        :key="'source-' + index"
        :footer="source.country"
        :header="source.type"
        :title="source.name"
        @click="openUrl(source.url)"
      >
        <img
          slot="media"
          :src="'/static/farmer_mobile_app/img/' + source.icon"
          style="max-height: 40px; max-width: 40px"
        >
      </f7-list-item>
    </f7-list>

    <f7-block-header>The following data sources are called on demand:</f7-block-header>
    <f7-list class="no-margin-top" style="margin-top: 10px !important;">
      <f7-list-item
        v-for="(source, index) in apis"
        :key="'source-' + index"
        :footer="source.country"
        :header="source.type"
        :title="source.name"
        @click="openUrl(source.url)"
      >
        <img
          slot="media"
          :src="'/static/farmer_mobile_app/img/' + source.icon"
          style="max-height: 40px; max-width: 40px"
        >
      </f7-list-item>
    </f7-list>

    <f7-block-title>Credits</f7-block-title>
    <f7-block-header>The FaST platform prototype makes use of the following great projects:</f7-block-header>
    <f7-list class="no-margin-top" style="margin-top: 10px !important;">
      <f7-list-item
        v-for="(credit, index) in credits"
        :key="'credit-' + index"
        :footer="'license: ' + credit.license"
        :title="credit.name"
        @click="openUrl(credit.url)"
      >
        <img
          slot="media"
          :src="'/static/farmer_mobile_app/img/' + credit.icon"
          style="max-height: 40px; max-width: 40px"
        >
      </f7-list-item>
    </f7-list>
  </f7-page>
</template>

<script>
import { client } from "@/apollo/client";
import { persistor } from "@/apollo/cache";

export default {
  name: "left-panel-page",
  data() {
    return {
      credits: [
        {
          name: "Vue.js",
          url: "https://vuejs.org/",
          icon: "vuejs.svg",
          license: "MIT"
        },
        {
          name: "Icons by Freepik",
          url: "https://www.freepik.com/",
          icon: "freepik.svg",
          license: "CC 3.0 BY"
        },
        {
          name: "Apollo",
          url: "https://www.apollographql.com/",
          icon: "apollo.svg",
          license: "MIT"
        },
        {
          name: "Leaflet",
          url: "https://leafletjs.com/",
          icon: "leaflet.svg",
          license: "2-clause BSD"
        },
        {
          name: "Framework 7",
          url: "https://framework7.io/",
          icon: "framework7.svg",
          license: "MIT"
        },
        {
          name: "Django",
          url: "https://www.djangoproject.com/",
          icon: "django.svg",
          license: "BSD"
        },
        {
          name: "GraphQL",
          url: "https://graphql.org/",
          icon: "graphql.svg",
          license: "MIT"
        },
        {
          name: "Graphene-Python",
          url: "https://graphene-python.org/",
          icon: "graphene.svg",
          license: "MIT"
        },
        {
          name: "Kubernetes",
          url: "https://kubernetes.io/",
          icon: "kubernetes-white.svg",
          license: "Apache 2.0"
        },
        {
          name: "Docker",
          url: "https://www.docker.com/",
          icon: "docker.svg",
          license: "Apache 2.0"
        },
        {
          name: "Nuclio",
          url: "https://nuclio.io/",
          icon: "nuclio.png",
          license: "Apache 2.0"
        },
        {
          name: "Apache Kafka",
          url: "https://kafka.apache.org/",
          icon: "kafka-white.svg",
          license: "Apache 2.0"
        },
        {
          name: "MongoDB",
          url: "https://www.mongodb.com/",
          icon: "mongodb.svg",
          license: "Server Side Public License"
        },
        {
          name: "PostgreSQL",
          url: "https://www.postgresql.org/",
          icon: "postgres-white.svg",
          license: "Postgres open source"
        },
        {
          name: "NodeJS",
          url: "https://nodejs.org/",
          icon: "nodejs.svg",
          license: "Nodejs open source"
        }
      ],
      dataSources: [
        {
          name: "Registre Parcellaire Graphique",
          url: "http://professionnels.ign.fr/rpg",
          icon: "ign.png",
          type: "Land Parcel Identification",
          country: "France"
        },
        {
          name: "SIGPAC (Castilla y León)",
          url: "http://ftp.itacyl.es/cartografia/05_SIGPAC/Catalogo_Metadatos/",
          icon: "cyl.svg",
          type: "Land Parcel Identification",
          country: "Spain"
        },
        {
          name: "BD TOPO® Hydrographie (IGN)",
          url: "http://professionnels.ign.fr/bdtopo-hydrographie",
          icon: "ign.png",
          type: "Hydrology",
          country: "France"
        },
        {
          name: "Red Hydrografica (MITECO)",
          url:
            "https://www.miteco.gob.es/es/cartografia-y-sig/ide/descargas/agua/red-hidrografica.aspx",
          icon: "miteco.jpg",
          type: "Hydrology",
          country: "Spain"
        },
        {
          name: "Natura2000 (EEA)",
          url:
            "https://www.eea.europa.eu/data-and-maps/data/natura-9#tab-gis-data",
          icon: "eea.svg",
          type: "Natura2000 areas",
          country: "Europe"
        },
        {
          name: "Organic Carbon Content (LUCAS)",
          url:
            "https://esdac.jrc.ec.europa.eu/themes/topsoil-soil-organic-carbon-lucas",
          icon: "jrc.png",
          type: "Soil information",
          country: "Europe"
        },
        {
          name: "Topsoil Survey (LUCAS)",
          url:
            "https://esdac.jrc.ec.europa.eu/ESDB_Archive/eusoils_docs/other/EUR26102EN.pdf",
          icon: "jrc.png",
          type: "Soil information",
          country: "Europe"
        },
        {
          name: "Plant variety catalogue",
          url:
            "https://ec.europa.eu/food/plant/plant_propagation_material/plant_variety_catalogues_databases_en",
          icon: "european-commission.svg",
          type: "Crop species",
          country: "Europe"
        },
        {
          name: "European regulation on livestock reporting",
          url:
            "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32008R1165",
          icon: "european-commission.svg",
          type: "Livestock species",
          country: "Europe"
        }
      ],
      apis: [
        {
          name: "Sobloo",
          url: "https://sobloo.eu",
          icon: "sobloo.jpg",
          type: "Sentinel-2 satellite imagery",
          country: "World"
        },
        {
          name: "DarkSky",
          url: "https://darksky.net/",
          icon: "darksky.svg",
          type: "Weather forecast & history",
          country: "World"
        },
        {
          name: "Mapquest",
          url: "https://www.mapquest.com/",
          icon: "mapquest.svg",
          type: "Reverse geocoding",
          country: "World"
        }
      ]
    };
  },
  methods: {
    onClickLogout() {
      // Stop all queries
      this.$apollo.skipAll = true

      // Clear the cache
      persistor.pause();
      persistor.purge();
      client.cache.reset();

      // Clear the token
      window.localStorage.removeItem("fast_token");

      // Clear the history and route to login
      this.$f7.panel.close("left", false);
      this.$f7router.clearPreviousHistory();
      this.$f7.views.main.router.navigate("/login/");
    },
    openUrl(url) {
      window.location = url;
    }
  }
};
</script>
