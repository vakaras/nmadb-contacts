from django.contrib import admin
from django.utils.translation import ugettext as _

from django_db_utils import utils as db_utils
from nmadb_contacts import models
from nmadb_contacts import forms
from nmadb_utils import admin as utils


class MunicipalityAdmin(utils.ModelAdmin):
    """ Administration for municipality.
    """

    list_display = (
            'id',
            'title',
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


class AddressAdmin(utils.ModelAdmin):
    """ Administration for addresses.
    """

    list_display = (
            'id',
            'human',
            'town',
            'address',
            'municipality',
            )

    search_fields = (
            'town',
            'address',
            'human__first_name',
            'human__last_name',
            'human__old_last_name',
            )

    sheet_mapping = (
            (_(u'ID'), ('id',)),
            (_(u'First name'), ('human', 'first_name',)),
            (_(u'Last name'), ('human', 'last_name',)),
            (_(u'Old last name'), ('human', 'old_last_name',)),
            (_(u'Town'), ('town',)),
            (_(u'Address'), ('address',)),
            (_(u'Municipality'), ('municipality', 'title',)),
            )


class ContactAdmin(utils.ModelAdmin):
    """ Administration for contacts.
    """

    list_display = (
            'id',
            'human',
            'last_time_used',
            'used',
            )

    search_fields = (
            'human__first_name',
            'human__last_name',
            'human__old_last_name',
            )

    sheet_mapping = (
            (_(u'ID'), ('id',)),
            (_(u'First name'), ('human', 'first_name',)),
            (_(u'Last name'), ('human', 'last_name',)),
            (_(u'Old last name'), ('human', 'old_last_name',)),
            (_(u'Last time used'), ('last_time_used',)),
            (_(u'Used'), ('used',)),
            )


class PhoneAdmin(ContactAdmin):
    """ Administration for phones.
    """

    list_display = ContactAdmin.list_display + (
            'number',
            )

    search_fields = ContactAdmin.search_fields + (
            'number',
            )

    sheet_mapping = ContactAdmin.sheet_mapping + (
            (_(u'Phone number'), ('number',)),
            )


class EmailAdmin(ContactAdmin):
    """ Administration for emails.
    """

    list_display = ContactAdmin.list_display + (
            'address',
            )

    search_fields = ContactAdmin.search_fields + (
            'address',
            )

    sheet_mapping = ContactAdmin.sheet_mapping + (
            (_(u'E-Mail address'), ('address',)),
            )


class InfoForContractsAdmin(utils.ModelAdmin):
    """ Administration for info for contracts.
    """

    list_display = (
            'id',
            'human',
            'identity_card_number',
            'identity_card_delivery_place',
            'identity_card_delivery_date',
            'social_insurance_number',
            'bank_account',
            'bank',
            )

    search_fields = (
            'human__first_name',
            'human__last_name',
            'human__old_last_name',
            )


class InstitutionAdmin(utils.ModelAdmin):
    """ Administration for institutions.
    """

    list_display = (
            'id',
            'human',
            'title',
            )

    search_fields = (
            'human__first_name',
            'human__last_name',
            'human__old_last_name',
            'title',
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


class HumanAdmin(utils.ModelAdmin):
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

    sheet_mapping = (
            (_(u'ID'), ('id',)),
            (_(u'First name'), ('first_name',)),
            (_(u'Last name'), ('last_name',)),
            (_(u'Old last name'), ('old_last_name',)),
            (_(u'Gender'), ('get_gender_display',)),
            (_(u'Academic degree'), ('academic_degree',)),
            (_(u'Birth date'), ('birth_date',)),
            (_(u'Identity code'), ('identity_code',)),
            (_(u'Main address'), ('main_address',)),
            )

    list_max_show_all = 100
    list_per_page = 10

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

        return db_utils.join(obj.phone_set.exclude(used=False), 'number')
    get_phones.short_description = _("Phone numbers")

    def get_emails(self, obj):
        """ Returns concatenation of all used emails.
        """

        return db_utils.join(obj.email_set.exclude(used=False), 'address')
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
admin.site.register(models.Address, AddressAdmin)
admin.site.register(models.Phone, PhoneAdmin)
admin.site.register(models.Email, EmailAdmin)
admin.site.register(models.InfoForContracts, InfoForContractsAdmin)
admin.site.register(models.Institution, InstitutionAdmin)
