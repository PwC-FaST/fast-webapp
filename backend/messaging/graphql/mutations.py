import graphene
from django.utils import timezone
from graphene_file_upload.scalars import Upload
from graphql_jwt.decorators import login_required
import core.models

from messaging.models import Thread, Message, Contact
from messaging.graphql.types import ThreadType, MessageType, ContactType


class CreateThread(graphene.Mutation):
    class Arguments:
        created_by = graphene.String(required=True)
        created_at = graphene.DateTime(required=True)
        members = graphene.List(graphene.NonNull(graphene.String), required=False)
        subject = graphene.String(required=False)

    thread = graphene.Field(ThreadType)

    @staticmethod
    @login_required
    def mutate(root, info, created_by, created_at, members, subject):
        # Create the Thread object in Django
        created_by = core.models.FaSTUser.objects.get(username=created_by)

        # If the user creating the thread is not part of the members, force him in
        if info.context.user not in members:
            members += [info.context.user.username]

        # Get the members pbject
        members = core.models.FaSTUser.objects.filter(username__in=members)

        # Create the thread
        thread = Thread(created_by=created_by, created_at=created_at, subject=subject)
        thread.save()
        thread.members.set(members)

        return CreateThread(thread=thread)


class UpdateThread(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        members = graphene.List(graphene.NonNull(graphene.String), required=False)
        subject = graphene.String(required=False)

    thread = graphene.Field(ThreadType)

    @staticmethod
    @login_required
    def mutate(root, info, id, **kwargs):

        thread = Thread.objects.get(pk=id)
        if 'members' in kwargs:
            members = core.models.FaSTUser.objects.filter(username__in=kwargs['members'])
            thread.members.set(members)
        if 'subject' in kwargs:
            thread.subject = kwargs['subject']
            thread.save()

        return UpdateThread(thread=thread)


class CreateMessage(graphene.Mutation):
    message = graphene.Field(MessageType)

    class Arguments:
        thread_id = graphene.Int(required=True)
        content = graphene.String(required=True)
        attachment = Upload(required=False)

    @staticmethod
    @login_required
    def mutate(root, info, thread_id, content, attachment=None):

        thread = Thread.objects.filter(pk=thread_id)
        thread = thread.filter(members=info.context.user).get()
        created_by = info.context.user
        created_at = timezone.now()
        message = Message(thread=thread, created_by=created_by, created_at=created_at,
                          content=content, attachment=attachment)
        message.save()

        return CreateMessage(message=message)


class AddContact(graphene.Mutation):

    class Arguments:
        contact_id = graphene.ID(required=True)

    contact = graphene.Field(ContactType)

    @staticmethod
    @login_required
    def mutate(root, info, contact_id):
        user = info.context.user
        contact = Contact.objects.get(pk=contact_id)
        if contact not in user.contact.contacts.all():
            user.contact.contacts.add(contact)
        return AddContact(contact=contact)


class RemoveContact(graphene.Mutation):

    class Arguments:
        contact_id = graphene.ID(required=True)

    contact = graphene.Field(ContactType)

    @staticmethod
    @login_required
    def mutate(root, info, contact_id):
        user = info.context.user
        contact = Contact.objects.get(pk=contact_id)
        if contact in user.contact.contacts.all():
            user.contact.contacts.remove(contact)
        return AddContact(None)
