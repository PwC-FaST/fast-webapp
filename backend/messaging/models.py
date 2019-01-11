from django.db import models as models
from localized_fields.fields import LocalizedField
from django.utils import six, timezone
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from core.models import FaSTUser


class Thread(models.Model):
    created_by = models.ForeignKey('core.FaSTUser', on_delete=models.CASCADE, related_name='threads_started')
    created_at = models.DateTimeField(auto_now_add=True)

    members = models.ManyToManyField('core.FaSTUser')
    subject = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.subject


class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField(max_length=1024, blank=True, null=True)
    attachment = models.FileField(upload_to='messaging/attachments/%Y/%m/%d', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('core.FaSTUser', on_delete=models.CASCADE, related_name='messages_created')

    class Meta:
        ordering = ('-created_at',)

    def delete(self, using=None, keep_parents=False):
        self.attachment.delete()
        super().delete()

    def clean(self):
        if self.content is None and self.attachment is None:
            raise ValidationError('A message must have at least a content text or an attachment')


class Contact(models.Model):
    user = models.OneToOneField(FaSTUser, on_delete=models.CASCADE, related_name='contact', unique=True)
    contacts = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username
