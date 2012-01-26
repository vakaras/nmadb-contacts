from django.db import models
from django.utils.translation import ugettext as _

from django_db_utils import models as db_models


class HumanInfo(models.Model):
    """ Information about human.
    """

    GENDER_CHOICES = (
            (u'M', _(u'Male')),
            (u'F', _(u'Female')),
            )

    first_name = db_models.FirstNameField()

    last_name = db_models.LastNameField()

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
            )

    identity_code = db_models.IdentityCodeField()

    main_address = models.ForeignKey(
            'Address',
            #limit_choices_to = {'human': self},
            blank=True,
            null=True,
            )

    class Meta(object):
        ordering = [u'last_name', u'first_name',]

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

    class Meta(object):
        ordering = [u'town', u'municipality_type',]

    def __unicode__(self):
        return u'{0.town} {0.municipality_type}: {0.code}'.format(self)


class Address(models.Model):
    """ Address.
    """

    human = models.ForeignKey(
            HumanInfo,
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

    def __unicode__(self):
        return u'{0.human} {0.address}'.format(self)
