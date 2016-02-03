# coding: utf-8
from main.models import Item
from django.forms import ModelForm
from django import forms

class ItemForm(ModelForm):
	
	class Meta:
 		model = Item
		fields = '__all__'

	