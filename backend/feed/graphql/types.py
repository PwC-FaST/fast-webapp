import graphene

from messaging.graphql.types import ThreadType
from core.graphql.types import FaSTUserType
from farming.graphql.types.farm import FarmParcelType
from additional_services.graphql.types import ServiceType

from additional_services.models import Service

class FeedItemInterface(graphene.Interface):
    id = graphene.ID()
    timestamp = graphene.DateTime()
    timegroup = graphene.String()
    component = graphene.String()
    service = graphene.Field(ServiceType)


class WeatherForecastFeedItemType(graphene.ObjectType):
    class Meta:
        interfaces = (FeedItemInterface,)

    def resolve_component(self, info):
        return 'WeatherForecastFeedBlock'

    def resolve_id(self, info):
        return hash((self.timestamp, self.component))


class MessagingNewMessagesInThreadFeedItemType(graphene.ObjectType):
    class Meta:
        interfaces = (FeedItemInterface,)

    thread = graphene.Field(ThreadType)
    number_of_new_messages = graphene.Int()
    authors_of_new_messages = graphene.List(FaSTUserType)

    def resolve_component(self, info):
        return 'MessagingNewMessagesInThreadFeedBlock'

    def resolve_id(self, info):
        return hash((self.timestamp, self.component, self.thread.id))


class MessagingNewThreadFeedItemType(graphene.ObjectType):
    class Meta:
        interfaces = (FeedItemInterface,)

    thread = graphene.Field(ThreadType)
    number_of_new_messages = graphene.Int()

    def resolve_component(self, info):
        return 'MessagingNewThreadFeedBlock'

    def resolve_id(self, info):
        return hash((self.timestamp, self.component, self.thread.id))


class FarmingFarmParcelAddedToFarmFeedItemType(graphene.ObjectType):
    class Meta:
        interfaces = (FeedItemInterface,)

    farm_parcel = graphene.Field(FarmParcelType)

    def resolve_component(self, info):
        return 'FarmingFarmParcelAddedToFarmFeedBlock'

    def resolve_id(self, info):
        return hash((self.timestamp, self.component, self.farm_parcel.id))


class NMPTodoFromTodoListFeedItemType(graphene.ObjectType):
    class Meta:
        interfaces = (FeedItemInterface,)

    def resolve_component(self, info):
        return 'NMPTodoFromTodoListFeedBlock'


class GenericOneButtonFeedItemType(graphene.ObjectType):
    class Meta:
        interfaces = (FeedItemInterface,)

    header = graphene.String()
    text = graphene.String()
    button_text = graphene.String()
    button_href = graphene.String()

    @staticmethod
    def resolve_component(self, info):
        return 'GenericOneButtonFeedBlock'

    def resolve_id(self, info):
        return hash((self.timestamp, self.component, self.text, self.button_text, self.button_href))


class ServicesSatelliteImageryFeedItemType(graphene.ObjectType):
    class Meta:
        interfaces = (FeedItemInterface,)

    band = graphene.String()
    title = graphene.String()
    color_scale = graphene.String()
    date = graphene.String()

    def resolve_component(self, info):
        return 'ServicesSatelliteImageryFeedBlock'

    def resolve_service(self, info):
        return Service.objects.get(pk=2)  # hard-coded as per init/ fixtures

    def resolve_id(self, info):
        return hash((self.timestamp, self.component, self.band, self.date))


class ServicesSoblooSatelliteImageryFeedItemType(graphene.ObjectType):
    class Meta:
        interfaces = (FeedItemInterface,)

    def resolve_component(self, info):
        return 'ServicesSoblooSatelliteImageryFeedBlock'

    def resolve_service(self, info):
        return Service.objects.get(pk=7)

    def resolve_id(self, info):
        return hash((self.timestamp, self.component))


class FeedItemType(graphene.Union):
    class Meta:
        types = (WeatherForecastFeedItemType,
                 MessagingNewMessagesInThreadFeedItemType,
                 MessagingNewThreadFeedItemType,
                 FarmingFarmParcelAddedToFarmFeedItemType,
                 NMPTodoFromTodoListFeedItemType,
                 GenericOneButtonFeedItemType,
                 ServicesSatelliteImageryFeedItemType,
                 ServicesSoblooSatelliteImageryFeedItemType)
