import json
from wsgiref import headers
from django.shortcuts import render,redirect
from django.urls import reverse
import requests
from django.conf import settings
#from shop.authentication import KeycloakAuthentication
from . models import *
from django.contrib import messages
from shop.form import CustomUserForm
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from jose import jwt
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

# for keycloak
from rest_framework.response import Response
from rest_framework import status
from keycloak.exceptions import KeycloakAuthenticationError,KeycloakError,KeycloakGetError
from rest_framework.decorators import api_view, permission_classes
from .keycloak_service import KeycloakService
#from rest_framework.permissions import IsAuthenticated
#from rest_framework.views import APIView 
#from .keycloak_service import get_user_info
# from keycloak import KeycloakOpenID
#from keycloak import KeycloakAdmin



# Create your views here.
def login_page(request):
    if request.user.is_authenticated:
        return redirect("/shop/home")
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Logged in successfully.")
            return redirect("/shop/home")
        else:
            messages.error(request,"Invalid Username or Password")
            return redirect("/login")
    return render(request,"login.html")

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logout Successfull.")
    return redirect("/shop/home")

def home(request):
    product=Product.objects.filter(trending=1)
    id_token = request.session.get('id_token') #keycloak improvement
    return render(request,'shop/index.html',{'product':product,'id_token': id_token})

# def register(request):
#     form = CustomUserForm()
#     if request.method=="POST":
#         form = CustomUserForm(request.POST)
#         if(form.is_valid()):
#             form.save()
#             messages.success(request,"Registration Success.You can login now..!")
#             return redirect('login')
#     return render(request,'shop/register.html',{'form':form})

def collections(request):
    category=Category.objects.filter(status=0)
    return render(request,"shop/collections.html",{"category":category})

def collections_view(request,name):
    if(Category.objects.filter(name=name,status=0)):
        products = Product.objects.filter(category__name=name)
        return render(request,"Products/index.html",{'products':products,'category_name':name})
    else:
        messages.warning(request,"No such Category found")
        return redirect('collections')

