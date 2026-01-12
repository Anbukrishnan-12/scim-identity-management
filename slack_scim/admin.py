from django.contrib import admin
from .models import SlackUser, SlackUserEmail, SlackUserPhoneNumber, SlackUserAddress, SlackUserGroup

class SlackUserEmailInline(admin.TabularInline):
    model = SlackUserEmail
    extra = 1

class SlackUserPhoneNumberInline(admin.TabularInline):
    model = SlackUserPhoneNumber
    extra = 1

class SlackUserAddressInline(admin.StackedInline):
    model = SlackUserAddress
    extra = 1

class SlackUserGroupInline(admin.TabularInline):
    model = SlackUserGroup
    extra = 1

@admin.register(SlackUser)
class SlackUserAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'display_name', 'given_name', 'family_name', 'active', 'created', 'last_modified']
    list_filter = ['active', 'user_type', 'created', 'last_modified']
    search_fields = ['user_name', 'display_name', 'given_name', 'family_name', 'scim_id', 'slack_user_id']
    readonly_fields = ['scim_id', 'created', 'last_modified']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('scim_id', 'external_id', 'user_name', 'display_name', 'nick_name', 'active')
        }),
        ('Name', {
            'fields': ('formatted_name', 'given_name', 'family_name', 'middle_name', 'honorific_prefix', 'honorific_suffix')
        }),
        ('Profile', {
            'fields': ('profile_url', 'title', 'user_type', 'preferred_language', 'locale', 'timezone')
        }),
        ('Slack Integration', {
            'fields': ('slack_user_id', 'team_id')
        }),
        ('Metadata', {
            'fields': ('created', 'last_modified', 'version'),
            'classes': ('collapse',)
        })
    )
    
    inlines = [SlackUserEmailInline, SlackUserPhoneNumberInline, SlackUserAddressInline, SlackUserGroupInline]

@admin.register(SlackUserEmail)
class SlackUserEmailAdmin(admin.ModelAdmin):
    list_display = ['user', 'value', 'type', 'primary']
    list_filter = ['type', 'primary']
    search_fields = ['value', 'user__user_name']

@admin.register(SlackUserPhoneNumber)
class SlackUserPhoneNumberAdmin(admin.ModelAdmin):
    list_display = ['user', 'value', 'type', 'primary']
    list_filter = ['type', 'primary']
    search_fields = ['value', 'user__user_name']

@admin.register(SlackUserAddress)
class SlackUserAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'locality', 'region', 'country', 'primary']
    list_filter = ['type', 'primary', 'country']
    search_fields = ['user__user_name', 'locality', 'region', 'country']

@admin.register(SlackUserGroup)
class SlackUserGroupAdmin(admin.ModelAdmin):
    list_display = ['user', 'value', 'display', 'type']
    list_filter = ['type']
    search_fields = ['user__user_name', 'value', 'display']