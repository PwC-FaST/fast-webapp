import graphene
import graphql_jwt

from core.graphql.types import FaSTUserType

import core.graphql.queries
import feed.graphql.queries
import farming.graphql.queries
import messaging.graphql.queries
import weather.graphql.queries
import additional_services.graphql.queries
import additional_services.sobloo.graphql.queries
import nmp.graphql.queries

import farming.graphql.mutations
import additional_services.graphql.mutations
import messaging.graphql.mutations
import nmp.graphql.mutations


class Query(core.graphql.queries.Query,
            feed.graphql.queries.Query,
            farming.graphql.queries.Query,
            messaging.graphql.queries.Query,
            weather.graphql.queries.Query,
            additional_services.graphql.queries.Query,
            additional_services.sobloo.graphql.queries.Query,
            nmp.graphql.queries.Query,
            graphene.ObjectType):

    hello = graphene.Field(graphene.String, default_value='Hello!')


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    create_thread = messaging.graphql.mutations.CreateThread.Field()
    update_thread = messaging.graphql.mutations.UpdateThread.Field()
    create_message = messaging.graphql.mutations.CreateMessage.Field()
    add_contact = messaging.graphql.mutations.AddContact.Field()
    remove_contact = messaging.graphql.mutations.RemoveContact.Field()

    update_user_service_subscription = additional_services.graphql.mutations.UpdateUserServiceSubscription.Field()

    add_farm_parcel_to_farm = farming.graphql.mutations.AddFarmParcelToFarm.Field()
    remove_farm_parcel_from_farm = farming.graphql.mutations.RemoveFarmParcelFromFarm.Field()
    update_farm_parcel = farming.graphql.mutations.UpdateFarmParcel.Field()
    update_farm_livestock = farming.graphql.mutations.UpdateFarmLivestock.Field()
    remove_farm_livestock = farming.graphql.mutations.RemoveFarmLivestock.Field()

    create_plan = nmp.graphql.mutations.CreatePlan.Field()
    delete_plan = nmp.graphql.mutations.DeletePlan.Field()
    update_plan = nmp.graphql.mutations.UpdatePlan.Field()

    create_produced_livestock_manure = nmp.graphql.mutations.CreateProducedLivestockManure.Field()
    update_produced_livestock_manure = nmp.graphql.mutations.UpdateProducedLivestockManure.Field()
    delete_produced_livestock_manure = nmp.graphql.mutations.DeleteProducedLivestockManure.Field()

    create_imported_or_exported_livestock_manure = nmp.graphql.mutations.CreateImportedOrExportedLivestockManure.Field()
    update_imported_or_exported_livestock_manure = nmp.graphql.mutations.UpdateImportedOrExportedLivestockManure.Field()
    delete_imported_or_exported_livestock_manure = nmp.graphql.mutations.DeleteImportedOrExportedLivestockManure.Field()

    update_farm_parcel_crop_needs = nmp.graphql.mutations.UpdateFarmParcelCropNeeds.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
