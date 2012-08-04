from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_db_utils import models as db_models


class Human(models.Model):
    """ Information about human.
    """

    GENDER_CHOICES = (
            (u'M', _(u'Male')),
            (u'F', _(u'Female')),
            )

    first_name = db_models.FirstNameField()

    last_name = db_models.LastNameField()

    old_last_name = db_models.LastNameField(
            verbose_name=_(u'Old last name'),
            blank=True,
            )

    gender = models.CharField(
            max_length=2,
            choices=GENDER_CHOICES,
            )

    academic_degree = models.CharField(
            max_length=45,
            blank=True,
            )

    birth_date = models.DateField(
            blank=True,
            null=True,
            verbose_name=_(u'birth date'),
            )

    identity_code = db_models.IdentityCodeField(
            blank=True,
            null=True,
            unique=True,
            )

    main_address = models.ForeignKey(
            'Address',
            #limit_choices_to = FIXME
            blank=True,
            null=True,
            related_name='+',
            )

    class Meta(object):
        ordering = [u'last_name', u'first_name',]
        verbose_name = _(u'Human')
        verbose_name_plural = _(u'Humans')

    def __unicode__(self):
        return u'{0.id} {0.first_name} {0.last_name}'.format(self)


class Municipality(models.Model):
    """ Information about municipality.
    """

    MUNICIPALITY_TYPES = (
            (u'T', _(u'town')),
            (u'D', _(u'district')),
            )

    town = models.CharField(
            max_length=45,
            )

    municipality_type = models.CharField(
            max_length=2,
            choices=MUNICIPALITY_TYPES,
            blank=True,
            )

    code = models.PositiveSmallIntegerField()

    def title(self):
        """ Return generated title of municipality.
        """

        if self.municipality_type:
            return u'{0} {1}'.format(
                    self.town, self.get_municipality_type_display())
        else:
            return self.town

    class Meta(object):
        ordering = [u'town', u'municipality_type',]
        verbose_name = _(u'municipality')
        verbose_name_plural = _(u'municipalities')

    def __unicode__(self):
        return u'{0}: {1}'.format(self.title(), self.code)


class Address(models.Model):
    """ Address.
    """

    human = models.ForeignKey(
            Human,
            verbose_name=_(u'human'),
            )

    town = models.CharField(
            max_length=45,
            )

    address = models.CharField(
            max_length=90,
            )

    municipality = models.ForeignKey(
            Municipality,
            blank=True,
            null=True,
            )

    class Meta(object):
        ordering = [u'municipality',]
        verbose_name = _(u'address')
        verbose_name_plural = _(u'addresses')

    def __unicode__(self):
        return u'{0.address}'.format(self)


class Contact(models.Model):
    """ Base contact information.
    """

    human = models.ForeignKey(
            Human,
            )

    last_time_used = models.DateTimeField(
            blank=True,
            null=True,
            )

    used = models.NullBooleanField(
            blank=True,
            null=True,
            help_text="If this contact is still used.",
            )

    class Meta(object):
        abstract = True
        ordering = [u'human',]


class Phone(Contact):
    """ Phone number.
    """

    number = db_models.PhoneNumberField(
            unique=True,
            )

    class Meta(object):
        verbose_name = _(u'Phone')
        verbose_name_plural = _(u'Phones')

    def __unicode__(self):
        return u'{0.human} {0.number}'.format(self)


class Email(Contact):
    """ Phone number.
    """

    address = models.EmailField(
            max_length=128,
            unique=True,
            )

    class Meta(object):
        verbose_name = _(u'Email')
        verbose_name_plural = _(u'Emails')

    def __unicode__(self):
        return u'{0.human} {0.address}'.format(self)


class InfoForContracts(models.Model):
    """ Information needed for contracts with human.
    """

    human = models.OneToOneField(
            Human,
            )

    identity_card_number = models.CharField(
            max_length=20,
            blank=True,
            null=True,
            )

    identity_card_delivery_place = models.CharField(
            max_length=45,
            blank=True,
            null=True,
            )

    identity_card_delivery_date = models.DateField(
            blank=True,
            null=True,
            )

    social_insurance_number = models.CharField(
            max_length=20,
            blank=True,
            null=True,
            )

    bank_account = models.CharField(
            max_length=30,
            blank=True,
            null=True,
            )

    bank = models.CharField(
            max_length=90,
            blank=True,
            null=True,
            )

    class Meta(object):
        ordering = [u'human']
        verbose_name = _('Information for contracts')
        verbose_name_plural = _('Informations for contracts')

    def __unicode__(self):
        return u'{0.human}'.format(self)


class Institution(models.Model):
    """ Institution, to which a human belongs.
    """

    human = models.ForeignKey(
            Human,
            )

    title = models.CharField(
            max_length=128,
            )

    class Meta(object):
        ordering = [u'title',]
        verbose_name = _(u'Institution')
        verbose_name_plural = _(u'Institutions')

    def __unicode__(self):
        return u'{0.human} {0.title}'.format(self)
