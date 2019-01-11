from django.db import models as models
from localized_fields.fields import LocalizedField
from django.contrib.auth.models import AbstractUser
from django.utils import six, timezone
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class Country(models.Model):
    id = models.CharField(max_length=2, unique=True, primary_key=True)
    name = LocalizedField(_('name'))

    def __str__(self):
        return '%s: %s' % (self.id, self.name.en)

    class Meta:
        ordering = ('id',)
        verbose_name_plural = "countries"


# Override the default Django model
class FaSTUser(AbstractUser):
    # from AbstractUser class
    # username = models.CharField(_('username'), max_length=30, unique=True,
    #                             help_text=_('Required. 30 characters or fewer. Letters, digits and '
    #                                         '@/./+/-/_ only.'),
    #                             validators=[
    #                                 validators.RegexValidator(r'^[\w.@+-]+$',
    #                                                           _('Enter a valid username. '
    #                                                             'This value may contain only letters, numbers '
    #                                                             'and @/./+/-/_ characters.'), 'invalid'),
    #                             ],
    #                             error_messages={
    #                                 'unique': _("A user with that username already exists."),
    #                             })
    # first_name = models.CharField(_('first name'), max_length=30, blank=True)
    # last_name = models.CharField(_('last name'), max_length=30, blank=True)
    # email = models.EmailField(_('email address'), blank=True)
    # is_staff = models.BooleanField(_('staff status'), default=False,
    #                                help_text=_('Designates whether the user can log into this admin '
    #                                            'site.'))
    # is_active = models.BooleanField(_('active'), default=True,
    #                                 help_text=_('Designates whether this user should be treated as '
    #                                             'active. Unselect this instead of deleting accounts.'))
    # date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    first_name = models.CharField(_('first name'), max_length=255, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.CASCADE)
    date_last_connection = models.DateTimeField(_('date last connection'), default=timezone.now)
    picture = models.ImageField(_('picture'), blank=True, null=True, upload_to='core/fast_users/pictures/%Y/%m/%d/')
    language = models.CharField(_('language'), max_length=2, choices=settings.LANGUAGES, default='en')

    class Meta:
        ordering = ('username',)
        verbose_name = "FaST user"
        verbose_name_plural = "FaST users"





















