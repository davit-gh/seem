# coding: utf-8
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from main.models import Item, ItemCategory
from main.forms import ItemForm
from django.contrib import messages


def home(request):
	if request.method == 'POST':
		form = ItemForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			messages.info(request, "Դուք ավելացրեցիք ապրանք, շնորհակալություն։")

	form = ItemForm()

	items = Item.objects.all()
	categories = ItemCategory.objects.all()
	#pdb.set_trace()
	return render(request,'main/index.html', {'form': form, 'items': items, 'categories': categories})

def return_desc(request):
	if request.method == 'POST' and request.is_ajax():
		
		id = request.POST.get('id','')
		item = get_object_or_404(Item, id = id)
		
		return JsonResponse({'desc': item.description, 'title': item.title })

