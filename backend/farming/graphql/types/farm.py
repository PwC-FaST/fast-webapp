import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from farming.models import FarmLivestock, FarmingCommitment, Farm, FarmParcel, Farmer

from .gis import GISInfoType, gis_info_loader_farm, gis_info_loader_farm_parcel
from .soil import SoilInfoType, soil_info_loader
from .hydro import HydroIntersectionType, hydro_intersections_loader
from .natura2000 import Natura2000IntersectionType, natura2000_intersections_loader
from .address import AddressType, address_loader
from .svg_snapshot import svg_snapshot_loader

from core.graphql.utils import localized_field_resolver


class FarmingCommitmentType(DjangoObjectType):
    class Meta:
        model = FarmingCommitment

    name = graphene.String(resolver=localized_field_resolver)


class FarmerType(DjangoObjectType):
    class Meta:
        model = Farmer


class FarmType(DjangoObjectType):
    class Meta:
        model = Farm

    gis_info = graphene.Field(GISInfoType)

    @login_required
    def resolve_gis_info(self, info):
        lpis_parcel_ids = tuple(fp.lpis_parcel_id for fp in self.farm_parcels.all())
        return gis_info_loader_farm.load(lpis_parcel_ids)


class FarmParcelConstraintType(graphene.ObjectType):
    id = graphene.String()
    displayName = graphene.String()


class FarmParcelType(DjangoObjectType):
    class Meta:
        model = FarmParcel

    snapshot_svg = graphene.String()
    gis_info = graphene.Field(GISInfoType)
    soil_info = graphene.Field(SoilInfoType)
    hydro_intersections = graphene.List(HydroIntersectionType)
    natura2000_intersections = graphene.List(Natura2000IntersectionType)
    address = graphene.Field(AddressType)

    @login_required
    def resolve_snapshot_svg(self, info):
        primary_parcels = (self.lpis_parcel_id,)
        secondary_parcels = FarmParcel.objects.filter(farm=self.farm).exclude(pk=self.id)
        secondary_parcels = tuple(secondary_parcels.values_list('lpis_parcel_id', flat=True))
        return svg_snapshot_loader.load((primary_parcels, secondary_parcels))

    @login_required
    def resolve_gis_info(self, info):
        return gis_info_loader_farm_parcel.load(self.lpis_parcel_id)

    @login_required
    def resolve_soil_info(self, info):
        return soil_info_loader.load(self.lpis_parcel_id)

    @login_required
    def resolve_address(self, info):
        return address_loader.load(self.lpis_parcel_id)

    def resolve_hydro_intersections(self, info):
        return hydro_intersections_loader.load(self.lpis_parcel_id)

    def resolve_natura2000_intersections(self, info):
        return natura2000_intersections_loader.load(self.lpis_parcel_id)


class FarmLivestockType(DjangoObjectType):
    class Meta:
        model = FarmLivestock
