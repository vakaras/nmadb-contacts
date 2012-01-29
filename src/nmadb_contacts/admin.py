from django.contrib import admin
from django.utils.translation import ugettext as _

from django_db_utils import utils
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


class EmailInline(admin.TabularInline):
    """ Inline email administration.
    """

    model = models.Email

    extra = 0


class PhoneInline(admin.TabularInline):
    """ Inline phone administration.
    """

    model = models.Phone

    extra = 0


class AddressInline(admin.TabularInline):
    """ Inline address administration.
    """

    model = models.Address

    extra = 0


class InstitutionInline(admin.TabularInline):
    """ Inline institution administration.
    """

    model = models.Institution

    extra = 0


class InfoForContractsInline(admin.StackedInline):
    """ Inline information for contracts administration.
    """

    model = models.InfoForContracts

    extra = 0


class HumanAdmin(admin.ModelAdmin):
    """ Administration for human.
    """

    form = forms.HumanForm

    list_display = (
            'id',
            'first_name',
            'last_name',
            'birth_date',
            'get_address',
            'get_phones',
            'get_emails',
            'has_contracts_information',
            )

    list_filter = [
            ]

    search_fields = (
            'first_name',
            'last_name',
            'old_last_name',
            )

    inlines = [
            EmailInline,
            PhoneInline,
            AddressInline,
            InfoForContractsInline,
            ]

    actions = [
            'download_selected',
            ]

    def get_address(self, obj):
        """ Returns main address, address column value.
        """

        if obj.main_address:
            return obj.main_address.address
        else:
            return u''
    get_address.short_description = _("Main address")

    def get_phones(self, obj):
        """ Returns concatenation of all used phone numbers.
        """

        return utils.join(obj.phone_set.exclude(used=False), 'number')
    get_phones.short_description = _("Phone numbers")

    def get_emails(self, obj):
        """ Returns concatenation of all used emails.
        """

        return utils.join(obj.email_set.exclude(used=False), 'address')
    get_emails.short_description = _("Email addresses")

    def has_contracts_information(self, obj):
        """ Returns if this human has contract information.
        """

        try:
            return obj.infoforcontracts and True
        except models.InfoForContracts.DoesNotExist:
            return False
    has_contracts_information.short_description = _("Contract info")
    has_contracts_information.boolean = True

    def download_selected(self, request, queryset):
        """ Generates ODS from queryset for download.
        """
        return utils.download_query(
                queryset, u'ODS',
                merge_rules=('nmadb_contacts:infoforcontracts',),
                join_rules=(
                    ('number', 'nmadb_contacts:phone',
                        ({}, {'used': False})),
                    ('address', 'nmadb_contacts:email',
                        ({}, {'used': False})),
                    )
                )
    download_selected.short_description = _(u'Download selected (ODS)')


admin.site.register(models.Human, HumanAdmin)
admin.site.register(models.Municipality, MunicipalityAdmin)
admin.site.register(models.Address)
admin.site.register(models.Phone)
admin.site.register(models.Email)
admin.site.register(models.InfoForContracts)
admin.site.register(models.Institution)
