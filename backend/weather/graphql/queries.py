import graphene
from graphql_jwt.decorators import login_required
from django.utils import timezone

from farming.models import FarmParcel
from weather.graphql.types import WeatherAggregateType, weather_loader


class Query(object):
    weather = graphene.Field(WeatherAggregateType,
                             timestamp=graphene.Argument(graphene.DateTime, required=False))

    @login_required
    def resolve_weather(self, info, timestamp=None):
        
        if timestamp is None:
            timestamp = timezone.now()
            
        timestamp = timestamp.replace(minute=0, second=0, microsecond=0)

        farm_parcels = FarmParcel.objects.filter(
            farm__farmers__user=info.context.user)

        lpis_parcel_ids = tuple(fp.lpis_parcel_id for fp in farm_parcels)

        return weather_loader.load((lpis_parcel_ids, timestamp))
