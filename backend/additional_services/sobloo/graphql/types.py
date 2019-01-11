import datetime
import graphene
import pytz

from promise import Promise
from promise.dataloader import DataLoader
import requests


class ServicesSoblooSentinel2LayerType(graphene.ObjectType):
    """GraphQL node for a WMTS layer served by Sobloo
    """

    id = graphene.ID()

    timestamp = graphene.DateTime(
        description='Timestamp of the request')

    latitude = graphene.Float(
        description='Latitude of search point')

    longitude = graphene.Float(
        description='Longitude of search point')

    external_id = graphene.String(
        description='Business ID as defined by Sobloo')

    uid = graphene.String(
        description='Internal ID as defined by Sobloo')

    wmts_layer_url = graphene.String(
        description='URL template for the WMTS layer')

    cloud_cover = graphene.Float(
        description='Actual cloud cover of the layer')

    max_cloud_cover = graphene.Float(
        description='Maximum acceptable cloud cover requested')

    mission_name = graphene.String(
        description='Sentinel mission name')

    collected_at = graphene.DateTime(
        description='Datetime the image was captured')

    def resolve_id(self, info):
        return hash((self.timestamp, self.latitude,
                     self.longitude, self.max_cloud_cover))


def sobloo_opensearch_params(latitude, longitude, max_cloud_cover):
    """Build Sobloo open search query string to get the latest Sentinel-2 image
    with minimal cloud cover at the requested location

    Arguments:
        latitude {float} -- latitude of search point
        longitude {float} -- longitude of search point
        max_cloud_cover {float} -- max cloud cover percentage (0 to 1)

    Returns:
        dict -- parameters of GET request to Sobloo Opensearch endpoint
    """

    # Create a small polygon around the search point
    polygon = [
        (longitude - 0.001, latitude - 0.001),
        (longitude + 0.001, latitude - 0.001),
        (longitude + 0.001, latitude + 0.001),
        (longitude - 0.001, latitude + 0.001),
        (longitude - 0.001, latitude - 0.001)
    ]

    # To WKT
    polygon = 'POLYGON ((%s))' % ', '.join(['%s %s' % p for p in polygon])

    # Querying the latest Sentinel 2 image for our polygon
    params = {
        'f': [
            'state.services.wmts:eq:true',
            'identification.collection:eq:Sentinel-2',
            'contentDescription.cloudCoverPercentage:lt:%i' % int(
                max_cloud_cover * 100)
        ],
        'sort': '-timeStamp',
        'size': 1,
        'gintersect': polygon
    }

    return params


def sobloo_opensearch_hit_to_graphql_node(timestamp, latitude, longitude,
                                          max_cloud_cover, hit):
    """Convert a Sobloo OpenSearch hit to the corresponding GraphQL node of
    our schema

    Arguments:
        timestamp {int} -- timestamp of the request (UNIX)
        latitude {float} -- latitude of search point
        longitude {float} -- longitude of search point
        max_cloud_cover {float} -- max cloud cover percentage (0 to 1)
        hit {dict} -- a search hit from the Sobloo OpenSearch endpoint

    Returns:
        ServicesSoblooSentinel2LayerType -- the corresponding GraphQL node
    """

    uid = hit['data'].get('uid')

    external_id = hit['data'].get(
        'identification', {}).get(
            'externalId', None)

    wmts_layer_url = 'https://sobloo.eu/api/v1/services/wmts/'
    wmts_layer_url += uid
    wmts_layer_url += '/tiles/1.0.0/default/rgb/EPSG4326/{z}/{x}/{y}.png'

    cloud_cover = hit['data'].get('contentDescription', {}).get(
        'cloudCoverPercentage', None)

    if cloud_cover is not None:
        cloud_cover /= 100

    mission_name = hit['data'].get(
        'acquisition', {}).get(
            'missionName', None)

    collected_at = hit['data'].get(
        'acquisition', {}).get(
            'centerViewingDate', None)

    if collected_at is not None:
        collected_at = datetime.datetime.fromtimestamp(
            int(collected_at/1000), tz=pytz.timezone('UTC'))

    return ServicesSoblooSentinel2LayerType(
        timestamp=timestamp,
        latitude=latitude,
        longitude=longitude,
        external_id=external_id,
        uid=uid,
        wmts_layer_url=wmts_layer_url,
        cloud_cover=cloud_cover,
        max_cloud_cover=max_cloud_cover,
        mission_name=mission_name,
        collected_at=collected_at
    )


class ServicesSoblooSentinel2LayerLoader(DataLoader):
    """Batch loader for Sentinel OpenSearch requests
    """

    max_batch_size = 10

    def batch_load_fn(self, keys):
        """Batch loading function

        Arguments:
            keys {list of tuples} -- List of (timestamp, latitude, longitude,
                                     max_cloud_cover)

        Returns:
            [object] -- A promise resolving to a list of
                        ServicesSoblooSentinel2LayerType nodes
        """

        results = []

        for (timestamp, latitude, longitude, max_cloud_cover) in keys:

            # OpenSearch endpoint from Sobloo
            url = 'https://sobloo.eu/api/v1/services/search'

            params = sobloo_opensearch_params(latitude,
                                              longitude,
                                              max_cloud_cover)

            headers = {'Content-Type': 'application/json'}

            # Get search results
            print(url, params, headers)
            data = requests.get(url, params=params, headers=headers).json()

            if 'hits' in data and data['hits']:

                # Convert result to Graphql node
                result = sobloo_opensearch_hit_to_graphql_node(
                    timestamp, latitude, longitude, max_cloud_cover,
                    data['hits'][0])

                results += [result]
            else:
                results += [None]

        return Promise.resolve(results)


services_sobloo_sentinel2_layer_loader = ServicesSoblooSentinel2LayerLoader()
