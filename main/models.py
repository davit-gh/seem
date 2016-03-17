# coding: utf-8
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

PERCENTAGE_CHOICES = (
    ('50%', '50%'), 
    ('100%', '100%'), 
)

class Item(models.Model):
    title = models.CharField("Վերնագիր", max_length=120, blank=False)
    user = models.ForeignKey(User, related_name="items")
    description = models.TextField("Նկարագրություն", blank=False)
    featured_image = models.ImageField("Նկար", upload_to="uploads/items", null=True, blank=True) 
    categories = models.ManyToManyField("ItemCategory", 
            verbose_name="Բաժիններ",\
            blank=True, related_name="items")
    percentage = models.CharField("Տոկոսաչափ", max_length=20, blank=False, choices=PERCENTAGE_CHOICES, default='100%')
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"


class ItemImage(models.Model):
    portfolioitem = models.ForeignKey(Item, related_name="images")
    image = models.ImageField(upload_to="uploads/items", null=True, blank=True)
    class Meta:
        verbose_name="Item Image"
        verbose_name_plural="Item Images"


class ItemCategory(models.Model):
    """
    A category for grouping portfolio items into a series.
    """
    category_name = models.CharField(max_length=100, blank=False)
    class Meta:
        verbose_name="Item Category"
        verbose_name_plural="Item Categories"

    def __unicode__(self):
    	return self.category_name