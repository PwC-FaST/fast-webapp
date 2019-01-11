import graphene
from datetime import timedelta
from django.db.models import Count, Q
from django.utils import timezone
from graphql_jwt.decorators import login_required

from messaging.models import Thread
from farming.models import FarmParcel
from additional_services.models import UserServiceSubscription

from feed.graphql.types import (FeedItemType, MessagingNewThreadFeedItemType, MessagingNewMessagesInThreadFeedItemType,
                                FarmingFarmParcelAddedToFarmFeedItemType, WeatherForecastFeedItemType,
                                ServicesSatelliteImageryFeedItemType, ServicesSoblooSatelliteImageryFeedItemType)


class Query:
    feed = graphene.List(FeedItemType)

    @login_required
    def resolve_feed(self, info):

        user = info.context.user
        feed_items = []

        midnight_this_morning = timezone.now().date()

        for label, date_range in [
            ('today', (midnight_this_morning, midnight_this_morning + timedelta(days=1))),
            ('yesterday', (midnight_this_morning -
                           timedelta(days=1), midnight_this_morning)),
                ('earlier', (midnight_this_morning - timedelta(days=180), midnight_this_morning - timedelta(days=1)))]:

            my_threads = Thread.objects.filter(members=user)

            # MessagingNewThreadFeedItemType
            new_threads = my_threads.filter(created_at__range=date_range)
            for thread in new_threads:
                feed_items += [
                    MessagingNewThreadFeedItemType(
                        timestamp=thread.created_at,
                        timegroup=label,
                        thread=thread
                    )]

            # MessagingNewMessagesInThreadFeedItemType
            threads_with_new_messages = my_threads.exclude(
                pk__in=new_threads.values_list('id', flat=True))
            count_new_messages = Count('messages', filter=Q(
                messages__created_at__range=date_range))
            threads_with_new_messages = threads_with_new_messages.annotate(
                number_of_new_messages=count_new_messages)
            threads_with_new_messages = threads_with_new_messages.filter(
                number_of_new_messages__gt=0)

            for thread in threads_with_new_messages:
                feed_items += [
                    MessagingNewMessagesInThreadFeedItemType(
                        timestamp=thread.created_at,
                        timegroup=label,
                        thread=thread,
                        number_of_new_messages=thread.number_of_new_messages
                    )]

            # FarmingFarmParcelAddedToFarmFeedItemType
            farm_parcels_added = FarmParcel.objects.filter(
                farm__farmers__user=user, added_at__range=date_range)
            for farm_parcel in farm_parcels_added:
                feed_items += [
                    FarmingFarmParcelAddedToFarmFeedItemType(
                        timestamp=farm_parcel.added_at,
                        timegroup=label,
                        farm_parcel=farm_parcel
                    )]

        # ServicesSatelliteImageryFeedItemType
        if UserServiceSubscription.objects.filter(user=user, service__id=2).exists():
            feed_items += [
                ServicesSatelliteImageryFeedItemType(
                    timestamp=timezone.now() - timedelta(days=30),
                    timegroup='earlier',
                    band='ndvi',
                    title='Vegetation index',
                    color_scale='greens',
                    date='Dec 27, 2018'
                ),
                ServicesSatelliteImageryFeedItemType(
                    timestamp=timezone.now() - timedelta(days=30),
                    timegroup='earlier',
                    band='infrared',
                    title='Infrared',
                    color_scale='hot',
                    date='Dec 27, 2018'
                )
            ]

        feed_items += [
            WeatherForecastFeedItemType(
                timestamp=timezone.now().replace(minute=0, second=0, microsecond=0),
                timegroup='today'
            )
        ]

        # ServicesSoblooSatelliteImageryFeedItemType
        if UserServiceSubscription.objects.filter(user=user, service__id=7).exists():
            feed_items += [
                ServicesSoblooSatelliteImageryFeedItemType(
                    timestamp=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0),
                    timegroup='today'
                )
            ]

        feed_items = reversed(sorted(feed_items, key=lambda x: x.timestamp))

        return feed_items
