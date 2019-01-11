from django.db import models

from core.models import FaSTUser

from farming.models import LivestockSpecies, Farm, FarmParcel


class Plan(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    created_by = models.ForeignKey(FaSTUser, blank=False, null=False, related_name='nmp_plans_created',
                                   on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    updated_by = models.ForeignKey(FaSTUser, blank=False, null=False, related_name='nmp_plans_updated',
                                   on_delete=models.CASCADE)

    farm = models.ForeignKey(Farm, blank=False, null=False, related_name='nmp_plans', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False, null=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ProducedLivestockManure(models.Model):
    plan = models.ForeignKey(Plan, null=False, blank=False, related_name='produced_livestock_manures',
                             on_delete=models.CASCADE)
    livestock_species = models.ForeignKey(LivestockSpecies, null=False, blank=False, related_name='produced_livestock_manures',
                                          on_delete=models.CASCADE)
    purity = models.FloatField(blank=False, null=False)
    nitrogen_content = models.FloatField(blank=False, null=False)
    phosphorus_content = models.FloatField(blank=False, null=False)
    potassium_content = models.FloatField(blank=False, null=False)
    number_of_heads = models.IntegerField(blank=False, null=False)
    storage_days = models.IntegerField(blank=False, null=False)
    liters_per_head_per_day = models.FloatField(blank=False, null=False)


class ImportedOrExportedLivestockManure(models.Model):
    plan = models.ForeignKey(Plan, null=False, blank=False, related_name='imported_or_exported_livestock_manures',
                             on_delete=models.CASCADE)
    livestock_species = models.ForeignKey(LivestockSpecies, null=False, blank=False, related_name='imported_or_exported_livestock_manures',
                                          on_delete=models.CASCADE)
    purity = models.FloatField(blank=False, null=False)
    nitrogen_content = models.FloatField(blank=False, null=False)
    phosphorus_content = models.FloatField(blank=False, null=False)
    potassium_content = models.FloatField(blank=False, null=False)
    total_quantity = models.FloatField(blank=False, null=False)


class FarmParcelCropNeeds(models.Model):
    plan = models.ForeignKey(Plan, null=False, blank=False, related_name='farm_parcel_crop_needs',
                             on_delete=models.CASCADE)
    farm_parcel = models.ForeignKey(FarmParcel, null=False, blank=False, related_name='crop_needs',
                                    on_delete=models.CASCADE)
    target_yield = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)
    estimated_nitrogen_needed = models.FloatField(null=True, blank=True)
    estimated_phosphorus_needed = models.FloatField(null=True, blank=True)
    estimated_potassium_needed = models.FloatField(null=True, blank=True)
    priority_order = models.FloatField(null=True, blank=True)


class FarmParcelNutrientPlanResult(models.Model):
    farm_parcel_crop_needs = models.OneToOneField(FarmParcelCropNeeds, null=False, blank=False,
                                                  related_name='nutrient_plan_result', on_delete=models.CASCADE)
    manure_quantity = models.FloatField(null=False, blank=False, default=0)
    chemical_quantity = models.FloatField(null=False, blank=False, default=0)
    chemical_type = models.CharField(max_length=25, null=True, blank=True)
