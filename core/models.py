from django.db import models


class ImmunizationVaccineCodes(models.Model):
    vaccine_code = models.CharField(max_length=20, blank=True, null=True)
    vaccine_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'immunization_vaccine_codes'


class ImmunizationLegalEntitiesInfo(models.Model):
    legal_entities_info = models.CharField(max_length=20, blank=True, null=True)
    vaccine_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'immunization_legal_entities_info'


class ImmunizationCovid192021(models.Model):
    immunization_covid19_2021 = models.CharField(max_length=20, blank=True, null=True)
    vaccine_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'immunization_covid19_2021'
