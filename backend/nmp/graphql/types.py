from graphene_django.types import DjangoObjectType
from graphene.utils.str_converters import to_snake_case

from nmp.models import (Plan, ProducedLivestockManure, ImportedOrExportedLivestockManure,
                        FarmParcelCropNeeds, FarmParcelNutrientPlanResult)


def localized_field_resolver(obj, info, **kwargs):
    """
    Custom resolver to return the user language value from localized fields
    """
    if info.context.user.is_authenticated:
        return getattr(obj, to_snake_case(info.field_name)).get(info.context.user.language)
    else:
        return getattr(obj, to_snake_case(info.field_name)).get('en')


class PlanType(DjangoObjectType):
    class Meta:
        model = Plan


class PlanType(DjangoObjectType):
    class Meta:
        model = Plan


class ProducedLivestockManureType(DjangoObjectType):
    class Meta:
        model = ProducedLivestockManure


class ImportedOrExportedLivestockManureType(DjangoObjectType):
    class Meta:
        model = ImportedOrExportedLivestockManure


class FarmParcelCropNeedsType(DjangoObjectType):
    class Meta:
        model = FarmParcelCropNeeds


class FarmParcelNutrientPlanResultType(DjangoObjectType):
    class Meta:
        model = FarmParcelNutrientPlanResult
