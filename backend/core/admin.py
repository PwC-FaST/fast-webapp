from django.contrib import admin
from .models import *

from localized_fields.admin import LocalizedFieldsAdminMixin
from additional_services.admin import UserServiceSubscriptionInline


@admin.register(Country)
class CountryAdmin(LocalizedFieldsAdminMixin, admin.ModelAdmin):
    pass


@admin.register(FaSTUser)
class FaSTUserAdmin(LocalizedFieldsAdminMixin, admin.ModelAdmin):
    search_fields = ('username', 'first_name', 'last_name', 'email')

    inlines = [UserServiceSubscriptionInline]
