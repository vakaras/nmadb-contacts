from django.contrib import admin
from django.utils.translation import ugettext as _

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

        return u'; '.join([
            phone.number
            for phone in obj.phone_set.exclude(used=False)
            ])
    get_phones.short_description = _("Phone numbers")

    def get_emails(self, obj):
        """ Returns concatenation of all used emails.
        """

        return u'; '.join([
            email.address
            for email in obj.email_set.exclude(used=False)
            ])
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


admin.site.register(models.Human, HumanAdmin)
admin.site.register(models.Municipality, MunicipalityAdmin)
admin.site.register(models.Address)
admin.site.register(models.Phone)
admin.site.register(models.Email)
admin.site.register(models.InfoForContracts)
admin.site.register(models.Institution)
