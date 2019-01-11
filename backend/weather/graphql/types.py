import graphene
import os
from datetime import datetime, timedelta
import pytz
from promise import Promise
from promise.dataloader import DataLoader
from graphene import ObjectType
import requests


class CurrentlyWeatherPointType(graphene.ObjectType):
    id = graphene.ID()
    datetime = graphene.DateTime()

    time = graphene.Int()
    timezone = graphene.String()
    summary = graphene.String()
    icon = graphene.String()
    nearestStormDistance = graphene.Float()
    nearestStormBearing = graphene.Float()
    precipIntensity = graphene.Float()
    precipIntensityError = graphene.Float()
    precipProbability = graphene.Float()
    precipType = graphene.String()
    precipAccumulation = graphene.Float()
    temperature = graphene.Float()
    apparentTemperature = graphene.Float()
    dewPoint = graphene.Float()
    humidity = graphene.Float()
    pressure = graphene.Float()
    windSpeed = graphene.Float()
    windGust = graphene.Float()
    windBearing = graphene.Float()
    cloudCover = graphene.Float()
    uvIndex = graphene.Float()
    visibility = graphene.Float()
    ozone = graphene.Float()

    def resolve_datetime(self, info):
        return datetime.fromtimestamp(self.time, tz=pytz.timezone(self.timezone))

    def resolve_id(self, info):
        return datetime.fromtimestamp(self.time, tz=pytz.timezone(self.timezone))


class CurrentlyWeatherType(graphene.ObjectType):
    id = graphene.ID()
    summary = graphene.String()
    icon = graphene.String()
    data = graphene.Field(CurrentlyWeatherPointType)

    def resolve_id(self, info):
        if self.data is not None and len(self.data) > 0:
            return datetime.fromtimestamp(self.data[0].time, tz=pytz.timezone(self.data[0].timezone))
        else:
            return None


class MinutelyWeatherPointType(graphene.ObjectType):
    id = graphene.ID()
    datetime = graphene.DateTime()

    time = graphene.Int()
    timezone = graphene.String()
    precipIntensity = graphene.Float()
    precipIntensityError = graphene.Float()
    precipProbability = graphene.Float()
    precipType = graphene.String()

    def resolve_datetime(self, info):
        return datetime.fromtimestamp(self.time, tz=pytz.timezone(self.timezone))

    def resolve_id(self, info):
        return datetime.fromtimestamp(self.time, tz=pytz.timezone(self.timezone))


class MinutelyWeatherType(graphene.ObjectType):
    id = graphene.ID()
    summary = graphene.String()
    icon = graphene.String()
    data = graphene.List(MinutelyWeatherPointType)

    def resolve_id(self, info):
        if self.data is not None and len(self.data) > 0:
            return datetime.fromtimestamp(self.data[0].time, tz=pytz.timezone(self.data[0].timezone))
        else:
            return None


class HourlyWeatherPointType(graphene.ObjectType):
    id = graphene.ID()
    datetime = graphene.DateTime()

    time = graphene.Int()
    timezone = graphene.String()
    summary = graphene.String()
    icon = graphene.String()
    precipIntensity = graphene.Float()
    precipProbability = graphene.Float()
    precipAccumulation = graphene.Float()
    precipType = graphene.String()
    temperature = graphene.Float()
    apparentTemperature = graphene.Float()
    dewPoint = graphene.Float()
    humidity = graphene.Float()
    pressure = graphene.Float()
    windSpeed = graphene.Float()
    windGust = graphene.Float()
    windBearing = graphene.Float()
    cloudCover = graphene.Float()
    uvIndex = graphene.Float()
    visibility = graphene.Float()
    ozone = graphene.Float()

    def resolve_datetime(self, info):
        return datetime.fromtimestamp(self.time, tz=pytz.timezone(self.timezone))

    def resolve_id(self, info):
        return datetime.fromtimestamp(self.time, tz=pytz.timezone(self.timezone))


class HourlyWeatherType(graphene.ObjectType):
    id = graphene.ID()
    summary = graphene.String()
    icon = graphene.String()
    data = graphene.List(HourlyWeatherPointType)

    def resolve_id(self, info):
        if self.data is not None and len(self.data) > 0:
            return datetime.fromtimestamp(self.data[0].time, tz=pytz.timezone(self.data[0].timezone))
        else:
            return None


