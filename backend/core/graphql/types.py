import graphene
from graphene_django.types import DjangoObjectType
from core.models import FaSTUser, Country
from core.graphql.utils import localized_field_resolver


def resolve_full_name(obj, info):
    if obj.first_name and obj.last_name:
        return '{} {}'.format(obj.first_name, obj.last_name).strip()
    elif obj.first_name:
        return obj.first_name
    elif obj.last_name:
        return obj.last_name
    else:
        return obj.username


class CurrentFaSTUserType(DjangoObjectType):
    class Meta:
        model = FaSTUser
        exclude_fields = ('password',)

    full_name = graphene.String(resolver=resolve_full_name)


class FaSTUserType(DjangoObjectType):
    class Meta:
        model = FaSTUser
        only_fields = ('id', 'username', 'first_name', 'last_name', 'full_name', 'country', 'language', 'picture',
                       'date_joined', 'contact')

    full_name = graphene.String(resolver=resolve_full_name)


class CountryType(DjangoObjectType):
    class Meta:
        model = Country

    id = graphene.ID(source='id')
    name = graphene.String(resolver=localized_field_resolver)