from django.contrib import admin

from nmadb_contacts import models
from nmadb_contacts import forms


class MunicipalityAdmin(admin.ModelAdmin):
    """ Administration for municipality.
    """

    list_display = (
            'id',
            'code',
            'town',
            'municipality_type',
            )

    list_filter = (
            'municipality_type',
            )

    search_fields = (
            'town',
            'code',
            )


class HumanAdmin(admin.ModelAdmin):
    """ Administration for human.
    """

    form = forms.HumanForm

    list_display = (
            'id',
            'first_name',
            'last_name',
            'birth_date',
            )

    list_filter = [
            ]

    search_fields = (
            'first_name',
            'last_name',
            'old_last_name',
            )


admin.site.register(models.Human, HumanAdmin)
admin.site.register(models.Municipality, MunicipalityAdmin)
admin.site.register(models.Address)
admin.site.register(models.Phone)
admin.site.register(models.Email)
admin.site.register(models.InfoForContracts)
admin.site.register(models.Institution)
