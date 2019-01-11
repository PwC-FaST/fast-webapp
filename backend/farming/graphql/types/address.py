import graphene
import os
from promise import Promise
from promise.dataloader import DataLoader
import requests


class AddressType(graphene.ObjectType):
    id = graphene.ID()
    street = graphene.String()
    city = graphene.String()
    postcode = graphene.String()
    country = graphene.String()


class AddressLoader(DataLoader):
    max_batch_size = 100

    def batch_load_fn(self, lpis_parcel_ids):
        # Query the GIS info service for the centroids
        url = os.getenv('FAST_API_PARCEL_INFO_URL')
        data = requests.post(url, json=lpis_parcel_ids).json()['details']

        # Extract the WGS84 coords for each centroid
        centroids = [list(filter(lambda c: c['crs'] == 'EPSG:4326', d['centroid']))[0] for d in data]
        list_of_coords = [(round(c['coords'][1], 3), round(c['coords'][0], 3)) for c in centroids]

        # Query the Mapquest service for the reverse geocoding
        url = os.getenv('FAST_MAPQUEST_API_URL')
        params = {
            'key': os.getenv('FAST_MAPQUEST_API_KEY'),
            'location': ['{},{}'.format(*coords) for coords in list_of_coords],
            'method': 'reverse'
        }
        data = requests.get(url, params).json()

        return Promise.resolve([
            AddressType(
                id=coords,
                street=result['locations'][0]['street'],
                city=result['locations'][0]['adminArea5'],
                postcode=result['locations'][0]['postalCode'],
                country=result['locations'][0]['adminArea1']
            ) for (coords, result) in zip(list_of_coords, data['results'])])


address_loader = AddressLoader()