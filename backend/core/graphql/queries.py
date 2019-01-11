import graphene
from graphql_jwt.decorators import login_required, staff_member_required

from core.graphql.types import CurrentFaSTUserType, CountryType
from core.models import FaSTUser, Country


class Query(object):
    countries = graphene.List(CountryType)
    who_am_i = graphene.Field(CurrentFaSTUserType)

    @login_required
    def resolve_who_am_i(self, info):
        return info.context.user

    @login_required
    def resolve_countries(self, info, **kwargs):
        return Country.objects.all()