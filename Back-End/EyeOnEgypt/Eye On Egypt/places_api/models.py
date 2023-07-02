# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Category(models.Model):
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'category'


class Place(models.Model):
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location_link = models.TextField(blank=True, null=True)
    photo1 = models.TextField(blank=True, null=True)
    photo2 = models.TextField(blank=True, null=True)
    photo3 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'place'
