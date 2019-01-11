<template>
  <f7-block strong class="no-margin-top" style="margin-bottom: 10px !important">
    <f7-block-header>
      <f7-row>
        <f7-col>Weather</f7-col>
        <f7-col class="text-align-right">
          <small>{{ $shortDate(feedItem.timestamp) }}</small>
        </f7-col>
      </f7-row>
    </f7-block-header>

    <f7-row>
      <f7-col width="30">Yesterday</f7-col>
      <f7-col v-if="weather.loading" width="70">loading...</f7-col>
      <template v-if="weather.yesterday">
        <f7-col width="40" class="text-align-center">
          from {{ Math.round(weather.yesterday.daily.data[0].temperatureLow) }}°
          to {{ Math.round(weather.yesterday.daily.data[0].temperatureHigh) }}°
        </f7-col>
        <f7-col
          width="30"
          class="text-align-center"
        >{{ Math.round(weather.yesterday.daily.data[0].precipIntensity) }}mm</f7-col>
      </template>
    </f7-row>

    <f7-row>
      <f7-col width="30">Today</f7-col>
      <f7-col v-if="weather.loading" width="70">loading...</f7-col>
      <template v-if="weather.forecast">
        <f7-col width="40" class="text-align-center">
          from {{ Math.round(weather.forecast.daily.data[0].temperatureLow) }}°
          to {{ Math.round(weather.forecast.daily.data[0].temperatureHigh) }}°
        </f7-col>
        <f7-col
          width="30"
          class="text-align-center"
        >{{ Math.round(weather.forecast.daily.data[0].precipIntensity) }}mm</f7-col>
      </template>
    </f7-row>

    <f7-row v-if="weather.forecast && weather.forecast.daily" class="margin-top">
      <f7-col
        v-for="forecast in weather.forecast.daily.data.slice(0, 5)"
        :key="forecast.id"
        width="20"
      >
        <div class="margin-left margin-right">
          <component :is="icons[forecast.icon]"></component>
        </div>

        <div class="text-align-center">
          <small>{{ daysOfWeek[forecast.dayOfWeek] }}</small>
        </div>
        <div class="text-align-center">
          <b>{{ Math.round(forecast.temperatureHigh) }}°</b>
        </div>
        <div class="text-align-center">
          <small v-if="forecast.precipProbability > 0" class="text-align-center display-block">
            <img
              src="/static/farmer_mobile_app/img/humidity.svg"
              height="12"
              style="vertical-align: middle"
            >
            {{ Math.round(forecast.precipProbability * 100) }}%
          </small>
        </div>
      </f7-col>
    </f7-row>
  </f7-block>
</template>

<script>
import queryWeather from "./queryWeather.gql";
import icons from "./icons/icons";

export default {
  name: "weather-forecast-feed-block",
  props: {
    feedItem: { type: Object, required: true }
  },
  apollo: {
    weather: {
      query: queryWeather,
      fetchPolicy: 'cache-first',
      variables() {
        let timestamp = new Date()
        timestamp.setMinutes(0)
        timestamp.setSeconds(0)
        timestamp.setMilliseconds(0)
        return {
          timestamp
        }
      }
    }
  },
  data() {
    return {
      weather: { loading: true }
    };
  },
  created() {
    this.daysOfWeek = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
    this.icons = icons;
  }
};
</script>

<style>
svg.weather-icon path {
  fill: black;
  fill-opacity: 0.7;
}
</style>
