from django.contrib import admin

from right_portion.accounts.models import RPUser

from django.utils.translation import gettext_lazy as _


class RPUserFilter(admin.SimpleListFilter):
    title = _('custom filter')
    parameter_name = 'custom_filter'

    def lookups(self, request, model_admin):
        return (
            ('option1', _('Is employee')),
            ('option2', _('Is staff')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'option1':
            return queryset.filter(is_employee="True")
        if self.value() == 'option2':
            return queryset.filter(is_staff="True")


@admin.register(RPUser)
class RPUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_employee')
    list_filter = [RPUserFilter]
    search_fields = ['username']