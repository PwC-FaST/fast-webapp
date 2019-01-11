import random

from django.utils import timezone

import graphene
from graphql_jwt.decorators import login_required, staff_member_required

from nmp.graphql.types import PlanType, ImportedOrExportedLivestockManureType, ProducedLivestockManureType, \
    FarmParcelCropNeedsType
from nmp.models import Plan, ProducedLivestockManure, ImportedOrExportedLivestockManure, FarmParcelCropNeeds, \
    FarmParcelNutrientPlanResult

from farming.models import Farm


class CreatePlan(graphene.Mutation):
    class Arguments:
        farm_id = graphene.ID(required=True)
        name = graphene.String(required=False)

    plan = graphene.Field(PlanType)

    @staticmethod
    @login_required
    def mutate(root, info, farm_id, **kwargs):
        user = info.context.user
        farm = Farm.objects.filter(pk=farm_id).get()

        name = kwargs.get('name')

        if not name:
            name = 'Plan %s %s' % (user.username, timezone.now().strftime('%y%m%d%H%M%S'))

        plan = Plan(created_by=user, is_active=False, farm=farm, name=name, updated_by=user, updated_at=timezone.now())
        plan.save()

        # Add the manure for the farm livestock
        for farm_livestock in farm.farm_livestock.all():
            ProducedLivestockManure(
                plan=plan,
                livestock_species=farm_livestock.livestock_species,
                purity=farm_livestock.livestock_species.default_manure_purity,
                nitrogen_content=farm_livestock.livestock_species.default_manure_nitrogen_content,
                phosphorus_content=farm_livestock.livestock_species.default_manure_phosphorus_content,
                potassium_content=farm_livestock.livestock_species.default_manure_potassium_content,
                number_of_heads=farm_livestock.number_of_heads,
                storage_days=farm_livestock.livestock_species.default_manure_storage_days,
                liters_per_head_per_day=farm_livestock.livestock_species.default_manure_liters_per_head_per_day
            ).save()

        # Do not add any import/export

        # Add crop needs for each parcel
        for idx, farm_parcel in enumerate(farm.farm_parcels.all()):
            if farm_parcel.crop_species is not None:
                farm_parcel_crop_needs = FarmParcelCropNeeds(
                    plan=plan,
                    farm_parcel=farm_parcel,
                    target_yield=farm_parcel.crop_species.default_yield_per_hectare,
                    is_active=True,
                    
                    # TODO: compute these based on crop agronomy and soil data
                    estimated_nitrogen_needed=120,  
                    estimated_phosphorus_needed=14,
                    estimated_potassium_needed=25,
                    priority_order=idx + 1)

                farm_parcel_crop_needs.save()

                # Add fake NMP result
                # TODO: implement real NMP algorithms
                manure_quantity = round(random.randint(1500, 4000), -2)
                chemical_quantity = 0 if farm_parcel.farming_commitments.filter(pk='ORG').exists() \
                    else round(random.randint(50, 200), -1)
                chemical_type = '12-4-8' if chemical_quantity > 0 else None

                FarmParcelNutrientPlanResult(
                    farm_parcel_crop_needs=farm_parcel_crop_needs,
                    manure_quantity=manure_quantity,
                    chemical_quantity=chemical_quantity,
                    chemical_type=chemical_type
                ).save()

            else:
                FarmParcelCropNeeds(
                    plan=plan,
                    farm_parcel=farm_parcel,
                    target_yield=None,
                    is_active=False,
                    estimated_nitrogen_needed=None,
                    estimated_phosphorus_needed=None,
                    estimated_potassium_needed=None,
                    priority_order=idx + 1).save()

        return CreatePlan(plan=plan)


class UpdatePlan(graphene.Mutation):
    class Arguments:
        plan_id = graphene.ID(required=True)
        name = graphene.String(required=False)
        is_active = graphene.Boolean(required=False)

    plan = graphene.Field(PlanType)

    @login_required
    def mutate(self, info, plan_id, **kwargs):
        user = info.context.user
        plan = Plan.objects.filter(pk=plan_id).get()

        name = kwargs.get('name')
        is_active = kwargs.get('is_active')

        if name is not None:
            plan.name = name

        if is_active is not None:
            plan.is_active = is_active

        if name is not None or is_active is not None:
            plan.updated_by = user
            plan.updated_at = timezone.now()
            plan.save()

        return UpdatePlan(plan=plan)