class DailyWeatherPointType(graphene.ObjectType):
    id = graphene.ID()
    datetime = graphene.DateTime()

    time = graphene.Int()
    timezone = graphene.String()
    day_of_week = graphene.Int()
    summary = graphene.String()
    icon = graphene.String()
    sunriseTime = graphene.DateTime()
    sunsetTime = graphene.DateTime()
    moonPhase = graphene.Float()
    precipIntensity = graphene.Float()
    precipIntensityMax = graphene.Float()
    precipIntensityMaxTime = graphene.DateTime()
    precipProbability = graphene.Float()
    precipType = graphene.String()
    precipAccumulation = graphene.Float()
    temperatureHigh = graphene.Float()
    temperatureHighTime = graphene.DateTime()
    temperatureLow = graphene.Float()
    temperatureLowTime = graphene.DateTime()
    apparentTemperatureHigh = graphene.Float()
    apparentTemperatureHighTime = graphene.DateTime()
    apparentTemperatureLow = graphene.Float()
    apparentTemperatureLowTime = graphene.DateTime()
    dewPoint = graphene.Float()
    humidity = graphene.Float()
    pressure = graphene.Float()
    windSpeed = graphene.Float()
    windGust = graphene.Float()
    windGustTime = graphene.DateTime()
    windBearing = graphene.Float()
    cloudCover = graphene.Float()
    uvIndex = graphene.Float()
    uvIndexTime = graphene.DateTime()
    visibility = graphene.Float()
    ozone = graphene.Float()
    temperatureMin = graphene.Float()
    temperatureMinTime = graphene.DateTime()
    temperatureMax = graphene.Float()
    temperatureMaxTime = graphene.DateTime()
    apparentTemperatureMin = graphene.Float()
    apparentTemperatureMinTime = graphene.DateTime()
    apparentTemperatureMax = graphene.Float()
    apparentTemperatureMaxTime = graphene.DateTime()

    def resolve_datetime(self, info):
        return datetime.fromtimestamp(self.time, tz=pytz.timezone(self.timezone))

    def resolve_id(self, info):
        return str(datetime.fromtimestamp(self.time, tz=pytz.timezone(self.timezone)))

    def resolve_day_of_week(self, info):
        return datetime.fromtimestamp(self.time, tz=pytz.timezone(self.timezone)).weekday()


class DailyWeatherType(graphene.ObjectType):
    id = graphene.ID()
    summary = graphene.String()
    icon = graphene.String()
    data = graphene.List(DailyWeatherPointType)

    def resolve_id(self, info):
        if self.data is not None and len(self.data) > 0:
            return datetime.fromtimestamp(self.data[0].time, tz=pytz.timezone(self.data[0].timezone))
        else:
            return None


class AlertType(graphene.ObjectType):
    id = graphene.ID()
    datetime = graphene.DateTime()

    title = graphene.String()
    time = graphene.Int()
    timezone = graphene.String()
    expires = graphene.Int()
    description = graphene.String()
    uri = graphene.String()
    regions = graphene.List(graphene.String)
    severity = graphene.String()

    def resolve_datetime(self, info):
        return datetime.fromtimestamp(self.time, tz=pytz.timezone(self.timezone))

    def resolve_id(self, info):
        return '%s/%s' % (datetime.fromtimestamp(self.time), self.title)


class WeatherType(ObjectType):
    id = graphene.ID()
    datetime = graphene.DateTime()
    latitude = graphene.NonNull(graphene.Float)
    longitude = graphene.NonNull(graphene.Float)
    currently = graphene.Field(CurrentlyWeatherType)
    minutely = graphene.Field(MinutelyWeatherType)
    hourly = graphene.Field(HourlyWeatherType)
    daily = graphene.Field(DailyWeatherType)
    alerts = graphene.List(AlertType)

    def resolve_id(self, info):
        return hash((self.datetime, self.longitude, self.latitude))


class WeatherAggregateType(ObjectType):
    id = graphene.ID()
    yesterday = graphene.Field(WeatherType)
    forecast = graphene.Field(WeatherType)