def product_details(request,cname,pname):
    if(Category.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            product = Product.objects.get(name=pname,status=0)
            return render(request,"Products/product_details.html",{'product':product,'category_name':cname})
        else:
            messages.error(request,"No such product found")
            return redirect(request,'Products/product_details.html')
    else:
        messages.error(request,"No suct Product Found")
        return redirect('collections')

def addtocart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            qty_bought = data['product_qty']
            id_bought = data['pid']
            #print(request.user.id)
            product_status = Product.objects.get(id=id_bought)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=id_bought):
                    return JsonResponse({'status':'Product Already in Cart'},status=200)
                else:
                    if product_status.quantity >= qty_bought:
                        Cart.objects.create(user=request.user,product_id = id_bought,product_qty = qty_bought)
                        return JsonResponse({'status':'Product Added to Cart'},status=200)
                    else:
                        return JsonResponse({'status':'Product out of Stock'},status=200)
        else:
            return JsonResponse({'status':'Login to Add Cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)

def cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request,'shop/cart.html',{'cart':cart})
    return redirect("shop/home")

def remove_from_cart(request,cart_id):
    cart_item= Cart.objects.get(id=cart_id)
    cart_item.delete()
    return redirect("cart")

def add_to_favorites(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            id_fav = data['pid']
            #print(request.user.id)
            product_status = Product.objects.get(id=id_fav)
            if product_status:
                if Favorite.objects.filter(user=request.user.id,product_id=id_fav):
                    return JsonResponse({'status':'Product Already in Favorites'},status=200)
                else:
                    Favorite.objects.create(user=request.user,product_id = id_fav)
                    return JsonResponse({'status':'Product Added to Favorites'},status=200)
        else:
            return JsonResponse({'status':'Login to Add Favorites'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)

def favorites_page(request):
    if request.user.is_authenticated:
        favs = Favorite.objects.filter(user=request.user)
        return render(request,'shop/favorites.html',{'favorites':favs})
    return redirect("shop/home")

def remove_from_favorite(request,fav_id):
    fav_item= Favorite.objects.get(id=fav_id)
    fav_item.delete()
    return redirect("fav")



def keycloak_callback(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'error': 'Missing code'}, status=400)

    token_url = f"{settings.KEYCLOAK_SERVER_URL}realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': settings.KEYCLOAK_CLIENT_ID,
        'client_secret': settings.KEYCLOAK_CLIENT_SECRET_KEY,
        'redirect_uri': 'http://localhost:8000/shop/keycloak/callback/'
    }

    response = requests.post(token_url, data=data)
    token_data = response.json()

    if 'access_token' not in token_data:
        return JsonResponse({'error': 'Token fetch failed', 'details': token_data}, status=400)

    # Store id_token directly from this response
    request.session['id_token'] = token_data.get('id_token')

    access_token = token_data['access_token']
    user_info = jwt.get_unverified_claims(access_token)

    username = user_info.get('preferred_username')
    email = user_info.get('email', f'{username}@example.com')  # fallback
    first_name = user_info.get('given_name', '')
    last_name = user_info.get('family_name', '')

    user, created = User.objects.get_or_create(username=username, defaults={
        'email': email,
        'first_name': first_name,
        'last_name': last_name
    })

    login(request, user)

    print(request.session.get('id_token'))  # should now show a JWT token starting with 'eyJ...'

    return redirect('/shop/home')

def keycloak_logout(request):
    id_token = request.session.get('id_token')
    logout(request)  # Django logout
    request.session.flush()

    keycloak_logout_url = (
        f"{settings.KEYCLOAK_SERVER_URL}realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/logout"
        f"?id_token_hint={id_token}&post_logout_redirect_uri=http://localhost:8000/shop/home"
    )

    return redirect(keycloak_logout_url)

def register_user(request):
    # Sample — you can extract these from POST data too
    username = "newuser123"
    email = "newuser123@example.com"
    password = "password123"
    first_name = "New"
    last_name = "User"

    keycloak = KeycloakService()
    result = keycloak.create_user(username, email, password, first_name, last_name)

    return JsonResponse(result)


def register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            #  Call Keycloak Service to create user
            keycloak = KeycloakService()
            result = keycloak.create_user(username, email, password)

            if result['status'] == 'success':
                messages.success(request, 'Your account has been created successfully in Keycloak! You can now log in.')
                return redirect('http://localhost:8080/realms/shopkart/protocol/openid-connect/auth?client_id=shopkart-client&redirect_uri=http://localhost:8000/shop/keycloak/callback/&response_type=code&scope=openid&prompt=login')
            elif result['status'] == 'exists':
                messages.warning(request, 'User already exists in Keycloak. Try a different username.')
            else:
                messages.error(request, f"Keycloak Error: {result['message']}")
        else:
            messages.error(request, 'Form validation failed. Check the details and try again.')
    else:
        form = CustomUserForm()

    return render(request, 'shop/register.html', {'form': form})


def search_products(request):
    if request.method == 'GET' and 'term' in request.GET:
        search_term = request.GET.get('term')

        products = Product.objects.filter(
            name__icontains=search_term, 
            status=0  # Only show visible products
        )[:5]  # Limit to 5 results
        
        results = []
        for product in products:
            product_dict = {
                'id': product.id,
                'label': f"{product.name} - {product.category.name}",
                'value': product.name,
                'url': reverse('product_details', kwargs={
                    'cname': product.category.name,
                    'pname': product.name
                })
            }
            results.append(product_dict)
        
        return JsonResponse(results, safe=False)
    
    return JsonResponse([], safe=False)

def product_search(request):
    query = request.GET.get('search', '')
    products = Product.objects.filter(name__icontains=query, status=0)
    return render(request, 'Products/search_results.html', {'products': products, 'query': query})

# views.py
def search_results(request, term):
    print("term",term)
    products = Product.objects.filter(
        name__icontains=term,
        status=0
    )
    return render(request, 'Products/search_results.html', {
        'products': products,
        'search_term': term,
        'category_name': 'all'  # Using 'all' as a generic category for search
    })

def search_redirect(request):
    term = request.GET.get('term')
    print("Search term:", term)  # to debug
    if term:
        return redirect('search_results', term=term)
    else:
        return redirect('home')