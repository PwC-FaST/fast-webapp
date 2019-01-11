import graphene
from graphene_django.types import DjangoObjectType

from farming.models import (LivestockSpecies, CropSpecies)
from core.graphql.utils import localized_field_resolver


class LivestockSpeciesType(DjangoObjectType):
    class Meta:
        model = LivestockSpecies

    name_singular = graphene.String(resolver=localized_field_resolver)
    name_plural = graphene.String(resolver=localized_field_resolver)
    root_livestock_species = graphene.Field(lambda: LivestockSpeciesType)

    def resolve_root_livestock_species(self, info):
        return self.parent if self.parent else self


class CropSpeciesType(DjangoObjectType):
    class Meta:
        model = CropSpecies

    name_singular = graphene.String(resolver=localized_field_resolver)
    name_plural = graphene.String(resolver=localized_field_resolver)