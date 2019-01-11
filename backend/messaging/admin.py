from django.contrib import admin
from django.forms import Textarea
from django.db import models

from .models import Thread, Message, Contact


class MessageAdmin(admin.ModelAdmin):
    autocomplete_fields = ('created_by', )
    readonly_fields = ('created_at',)

admin.site.register(Message, MessageAdmin)


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    fields = ('created_by', 'content', 'attachment', 'created_at')
    readonly_fields = ('created_at',)

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 60})}
    }


class ThreadAdmin(admin.ModelAdmin):
    autocomplete_fields = ('created_by', 'members',)
    inlines = [MessageInline]


admin.site.register(Thread, ThreadAdmin)


class ContactAdmin(admin.ModelAdmin):
    autocomplete_fields = ('user', 'contacts',)
    search_fields = ['user__username', 'user__first_name', 'user__last_name']

admin.site.register(Contact, ContactAdmin)
