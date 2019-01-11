import graphene
from graphql_jwt.decorators import login_required

from additional_services.models import Service, Provider, SubscriptionType
from additional_services.graphql.types import ServiceType, ProviderType, SubscriptionTypeType


class Query:
    subscription_types = graphene.List(SubscriptionTypeType)

    providers = graphene.List(ProviderType)
    provider = graphene.Field(ProviderType, id=graphene.Argument(graphene.ID, required=True))

    services = graphene.List(ServiceType)
    service = graphene.Field(ServiceType, id=graphene.Argument(graphene.ID, required=True))

    @login_required
    def resolve_subscription_types(self, info):
        return SubscriptionType.objects.all()

    @login_required
    def resolve_providers(self, info):
        return Provider.objects.all()

    @login_required
    def resolve_provider(self, info, id):
        return Provider.objects.filter(pk=id).get()

    @login_required
    def resolve_services(self, info):
        return Service.objects.all().prefetch_related()

    @login_required
    def resolve_service(self, info, id):
        return Service.objects.filter(pk=id).get()
