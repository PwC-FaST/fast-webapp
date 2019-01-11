"""GraphQL queries for Sobloo additooal service
"""

import graphene
from graphql_jwt.decorators import login_required
from django.utils import timezone

from additional_services.sobloo.graphql.types import (
    ServicesSoblooSentinel2LayerType, services_sobloo_sentinel2_layer_loader
)


class Query:
    """Root query node for Sobloo service
    """

    services_sobloo_latest_sentinel2_layer = graphene.Field(
        ServicesSoblooSentinel2LayerType,
        latitude=graphene.Argument(
            graphene.Float,
            required=True,
            description='Latitude of search point'),
        longitude=graphene.Argument(
            graphene.Float,
            required=True,
            description='Longitude of search point'),
        max_cloud_cover=graphene.Argument(
            graphene.Float,
            default_value=0.5,
            description='Max acceptable cloud cover of satellite image')
    )

    @login_required
    def resolve_services_sobloo_latest_sentinel2_layer(self,
                                                       info,
                                                       latitude,
                                                       longitude,
                                                       max_cloud_cover):
        """Resolver for services_sobloo_latest_sentinel2_layer field

        Arguments:
            self {object} -- Node
            info {dict} -- Query info as forwarded by graphene
            latitude {float} -- Latitude of serach point
            longitude {float} -- Longitude of search point
            max_cloud_cover {float} -- Max cloud cover percentage (0 - 1)
        """

        timestamp = timezone.now().replace(minute=0, second=0, microsecond=0)

        # Push task to the loader
        return services_sobloo_sentinel2_layer_loader.load((timestamp,
                                                            latitude,
                                                            longitude,
                                                            max_cloud_cover))
