from django.utils import timezone

import graphene
from graphql_jwt.decorators import login_required, staff_member_required

from farming.graphql.types.farm import FarmParcelType, FarmLivestockType
from farming.models import Farm, FarmParcel, FarmingCommitment, LivestockSpecies, CropSpecies, FarmLivestock


class AddFarmParcelToFarm(graphene.Mutation):
    class Arguments:
        lpis_parcel_id = graphene.String(required=True)
        farm_id = graphene.ID(required=True)

    farm_parcel = graphene.Field(FarmParcelType)

    @staticmethod
    @login_required
    def mutate(root, info, lpis_parcel_id, farm_id):
        user = info.context.user
        farm = Farm.objects.filter(pk=farm_id).get()

        if farm.farm_parcels.filter(lpis_parcel_id=lpis_parcel_id).exists():
            return AddFarmParcelToFarm(farm_parcel=farm.farm_parcels.filter(lpis_parcel_id=lpis_parcel_id).get())

        name = ('Parcel ' + lpis_parcel_id.split(':')[-1])[:32]

        farm_parcel = FarmParcel(farm=farm,
                                 name=name,
                                 lpis_parcel_id=lpis_parcel_id,
                                 added_at=timezone.now(),
                                 added_by=user)

        farm_parcel.save()

        return AddFarmParcelToFarm(farm_parcel=farm_parcel)


class RemoveFarmParcelFromFarm(graphene.Mutation):
    class Arguments:
        farm_parcel_id = graphene.ID(required=True)

    farm_parcel = graphene.Field(FarmParcelType)

    @staticmethod
    @login_required
    def mutate(root, info, farm_parcel_id):
        FarmParcel.objects.filter(pk=farm_parcel_id).delete()

        return RemoveFarmParcelFromFarm(None)


class UpdateFarmParcel(graphene.Mutation):
    class Arguments:
        farm_parcel_id = graphene.ID(required=True)
        name = graphene.String(required=False)
        farming_commitment_ids = graphene.List(graphene.NonNull(graphene.ID), required=False)
        crop_species_id = graphene.ID(required=False)

    farm_parcel = graphene.Field(FarmParcelType)

    @staticmethod
    @login_required
    def mutate(root, info, farm_parcel_id, **kwargs):
        farm_parcel = FarmParcel.objects.filter(pk=farm_parcel_id).get()

        if 'name' in kwargs:
            farm_parcel.name = kwargs['name'][:32]
            farm_parcel.save()

        if 'crop_species_id' in kwargs:
            if kwargs['crop_species_id'] in [-1, "-1"]:
                farm_parcel.crop_species = None
            else:
                crop_species = CropSpecies.objects.filter(pk=kwargs['crop_species_id']).get()
                farm_parcel.crop_species = crop_species

        if 'name' in kwargs or 'crop_species_id' in kwargs:
            farm_parcel.save()

        if 'farming_commitment_ids' in kwargs:
            farming_commitments = FarmingCommitment.objects.filter(pk__in=kwargs['farming_commitment_ids']).all()
            farm_parcel.farming_commitments.set(farming_commitments)

        return UpdateFarmParcel(farm_parcel=farm_parcel)


class UpdateFarmLivestock(graphene.Mutation):
    class Arguments:
        farm_id = graphene.ID(required=True)
        livestock_species_id = graphene.ID(required=True)
        number_of_heads = graphene.Int(required=True)
        start_at = graphene.DateTime(required=False)
        end_at = graphene.DateTime(required=False)

    farm_livestock = graphene.Field(FarmLivestockType)
    created = graphene.Boolean()

    @staticmethod
    @login_required
    def mutate(root, info, farm_id, livestock_species_id, number_of_heads, **kwargs):
        farm = Farm.objects.filter(pk=farm_id).get()
        livestock_species = LivestockSpecies.objects.filter(pk=livestock_species_id).get()

        farm_livestock = FarmLivestock.objects.filter(farm=farm, livestock_species=livestock_species)

        if farm_livestock.exists():

            if number_of_heads == 0:
                farm_livestock.delete()
                return UpdateFarmLivestock(None)

            farm_livestock = farm_livestock.get()
            farm_livestock.number_of_heads = number_of_heads

            if 'start_at' in kwargs:
                farm_livestock['start_at'] = kwargs['start_at']

            if 'end_at' in kwargs:
                farm_livestock['end_at'] = kwargs['end_at']

            farm_livestock.save()

            return UpdateFarmLivestock(farm_livestock=farm_livestock, created=False)

        else:
            farm_livestock = FarmLivestock(farm=farm,
                                           livestock_species=livestock_species,
                                           number_of_heads=number_of_heads,
                                           **kwargs)
            farm_livestock.save()

            return UpdateFarmLivestock(farm_livestock=farm_livestock, created=True)


class RemoveFarmLivestock(graphene.Mutation):
    class Arguments:
        farm_id = graphene.ID(required=True)
        livestock_species_id = graphene.ID(required=True)

    farm_livestock = graphene.Field(FarmLivestockType)

    @login_required
    def mutate(self, info, farm_id, livestock_species_id):
        FarmLivestock.objects.filter(farm__id=farm_id, livestock_species__id=livestock_species_id).delete()
        return RemoveFarmLivestock(farm_livestock=None)