def dark_sky_to_weather_type(data, timestamp, latitude, longitude):

    tz = data['timezone']

    if 'currently' in data:
        d = CurrentlyWeatherPointType(time=data['currently'].get('time'),
                                      timezone=tz,
                                      summary=data['currently'].get('summary'),
                                      icon=data['currently'].get('icon'),
                                      nearestStormDistance=data['currently'].get(
                                          'nearestStormDistance'),
                                      nearestStormBearing=data['currently'].get(
                                          'nearestStormBearing'),
                                      precipIntensity=data['currently'].get(
                                          'precipIntensity'),
                                      precipIntensityError=data['currently'].get(
                                          'precipIntensityError'),
                                      precipProbability=data['currently'].get(
                                          'precipProbability'),
                                      precipType=data['currently'].get(
                                          'precipType'),
                                      precipAccumulation=data['currently'].get(
                                          'precipAccumulation'),
                                      temperature=data['currently'].get(
                                          'temperature'),
                                      apparentTemperature=data['currently'].get(
                                          'apparentTemperature'),
                                      dewPoint=data['currently'].get(
                                          'dewPoint'),
                                      humidity=data['currently'].get(
                                          'humidity'),
                                      pressure=data['currently'].get(
                                          'pressure'),
                                      windSpeed=data['currently'].get(
                                          'windSpeed'),
                                      windGust=data['currently'].get(
                                          'windGust'),
                                      windBearing=data['currently'].get(
                                          'windBearing'),
                                      cloudCover=data['currently'].get(
                                          'cloudCover'),
                                      uvIndex=data['currently'].get('uvIndex'),
                                      visibility=data['currently'].get(
                                          'visibility'),
                                      ozone=data['currently'].get('ozone'))

        currently = CurrentlyWeatherType(summary=data['currently'].get('summary'),
                                         icon=data['currently'].get('icon'),
                                         data=d)
    else:
        currently = None

    if 'minutely' in data:
        d = [MinutelyWeatherPointType(time=p.get('time'),
                                      timezone=tz,
                                      precipIntensity=p.get('precipIntensity'),
                                      precipIntensityError=p.get(
                                          'precipIntensityError'),
                                      precipProbability=p.get(
                                          'precipProbability'),
                                      precipType=p.get('precipType'))
             for p in data['minutely'].get('data', [])]

        minutely = MinutelyWeatherType(summary=data['minutely'].get('summary'),
                                       icon=data['minutely'].get('icon'),
                                       data=d)
    else:
        minutely = None

    if 'hourly' in data:
        d = [HourlyWeatherPointType(time=p.get('time'),
                                    timezone=tz,
                                    summary=p.get('summary'),
                                    icon=p.get('icon'),
                                    precipIntensity=p.get('precipIntensity'),
                                    precipProbability=p.get(
                                        'precipProbability'),
                                    precipAccumulation=p.get(
                                        'precipAccumulation'),
                                    precipType=p.get('precipType'),
                                    temperature=p.get('temperature'),
                                    apparentTemperature=p.get(
                                        'apparentTemperature'),
                                    dewPoint=p.get('dewPoint'),
                                    humidity=p.get('humidity'),
                                    pressure=p.get('pressure'),
                                    windSpeed=p.get('windSpeed'),
                                    windGust=p.get('windGust'),
                                    windBearing=p.get('windBearing'),
                                    cloudCover=p.get('cloudCover'),
                                    uvIndex=p.get('uvIndex'),
                                    visibility=p.get('visibility'),
                                    ozone=p.get('ozone'))
             for p in data['hourly'].get('data', [])]

        hourly = HourlyWeatherType(summary=data['hourly'].get('summary'),
                                   icon=data['hourly'].get('icon'),
                                   data=d)
    else:
        hourly = None

    if 'daily' in data:
        d = [
            DailyWeatherPointType(time=p.get('time'),
                                  timezone=tz,
                                  summary=p.get('summary'),
                                  icon=p.get('icon'),
                                  sunriseTime=p.get('sunriseTime'),
                                  sunsetTime=p.get('sunsetTime'),
                                  moonPhase=p.get('moonPhase'),
                                  precipIntensity=p.get('precipIntensity'),
                                  precipIntensityMax=p.get(
                                      'precipIntensityMax'),
                                  precipIntensityMaxTime=p.get(
                'precipIntensityMaxTime'),
                precipProbability=p.get(
                'precipProbability'),
                precipType=p.get('precipType'),
                precipAccumulation=p.get(
                'precipAccumulation'),
                temperatureHigh=p.get('temperatureHigh'),
                temperatureHighTime=p.get(
                'temperatureHighTime'),
                temperatureLow=p.get('temperatureLow'),
                temperatureLowTime=p.get(
                'temperatureLowTime'),
                apparentTemperatureHigh=p.get(
                'apparentTemperatureHigh'),
                apparentTemperatureHighTime=p.get(
                'apparentTemperatureHighTime'),
                apparentTemperatureLow=p.get(
                'apparentTemperatureLow'),
                apparentTemperatureLowTime=p.get(
                'apparentTemperatureLowTime'),
                dewPoint=p.get('dewPoint'),
                humidity=p.get('humidity'),
                pressure=p.get('pressure'),
                windSpeed=p.get('windSpeed'),
                windGust=p.get('windGust'),
                windGustTime=p.get('windGustTime'),
                windBearing=p.get('windBearing'),
                cloudCover=p.get('cloudCover'),
                uvIndex=p.get('uvIndex'),
                uvIndexTime=p.get('uvIndexTime'),
                visibility=p.get('visibility'),
                ozone=p.get('ozone'),
                temperatureMin=p.get('temperatureMin'),
                temperatureMinTime=p.get(
                'temperatureMinTime'),
                temperatureMax=p.get('temperatureMax'),
                temperatureMaxTime=p.get(
                'temperatureMaxTime'),
                apparentTemperatureMin=p.get(
                'apparentTemperatureMin'),
                apparentTemperatureMinTime=p.get(
                'apparentTemperatureMinTime'),
                apparentTemperatureMax=p.get(
                'apparentTemperatureMax'),
                apparentTemperatureMaxTime=p.get('apparentTemperatureMaxTime'))
            for p in data['daily'].get('data', [])
        ]

        daily = DailyWeatherType(summary=data['daily'].get('summary'),
                                 icon=data['daily'].get('icon'),
                                 data=d)
    else:
        daily = None

    if 'alerts' in data:
        alerts = [AlertType(title=p.get('title'),
                            time=p.get('time'),
                            timezone=tz,
                            expires=p.get('expires'),
                            description=p.get('description'),
                            uri=p.get('uri'),
                            regions=p.get('regions'),
                            severity=p.get('severity'))
                  for p in data['alerts']]
    else:
        alerts = None

    return WeatherType(datetime=timestamp, latitude=latitude, longitude=longitude,
                       currently=currently, minutely=minutely, hourly=hourly, daily=daily, alerts=alerts)


