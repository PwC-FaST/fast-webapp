from django.contrib import admin

from nmp.models import (Plan, ProducedLivestockManure, ImportedOrExportedLivestockManure, FarmParcelCropNeeds,
                        FarmParcelNutrientPlanResult)


class ProducedLivestockManureInline(admin.TabularInline):
    model = ProducedLivestockManure
    extra = 0


class ImportedOrExportedLivestockManureInline(admin.TabularInline):
    model = ImportedOrExportedLivestockManure
    extra = 0


class FarmParcelCropNeedsInline(admin.TabularInline):
    model = FarmParcelCropNeeds
    extra = 0


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    inlines = [ProducedLivestockManureInline, ImportedOrExportedLivestockManureInline, FarmParcelCropNeedsInline]

