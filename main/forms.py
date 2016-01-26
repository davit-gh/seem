from main.models import Item
from django.forms import ModelForm
from django import forms

class ItemForm(ModelForm):
	description = forms.CharField(widget=forms.Textarea )
	class Meta:
 		model = Item
		fields = '__all__'

	