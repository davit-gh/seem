# coding: utf-8
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from main.models import Item, ItemCategory
from main.forms import ItemForm, LoginForm, ProfileForm
from django.contrib import messages
from django.contrib.auth import (authenticate, login as auth_login,
                                               logout as auth_logout)
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
def home(request):
	
	#import pdb;pdb.set_trace()
    items = Item.objects.all()
    loginform = LoginForm(prefix="login")
    return render(request,'main/index.html', {'loginform':loginform, 'items':items})

def return_desc(request):
	if request.method == 'POST' and request.is_ajax():
		
		id = request.POST.get('id','')
		item = get_object_or_404(Item, id = id)
		
		return JsonResponse({'desc': item.description, 'title': item.title })

def login_view(request):
	return render(request, 'main/register.html')

def logout(request):
    """
    Log the user out.
    """
    auth_logout(request)
    messages.info(request, "Successfully logged out")
    return redirect('/')

def signup(request, template="main/register.html"):
    """
    Signup form.
    """
    """
    Login form.
    """
    login_form = LoginForm(prefix="login")
    signup_form = ProfileForm()
    if request.method == "POST":
        login_form = LoginForm(request.POST, prefix="login")
        signup_form = ProfileForm(request.POST)
        if not login_form.has_changed() and not request.POST.get("from_popup",False): login_form = LoginForm(prefix="login")
        if not signup_form.has_changed(): signup_form = ProfileForm()
        
        if login_form.is_valid():
            authenticated_user = login_form.save()
            messages.info(request, "Successfully logged in")
            auth_login(request, authenticated_user)
            
            return redirect('/')

        if signup_form.has_changed() and signup_form.is_valid():
            #import pdb;pdb.set_trace()
            new_user = signup_form.save()
            messages.info(request, "Successfully signed up")
            auth_login(request, new_user)
            return redirect("/")
    
    context = {"login_form": login_form, "signup_form": signup_form}
    return render(request, template, context)

def profile(request, pk=None, template='main/profile.html'):
    items = Item.objects.all()
    categories = ItemCategory.objects.all()
    instance = get_object_or_404(Item, pk=pk) if pk else None
    if request.method == 'POST':
        
        form = ItemForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            f=form.save(commit=False)
            f.user = request.user
            f.save()
            items = Item.objects.all()
            messages.info(request, "Դուք ավելացրեցիք ապրանք, շնորհակալություն։")
            return redirect('profile')
    else:
        form = ItemForm()
    
    context = {'form':form, 'items': items, 'categories': categories}
    return render(request, template, context)

@csrf_exempt
def del_prod(request):
    if request.method == "POST" and request.is_ajax():
        prod_id = request.POST.get('prod_id')
        get_object_or_404(Item, pk=prod_id).delete()
        return JsonResponse({'id': prod_id})
    return JsonResponse({'id': 0})