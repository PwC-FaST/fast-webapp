import graphene
import os
from promise import Promise
from promise.dataloader import DataLoader
import requests


class HydroFeatureType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    wkt_type = graphene.String()


class HydroIntersectionType(graphene.ObjectType):
    id = graphene.ID()
    intersects = graphene.Boolean()
    minimum_distance = graphene.Float()
    intersection = graphene.Float()
    hydrology_feature = graphene.Field(HydroFeatureType)


class HydroIntersectionLoader(DataLoader):
    def batch_load_fn(self, lpis_parcel_ids):
        url = os.getenv('FAST_API_PARCEL_HYDRO_URL')
        data = requests.post(url, params={'search': '20'}, json=lpis_parcel_ids).json()

        # Sort the results in the same order as the request
        sorting = {lpis_parcel_id: index for index, lpis_parcel_id in enumerate(lpis_parcel_ids)}
        data = sorted(data, key=lambda x: sorting[x['_id']])

        return Promise.resolve(
            [
                [HydroIntersectionType(id=lpis_parcel_id + '.' + h['_id'],
                                       intersects=h.get('intersects'),
                                       minimum_distance=h.get('minDistance'),
                                       intersection=h.get('intersection'),
                                       hydrology_feature=HydroFeatureType(
                                           id=h['_id'],
                                           wkt_type=h.get('wktType'),
                                           name=h.get('name')
                                       )
                                       ) for h in d['hydro']]
                for lpis_parcel_id, d in zip(lpis_parcel_ids, data)
            ])


hydro_intersections_loader = HydroIntersectionLoader()
