import graphene
import os
from promise import Promise
from datetime import datetime
from promise.dataloader import DataLoader
import requests
from core.graphql.types import CountryType
from core.models import Country


class Natura2000FeatureType(graphene.ObjectType):
    id = graphene.String()
    site_code = graphene.String()
    site_name = graphene.String()
    country = graphene.Field(CountryType)
    released_at = graphene.DateTime()
    wkt_type = graphene.String()
    site_types = graphene.List(graphene.String)


class Natura2000IntersectionType(graphene.ObjectType):
    id = graphene.String()
    intersects = graphene.Boolean()
    minimum_distance = graphene.Float()
    intersection = graphene.Float()
    natura2000_feature = graphene.Field(Natura2000FeatureType)


class Natura2000IntersectionLoader(DataLoader):
    def batch_load_fn(self, lpis_parcel_ids):
        url = os.getenv('FAST_API_PARCEL_NATURA2000_URL')
        data = requests.post(url, params={'search': '10000'}, json=lpis_parcel_ids).json()

        # Sort the results in the same order as the request
        sorting = {lpis_parcel_id: index for index, lpis_parcel_id in enumerate(lpis_parcel_ids)}
        data = sorted(data, key=lambda x: sorting[x['_id']])

        results = []
        for lpis_parcel_id, d in zip(lpis_parcel_ids, data):

            result = []
            for n in d['natura2000']:

                if n is None:
                    continue

                # Create a real Country vertex
                country = Country.objects.filter(pk=n.get('country').upper()).get()

                released_at = datetime.strptime(n.get('releaseDate'), '%Y-%m-%d')

                # The feature that is intersecting
                natura2000_feature = Natura2000FeatureType(id=n.get('_id'),
                                                           site_code=n.get('siteCode'),
                                                           site_name=n.get('siteName'),
                                                           wkt_type=n.get('wktType'),
                                                           country=country,
                                                           released_at=released_at,
                                                           site_types=n.get('siteTypes'))

                # The intersection itself
                intersection = Natura2000IntersectionType(id=lpis_parcel_id + '.' + n.get('_id'),
                                                          intersects=n.get('intersects'),
                                                          minimum_distance=n.get('minDistance'),
                                                          intersection=n.get('intersection'),
                                                          natura2000_feature=natura2000_feature)

                result += [intersection]

            results += [result]

        return Promise.resolve(results)


natura2000_intersections_loader = Natura2000IntersectionLoader()