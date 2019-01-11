"""Admin for additional services
"""

from django.contrib import admin
from localized_fields.admin import LocalizedFieldsAdminMixin

from .models import Service, SubscriptionType, Provider, UserServiceSubscription


@admin.register(Service)
class ServiceAdmin(LocalizedFieldsAdminMixin, admin.ModelAdmin):
    pass


@admin.register(SubscriptionType)
class SubscriptionTypeAdmin(LocalizedFieldsAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Provider)
class ProviderAdmin(LocalizedFieldsAdminMixin, admin.ModelAdmin):
    pass


@admin.register(UserServiceSubscription)
class UserServiceAdmin(admin.ModelAdmin):
    pass


class UserServiceSubscriptionInline(admin.TabularInline):
    model = UserServiceSubscription
    extra = 0
