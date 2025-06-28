from django.urls import path,include
from . import views


urlpatterns = [
    path('shop/keycloak/callback/', views.keycloak_callback, name='keycloak_callback'),
    path('keycloak/callback/', views.keycloak_callback, name='keycloak_callback'),
    path('logout' ,views.keycloak_logout, name="logout" ),
    path('home',views.home,name='home'),
    path('register',views.register,name='register'),
    path('collections/' ,views.collections, name="collections" ),
    path('collections/<str:name>' ,views.collections_view, name="collections_view" ),
    path('collections/<str:cname>/<str:pname>' ,views.product_details, name="product_details" ),
    path('login' ,views.login_page, name="login" ),
    #path('logout' ,views.logout_page, name="logout" ),
    path('addToCart' ,views.addtocart, name="addtocart" ),
    path('cart' ,views.cart_page, name="cart" ),
    path('removeFromCart/<str:cart_id>' ,views.remove_from_cart, name="remove_from_cart" ),
    path('addToFav' ,views.add_to_favorites, name="add_to_fav" ),
    path('fav' ,views.favorites_page, name="fav" ),
    path('removeFromFav/<str:fav_id>' ,views.remove_from_favorite, name="remove_from_fav" ),
    path('search/', views.search_redirect, name='search_redirect'),
    path('collections/all/<str:term>/', views.search_results, name="search_results"),
]