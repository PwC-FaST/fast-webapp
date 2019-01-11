from django.db import models as models
from localized_fields.fields import LocalizedField
from django.contrib.auth.models import AbstractUser
from django.utils import six, timezone
from django.utils.translation import ugettext_lazy as _


class FarmingCommitment(models.Model):
    id = models.CharField(max_length=3, unique=True, primary_key=True)
    name = LocalizedField(_('name'))
    available_countries = models.ManyToManyField('core.Country')

    def __str__(self):
        return '%s: %s' % (self.id, str(self.name))

    class Meta:
        ordering = ('id',)


class LivestockSpecies(models.Model):
    parent = models.ForeignKey(to='LivestockSpecies', on_delete=models.CASCADE, verbose_name=_('parent'), null=True,
                               related_name='children')
    icon = models.ImageField(verbose_name=_('icon'), upload_to='farming/livestock_species/icons/%Y/%m/%d/')
    name_singular = LocalizedField(verbose_name=_('name singular'))
    name_plural = LocalizedField(verbose_name=_('name plural'))
    default_manure_purity = models.FloatField()
    default_manure_liters_per_head_per_day = models.FloatField()
    default_manure_nitrogen_content = models.FloatField()
    default_manure_phosphorus_content = models.FloatField()
    default_manure_potassium_content = models.FloatField()
    default_manure_storage_days = models.FloatField()

    class Meta:
        ordering = ('name_singular',)
        verbose_name_plural = "livestock species"

    def __str__(self):
        return str(self.name_plural)


class CropSpecies(models.Model):
    parent = models.ForeignKey('CropSpecies', null=True, on_delete=models.CASCADE, related_name='children')
    name_singular = LocalizedField(_('name singular'))
    name_plural = LocalizedField(_('name plural'))
    name_latin = models.TextField(_('name latin'), null=True)
    default_yield_per_hectare = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ('name_singular',)
        verbose_name_plural = "crop species"

    def __str__(self):
        return str(self.name_plural)


# One farmer is one user, but possibly many farmers for the same farm
class Farmer(models.Model):
    user = models.OneToOneField('core.FaSTUser', on_delete=models.CASCADE, null=False, related_name='farmer')

    def __str__(self):
        return self.user.username


class Farm(models.Model):
    name = models.CharField(_('name'), max_length=255, null=True)
    farmers = models.ManyToManyField(Farmer, blank=True, related_name='farms')

    def __str__(self):
        return self.name


class FarmParcel(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='farm_parcels')
    name = models.CharField(max_length=32, blank=True, null=True)
    lpis_parcel_id = models.CharField(max_length=255, blank=False, null=False)
    farming_commitments = models.ManyToManyField(FarmingCommitment, blank=True, related_name='farm_parcels')
    crop_species = models.ForeignKey(CropSpecies, null=True, blank=True, related_name='farm_parcels', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey('core.FaSTUSer', blank=False, null=False, on_delete=models.CASCADE,
                                 related_name='farm_parcels_added')

    def __str__(self):
        return self.name


class FarmLivestock(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='farm_livestock')
    livestock_species = models.ForeignKey(LivestockSpecies, on_delete=models.PROTECT, related_name='farm_livestock_species')
    number_of_heads = models.IntegerField(blank=False, null=False)
    start_at = models.DateField(blank=True, null=True)
    end_at = models.DateField(blank=True, null=True)

    def __str__(self):
        return '%s (%s)' % (self.livestock_species.name_plural.en, self.farm.name)
