import graphene
from graphql_jwt.decorators import login_required, staff_member_required
from django.db.models import Q

from farming.graphql.types.farm import FarmingCommitmentType, FarmType, FarmerType, FarmParcelType, FarmLivestockType
from farming.graphql.types.species import LivestockSpeciesType, CropSpeciesType

from farming.models import FarmingCommitment, LivestockSpecies, CropSpecies, Farmer, Farm, FarmParcel, FarmLivestock


class Query(object):
    farming_commitments = graphene.List(FarmingCommitmentType)
    livestock_species = graphene.List(LivestockSpeciesType)
    crop_species = graphene.List(CropSpeciesType)

    farm = graphene.Field(FarmType,
                          farm_id=graphene.Argument(graphene.ID, required=False))

    farms = graphene.List(FarmType)

    farm_parcel = graphene.Field(FarmParcelType,
                                 farm_parcel_id=graphene.Argument(graphene.ID, required=False))

    farm_livestock = graphene.List(FarmLivestockType,
                                   farm_livestock_id=graphene.Argument(graphene.ID, required=False))

    farmer = graphene.Field(FarmerType,
                            farmer_id=graphene.Argument(graphene.ID, required=True))

    farmers = graphene.List(FarmerType,
                            search=graphene.Argument(graphene.String, required=False),
                            offset=graphene.Argument(graphene.Int, required=False),
                            limit=graphene.Argument(graphene.Int, required=False))

    @login_required
    def resolve_farming_commitments(self, info):
        return FarmingCommitment.objects.all()

    @login_required
    def resolve_livestock_species(self, info):
        livestock = LivestockSpecies.objects.filter(parent=None)  # root species
        livestock = livestock.prefetch_related('children', 'children__children')
        return livestock

    @login_required
    def resolve_crop_species(self, info):
        crop_species = CropSpecies.objects.filter(parent=None)  # root species
        crop_species = crop_species.prefetch_related('children', 'children__children')
        return crop_species

    @login_required
    def resolve_farm(self, info):
        farm = Farm.objects.filter(farmers__user=info.context.user)
        farm = farm.prefetch_related('farm_parcels', 'farm_parcels__crop_species')
        return farm.get()

    @login_required
    @staff_member_required
    def resolve_farms(self, info, **kwargs):
        if info.context.user.is_superuser:
            return Farm.objects.all()
        else:
            return Query.resolve_farm(self, info)

    @login_required
    def resolve_farm_parcel(self, info, farm_parcel_id=None):
        if farm_parcel_id:
            return FarmParcel.objects.filter(farm__farmers__user=info.context.user, pk=farm_parcel_id).get()
        else:
            return FarmParcel.objects.filter(farm__farmers__user=info.context.user).all()

    @login_required
    def resolve_farm_livestock(self, info, farm_livestock_id=None):
        if farm_livestock_id:
            return FarmLivestock.objects.filter(farm__farmers__user=info.context.user, pk=farm_livestock_id).get()
        else:
            return FarmLivestock.objects.filter(farm__farmers__user=info.context.user).all()

    @login_required
    def resolve_farmer(self, info, farmer_id):
        farmer = Farmer.objects.filter(pk=farmer_id)
        return farmer.get()

    @login_required
    @staff_member_required
    def resolve_farmers(self, info, search, offset, limit):
        if not info.context.user.is_superuser:
            limit = min(limit, 100)

        farmers = Farmer.objects

        if search is not None:
            farmers = farmers.filter(
                Q(username__search=search) | Q(first_name__search=search) | Q(last_name__search=search))

        if offset:
            farmers = farmers[offset:]

        if limit:
            farmers = farmers[:limit]

        return farmers.select_related('user').all()
