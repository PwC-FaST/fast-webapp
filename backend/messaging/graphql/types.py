from graphene_django.types import DjangoObjectType
import graphene
from graphql_jwt.decorators import login_required

from messaging.models import Thread, Message, Contact


class ThreadType(DjangoObjectType):
    class Meta:
        model = Thread


class MessageType(DjangoObjectType):
    class Meta:
        model = Message


class ContactType(DjangoObjectType):
    class Meta:
        model = Contact

    is_in_my_contacts = graphene.Boolean()

    @login_required
    def resolve_is_in_my_contacts(self, info):
        return self in info.context.user.contact.contacts.all()