class DeletePlan(graphene.Mutation):
    class Arguments:
        plan_id = graphene.ID(required=True)

    plan = graphene.Field(PlanType)

    @staticmethod
    @login_required
    def mutate(root, info, plan_id):
        plan = Plan.objects.filter(pk=plan_id).get()
        plan.delete()

        return DeletePlan(plan=None)


class UpdateProducedLivestockManure(graphene.Mutation):
    class Arguments:
        produced_livestock_manure_id = graphene.ID(required=True)
        livestock_species_id = graphene.ID(required=False)
        number_of_heads = graphene.Int(required=False)
        purity = graphene.Float(required=False)
        nitrogen_content = graphene.Float(required=False)
        phosphorus_content = graphene.Float(required=False)
        potassium_content = graphene.Float(required=False)
        storage_days = graphene.Int(required=False)
        liters_per_head_per_day = graphene.Float(required=False)

    produced_livestock_manure = graphene.Field(ProducedLivestockManureType)

    @login_required
    def mutate(self, info, produced_livestock_manure_id, **kwargs):
        produced_livestock_manure = ProducedLivestockManure.objects.filter(pk=produced_livestock_manure_id)
        produced_livestock_manure.update(**{k: v for k, v in kwargs.items() if k != 'produced_livestock_manure_id'})

        produced_livestock_manure = produced_livestock_manure.get()
        produced_livestock_manure.plan.updated_by = info.context.user
        produced_livestock_manure.plan.updated_at = timezone.now()
        produced_livestock_manure.plan.save()

        return UpdateProducedLivestockManure(produced_livestock_manure=produced_livestock_manure)


class CreateProducedLivestockManure(graphene.Mutation):
    class Arguments:
        plan_id = graphene.ID(required=True)
        livestock_species_id = graphene.ID(required=True)
        number_of_heads = graphene.Int(required=True)
        purity = graphene.Float(required=False, default_value=0.8)  # TODO:
        nitrogen_content = graphene.Float(required=False, default_value=0.0015)  # TODO:
        phosphorus_content = graphene.Float(required=False, default_value=0.0018)  # TODO:
        potassium_content = graphene.Float(required=False, default_value=0.0015)  # TODO:
        storage_days = graphene.Int(required=False, default_value=125)  # TODO:
        liters_per_head_per_day = graphene.Float(required=False, default_value=50)  # TODO:

    produced_livestock_manure = graphene.Field(ProducedLivestockManureType)

    @login_required
    def mutate(self, info, **kwargs):
        produced_livestock_manure = ProducedLivestockManure(**kwargs)
        produced_livestock_manure.save()

        produced_livestock_manure.plan.updated_by = info.context.user
        produced_livestock_manure.plan.updated_at = timezone.now()
        produced_livestock_manure.plan.save()

        return CreateProducedLivestockManure(produced_livestock_manure=produced_livestock_manure)


class DeleteProducedLivestockManure(graphene.Mutation):
    class Arguments:
        produced_livestock_manure_id = graphene.ID(required=True)

    produced_livestock_manure = graphene.Field(ProducedLivestockManureType)

    @login_required
    def mutate(self, info, produced_livestock_manure_id):
        produced_livestock_manure = ProducedLivestockManure.objects.get(pk=produced_livestock_manure_id)
        produced_livestock_manure.delete()

        produced_livestock_manure.plan.updated_by = info.context.user
        produced_livestock_manure.plan.updated_at = timezone.now()
        produced_livestock_manure.plan.save()

        return DeleteProducedLivestockManure(produced_livestock_manure=None)


