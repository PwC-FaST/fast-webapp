import graphene
from graphql_jwt.decorators import login_required

from additional_services.graphql.types import UserServiceSubscriptionType
from additional_services.models import Service, UserServiceSubscription


class UpdateUserServiceSubscription(graphene.Mutation):
    class Arguments:
        service_id = graphene.ID(required=True)
        subscribe = graphene.Boolean(required=True)

    user_service_subscription = graphene.Field(UserServiceSubscriptionType)

    @login_required
    def mutate(self, info, service_id, subscribe):
        service = Service.objects.get(pk=service_id)
        is_already_subscribed = UserServiceSubscription.objects.filter(user=info.context.user, service=service).exists()
        if subscribe and not is_already_subscribed:
            user_service_subscription = UserServiceSubscription(user=info.context.user, service=service)
            user_service_subscription.save()
            return UpdateUserServiceSubscription(user_service_subscription=user_service_subscription)
        elif subscribe and is_already_subscribed:
            user_service_subscription = UserServiceSubscription.objects.filter(user=info.context.user, service=service).get()
            return UpdateUserServiceSubscription(user_service_subscription=user_service_subscription)
        elif not subscribe and is_already_subscribed:
            user_service_subscription = UserServiceSubscription.objects.filter(user=info.context.user, service=service).get()
            user_service_subscription.delete()
            return UpdateUserServiceSubscription(user_service_subscription=None)
