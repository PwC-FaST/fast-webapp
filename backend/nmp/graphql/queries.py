import graphene
import os
from datetime import datetime
from graphql import GraphQLError
from graphene_django.types import DjangoObjectType
from graphene_django.converter import convert_django_field
from graphql_jwt.decorators import login_required, staff_member_required
from localized_fields.fields import LocalizedField
import requests
import json

from django.db.models import Q

from .types import (PlanType, FarmParcelCropNeedsType, FarmParcelNutrientPlanResultType,
                    ImportedOrExportedLivestockManureType, ProducedLivestockManureType)

from nmp.models import (Plan, FarmParcelCropNeeds, FarmParcelNutrientPlanResult, ImportedOrExportedLivestockManure,
                        ProducedLivestockManure)


class Query(object):
    plans = graphene.List(PlanType)
    plan = graphene.Field(PlanType,
                          plan_id=graphene.Argument(graphene.ID, required=True))

    @login_required
    def resolve_plans(self, info):
        return Plan.objects.filter(farm__farmers__user=info.context.user).all()

    @login_required
    def resolve_plan(self, info, plan_id):
        return Plan.objects.filter(pk=plan_id, farm__farmers__user=info.context.user).get()