class UpdateImportedOrExportedLivestockManure(graphene.Mutation):
    class Arguments:
        imported_or_exported_livestock_manure_id = graphene.ID(required=True)
        livestock_species_id = graphene.ID(required=False)
        total_quantity = graphene.Float(required=False)
        purity = graphene.Float(required=False)
        nitrogen_content = graphene.Float(required=False)
        phosphorus_content = graphene.Float(required=False)
        potassium_content = graphene.Float(required=False)

    imported_or_exported_livestock_manure = graphene.Field(ImportedOrExportedLivestockManureType)

    @login_required
    def mutate(self, info, imported_or_exported_livestock_manure_id, **kwargs):
        imported_or_exported_livestock_manure = ImportedOrExportedLivestockManure.objects.filter(
            pk=imported_or_exported_livestock_manure_id)
        imported_or_exported_livestock_manure.update(
            **{k: v for k, v in kwargs.items() if k != 'imported_or_exported_livestock_manure_id'})

        imported_or_exported_livestock_manure = imported_or_exported_livestock_manure.get()
        imported_or_exported_livestock_manure.plan.updated_by = info.context.user
        imported_or_exported_livestock_manure.plan.updated_at = timezone.now()
        imported_or_exported_livestock_manure.plan.save()

        return UpdateImportedOrExportedLivestockManure(
            imported_or_exported_livestock_manure=imported_or_exported_livestock_manure)


class CreateImportedOrExportedLivestockManure(graphene.Mutation):
    class Arguments:
        plan_id = graphene.ID(required=True)
        livestock_species_id = graphene.ID(required=True)
        total_quantity = graphene.Float(required=True)
        purity = graphene.Float(required=False, default_value=0.8)  # TODO:
        nitrogen_content = graphene.Float(required=False, default_value=0.0015)  # TODO:
        phosphorus_content = graphene.Float(required=False, default_value=0.0018)  # TODO:
        potassium_content = graphene.Float(required=False, default_value=0.0015)  # TODO:

    imported_or_exported_livestock_manure = graphene.Field(ImportedOrExportedLivestockManureType)

    @login_required
    def mutate(self, info, **kwargs):
        imported_or_exported_livestock_manure = ImportedOrExportedLivestockManure(**kwargs)
        imported_or_exported_livestock_manure.save()

        imported_or_exported_livestock_manure.plan.updated_by = info.context.user
        imported_or_exported_livestock_manure.plan.updated_at = timezone.now()
        imported_or_exported_livestock_manure.plan.save()

        return CreateImportedOrExportedLivestockManure(
            imported_or_exported_livestock_manure=imported_or_exported_livestock_manure)


class DeleteImportedOrExportedLivestockManure(graphene.Mutation):
    class Arguments:
        imported_or_exported_livestock_manure_id = graphene.ID(required=True)

    imported_or_exported_livestock_manure = graphene.Field(ImportedOrExportedLivestockManureType)

    @login_required
    def mutate(self, info, imported_or_exported_livestock_manure_id):
        imported_or_exported_livestock_manure = ImportedOrExportedLivestockManure.objects.get(
            pk=imported_or_exported_livestock_manure_id)
        imported_or_exported_livestock_manure.delete()

        imported_or_exported_livestock_manure.plan.updated_by = info.context.user
        imported_or_exported_livestock_manure.plan.updated_at = timezone.now()
        imported_or_exported_livestock_manure.plan.save()

        return DeleteImportedOrExportedLivestockManure(imported_or_exported_livestock_manure=None)


class UpdateFarmParcelCropNeeds(graphene.Mutation):
    class Arguments:
        farm_parcel_crop_needs_id = graphene.ID(required=True)
        target_yield = graphene.Float(required=False)
        is_active = graphene.Boolean(required=False)
        priority_order = graphene.Float(required=False)

    farm_parcel_crop_needs = graphene.Field(FarmParcelCropNeedsType)

    @login_required
    def mutate(self, info, farm_parcel_crop_needs_id, **kwargs):
        farm_parcel_crop_needs = FarmParcelCropNeeds.objects.filter(pk=farm_parcel_crop_needs_id)
        farm_parcel_crop_needs.update(**{k: v for k, v in kwargs.items() if k != 'farm_parcel_crop_needs_id'})

        farm_parcel_crop_needs = farm_parcel_crop_needs.get()
        farm_parcel_crop_needs.plan.updated_by = info.context.user
        farm_parcel_crop_needs.plan.updated_at = timezone.now()
        farm_parcel_crop_needs.plan.save()

        return UpdateFarmParcelCropNeeds(farm_parcel_crop_needs=farm_parcel_crop_needs)
