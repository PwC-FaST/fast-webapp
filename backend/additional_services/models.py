"""Models for additional services
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from localized_fields.fields import LocalizedField


class Provider(models.Model):
    """A service provider
    """

    display_name = LocalizedField(_('display name'))

    short_name = LocalizedField(_('short name'))

    website = LocalizedField(_('website'))

    logo = models.ImageField(_('logo'),
                             upload_to='additional_services/providers/logos/%Y/%m/%d/')

    owners = models.ManyToManyField('core.FaSTUser')

    def __str__(self):
        return str(self.display_name)

    class Meta:
        ordering = ('display_name',)


class SubscriptionType(models.Model):
    """A possible subscription type (eg FREE, MONTHLY, etc)
    """

    id = models.CharField(max_length=5, primary_key=True)

    display_name = LocalizedField(_('display name'))

    def __str__(self):
        return str(self.display_name)


class Service(models.Model):
    """A service that a user can opt-in to
    """

    display_name = LocalizedField(_('display name'))

    short_description = LocalizedField(_('short description'))

    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)

    subscription_type = models.ForeignKey(SubscriptionType,
                                          on_delete=models.CASCADE,
                                          default='FREE')

    def __str__(self):
        return str(self.display_name)

    class Meta:
        ordering = ('display_name',)


class UserServiceSubscription(models.Model):
    """A subscription of a service by a user
    """

    user = models.ForeignKey('core.FaSTUser', blank=False, null=False, on_delete=models.CASCADE,
                             related_name='service_subscriptions')
    service = models.ForeignKey(Service, blank=False, null=False, on_delete=models.CASCADE,
                                related_name='user_subscriptions')
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'service'),)
