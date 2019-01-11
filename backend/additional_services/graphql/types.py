import graphene
from graphene_django.types import DjangoObjectType

from graphql_jwt.decorators import login_required
from core.graphql.utils import localized_field_resolver
from additional_services.models import Service, SubscriptionType, Provider, UserServiceSubscription


class ProviderType(DjangoObjectType):
    class Meta:
        model = Provider

    website = graphene.String(resolver=localized_field_resolver)
    short_name = graphene.String(resolver=localized_field_resolver)
    display_name = graphene.String(resolver=localized_field_resolver)


class SubscriptionTypeType(DjangoObjectType):
    class Meta:
        model = SubscriptionType

    display_name = graphene.String(resolver=localized_field_resolver)


class ServiceType(DjangoObjectType):
    class Meta:
        model = Service

    display_name = graphene.String(resolver=localized_field_resolver)
    short_description = graphene.String(resolver=localized_field_resolver)

    @login_required
    def resolve_user_subscriptions(self, info):
        return self.user_subscriptions.filter(user=info.context.user)


class UserServiceSubscriptionType(DjangoObjectType):
    class Meta:
        model = UserServiceSubscription
