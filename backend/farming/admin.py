from django.contrib import admin
from .models import *

from localized_fields.admin import LocalizedFieldsAdminMixin


@admin.register(FarmingCommitment)
class FarmingCommitmentAdmin(LocalizedFieldsAdminMixin, admin.ModelAdmin):
    search_fields = ['id', 'name']


class LivestockSpeciesInline(admin.StackedInline):
    model = LivestockSpecies
    extra = 0


@admin.register(LivestockSpecies)
class LivestockSpeciesAdmin(LocalizedFieldsAdminMixin, admin.ModelAdmin):
    list_display = ('__str__', 'parent')
    autocomplete_fields = ('parent',)
    search_fields = ('name_singular', 'name_plural')

    inlines = [LivestockSpeciesInline]


@admin.register(CropSpecies)
class CropSpeciesAdmin(LocalizedFieldsAdminMixin, admin.ModelAdmin):
    pass


"""
Farmers
"""


@admin.register(Farmer)
class FarmerAdmin(LocalizedFieldsAdminMixin, admin.ModelAdmin):
    pass

"""
Farms
"""


class FarmParcelInline(admin.TabularInline):
    model = FarmParcel
    extra = 0
    autocomplete_fields = ('farming_commitments',)


class FarmLivestockInline(admin.TabularInline):
    model = FarmLivestock
    extra = 0


@admin.register(Farm)
class FarmAdmin(LocalizedFieldsAdminMixin, admin.ModelAdmin):
    inlines = [FarmParcelInline, FarmLivestockInline]


@admin.register(FarmLivestock)
class FarmLivestockAdmin(LocalizedFieldsAdminMixin, admin.ModelAdmin):
    pass
