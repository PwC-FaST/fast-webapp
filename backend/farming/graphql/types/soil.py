import graphene
import os
from promise import Promise
from promise.dataloader import DataLoader
import requests


class SoilInfoType(graphene.ObjectType):
    id = graphene.String()
    coarse = graphene.Float()
    clay = graphene.Float()
    silt = graphene.Float()
    sand = graphene.Float()
    ph_in_h20 = graphene.Float(name='pHinH20')
    ph_in_cacl2 = graphene.Float(name='pHinCaCl2')
    organic_carbon = graphene.Float()
    caco3 = graphene.Float(name='CaCO3')
    nitrogen = graphene.Float()
    phosphorus = graphene.Float()
    potassium = graphene.Float()
    cation_exchange_capacity = graphene.Float()
    number_of_soil_samples_within_buffer = graphene.Int()
    closest_sample_distance = graphene.Float()


class SoilInfoLoader(DataLoader):
    def batch_load_fn(self, lpis_parcel_ids):
        url = os.getenv('FAST_API_PARCEL_TOPSOIL_URL')
        data = requests.post(url, json=lpis_parcel_ids).json()

        # Sort the results in the same order as the request
        sorting = {lpis_parcel_id: index for index, lpis_parcel_id in enumerate(lpis_parcel_ids)}
        data = sorted(data, key=lambda x: sorting[x['_id']])

        return Promise.resolve([
            SoilInfoType(
                id=lpis_parcel_id,
                coarse=d['topsoil'].get('coarse'),
                clay=d['topsoil'].get('clay'),
                silt=d['topsoil'].get('silt'),
                sand=d['topsoil'].get('sand'),
                ph_in_h20=d['topsoil'].get('pHinH2O'),
                ph_in_cacl2=d['topsoil'].get('pHinCaCl2'),
                organic_carbon=d['topsoil'].get('OC'),
                caco3=d['topsoil'].get('CaCO3'),
                nitrogen=d['topsoil'].get('N'),
                phosphorus=d['topsoil'].get('P'),
                potassium=d['topsoil'].get('K'),
                cation_exchange_capacity=d['topsoil'].get('CEC'),
                number_of_soil_samples_within_buffer=d.get('nbSamples'),
                closest_sample_distance=d.get('closestSampleDistance')
            ) for lpis_parcel_id, d in zip(lpis_parcel_ids, data)
        ])


soil_info_loader = SoilInfoLoader()