class WeatherLoader(DataLoader):
    max_batch_size = 1

    def batch_load_fn(self, keys):

        list_of_coords = []
        list_of_timestamps = [k[1] for k in keys]
        results = []

        # Query the GIS info service for the centroid
        for key in keys:
            lpis_parcel_ids = key[0]
            url = os.getenv('FAST_API_PARCEL_INFO_URL')
            data = requests.post(url, json=lpis_parcel_ids).json()[
                'aggregated']

            # Extract the WGS84 coords for the centroid
            centroid = list(
                filter(lambda c: c['crs'] == 'EPSG:4326', data['centroid']))[0]
            list_of_coords += [(round(centroid['coords'][1], 3),
                                round(centroid['coords'][0], 3))]

        # Query the Dark Sky API
        key = os.getenv('FAST_DARK_SKY_API_KEY')
        url_time_machine = os.getenv('FAST_DARK_SKY_TIME_MACHINE_API_URL')
        url_forecast = os.getenv('FAST_DARK_SKY_FORECAST_API_URL')

        for coords, timestamp in zip(list_of_coords, list_of_timestamps):
            latitude, longitude = coords[0], coords[1]

            # First query the forecast
            url = url_forecast.format(
                key=key, latitude=latitude, longitude=longitude)
            print(url)
            response = requests.get(url)

            try:
                data = response.json()
            except Exception as exc:
                print(str(exc), data.text)
                results += [None]
                continue

            # Convert to our GraphQL types
            weather_type_forecast = dark_sky_to_weather_type(data, latitude=latitude, longitude=longitude,
                                                             timestamp=timestamp)

            # Then query the historical weather from previous day
            time = (timestamp - timedelta(days=1)
                    ).strftime('%Y-%m-%dT%H:%M:%S%z')
            url = url_time_machine.format(
                key=key, latitude=latitude, longitude=longitude, time=time)
            response = requests.get(url)

            try:
                data = response.json()
            except Exception as exc:
                print(str(exc), data.text)
                results += [None]
                continue

            weather_type_yesterday = dark_sky_to_weather_type(data, latitude=latitude, longitude=longitude,
                                                              timestamp=timestamp - timedelta(days=1))

            results += [WeatherAggregateType(id=str(timestamp),
                                             yesterday=weather_type_yesterday,
                                             forecast=weather_type_forecast)]

        return Promise.resolve(results)


weather_loader = WeatherLoader()
