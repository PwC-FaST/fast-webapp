import graphene
from django.db.models import Q
from graphql_jwt.decorators import login_required
from django.db.models import Max
from django.db.models import OuterRef, Subquery, Prefetch

from messaging.models import Thread, Message, Contact
from messaging.graphql.types import ThreadType, ContactType


class Query(object):
    threads = graphene.Field(graphene.List(ThreadType))

    thread = graphene.Field(ThreadType,
                            thread_id=graphene.Argument(graphene.Int, required=True))

    my_contacts = graphene.List(ContactType)

    contacts = graphene.List(ContactType)

    contact = graphene.Field(ContactType,
                             contact_id=graphene.Argument(graphene.ID, required=True))

    @login_required
    def resolve_threads(self, info):
        threads = Thread.objects.filter(members=info.context.user)
        threads = threads.annotate(Max('messages__created_at')).order_by('-messages__created_at__max')

        messages_queryset = Message.objects.filter(thread__id=OuterRef('thread__id')).order_by('-created_at')
        messages_queryset = messages_queryset.values_list('id', flat=True)[:1]
        messages_queryset = Message.objects.filter(id__in=Subquery(messages_queryset))

        return threads.prefetch_related(Prefetch('messages', messages_queryset))

    @login_required
    def resolve_thread(self, info, thread_id):
        try:
            thread = Thread.objects.filter(pk=thread_id)
            thread = thread.filter(members=info.context.user)
            thread = thread.get()
            return thread
        except:
            return None

    @login_required
    def resolve_my_contacts(self, info):
        contact = Contact.objects.filter(user=info.context.user).get()
        contacts = Contact.objects.filter(Q(user=info.context.user) | Q(contacts=contact))
        contacts = contacts.distinct().exclude(pk=contact.id).all()
        return contacts

    @login_required
    def resolve_contacts(self, info):
        contacts = Contact.objects
        return contacts.filter(user__is_active=True).all()

    @login_required
    def resolve_contact(self, info, contact_id):
        return Contact.objects.get(pk=int(contact_id))
