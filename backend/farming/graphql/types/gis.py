import graphene
import os
from promise import Promise
from promise.dataloader import DataLoader
import requests


class CoordinatesType(graphene.ObjectType):
    id = graphene.String()
    coordinate_reference_system = graphene.String()
    x = graphene.Float()
    y = graphene.Float()

    def resolve_id(self, info):
        return hash((self.coordinate_reference_system, round(self.x, 3), round(self.y, 3)))


class GISInfoType(graphene.ObjectType):
    id = graphene.String()
    area = graphene.Float()
    perimeter = graphene.Float()
    centroid = graphene.List(CoordinatesType)


class GisInfoLoaderFarmParcel(DataLoader):
    def batch_load_fn(self, lpis_parcel_ids):
        url = os.getenv('FAST_API_PARCEL_INFO_URL')
        data = requests.post(url, json=list(lpis_parcel_ids)).json()
        data = data['details']

        # Sort the results in the same order as the request
        sorting = {lpis_parcel_id: index for index, lpis_parcel_id in enumerate(lpis_parcel_ids)}
        data = sorted(data, key=lambda x: sorting[x['_id']])

        return Promise.resolve(
            [GISInfoType(id=lpis_parcel_id,
                         area=d['area'],
                         perimeter=d['perimeter'],
                         centroid=[CoordinatesType(
                             coordinate_reference_system=c['crs'],
                             x=c['coords'][0],
                             y=c['coords'][1]
                         ) for c in d['centroid']
                         ]) for lpis_parcel_id, d in zip(lpis_parcel_ids, data)])


gis_info_loader_farm_parcel = GisInfoLoaderFarmParcel()


class GisInfoLoaderFarm(DataLoader):
    def batch_load_fn(self, farm_lpis_parcel_ids):
        url = os.getenv('FAST_API_PARCEL_INFO_URL')
        results = []

        for lpis_parcel_ids in farm_lpis_parcel_ids:
            data = requests.post(url, json=lpis_parcel_ids).json()['aggregated']
            results += [GISInfoType(id=hash(lpis_parcel_ids),
                                    area=data['area'],
                                    perimeter=data['perimeter'],
                                    centroid=[CoordinatesType(
                                        coordinate_reference_system=c['crs'],
                                        x=c['coords'][0],
                                        y=c['coords'][1]
                                    ) for c in data['centroid']
                                    ])]

        return Promise.resolve(results)


gis_info_loader_farm = GisInfoLoaderFarm()