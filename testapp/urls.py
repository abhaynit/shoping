from django.urls import path
from testapp import views
#from django.contrib.auth import views as auth_views

# FOR STATIC FILE 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name= "home"),
    path('register/',views.register,name="register"),
    path('valid/',views.valid,name='valid'),
    path('validate/',views.otp_validate,name='validate'),
    path('login/',views.user_login,name = "login"),
    path('logout/',views.user_logout,name= "logout"),
    path('profile/',views.user_profile,name="profile"),
    path('change_password/',views.user_change_password,name="change_password"),
    path('detail/<int:id>',views.product_detail,name="detail"),
    path('mobile/<slug:it>',views.product,name="utility"),
    path('filter/<int:price>/<slug:it>/<int:abc>',views.product_filter,name="filte"),
    path('add/<int:it>',views.add_to_cart,name= "add"),
    path('cart/',views.carted_item,name="cart"),
    path('remove/<int:id1>',views.remove_from_cart,name="remove"),
    path('ordered_placed/',views.order_status,name='ordered_placed'),
    path('cancel/<int:it>',views.cancel_order,name='cancel'),
    path('address/',views.address_of_the_current_user,name="address"),
    path('remove_ad/<int:it>',views.remove_address,name= 'remove_ad'),
    path('addaddress/',views.add_address,name='addaddress'),
    path('ordered/<int:it>',views.place_order,name="ordered"),
    path('add_user_image/',views.add_image,name='add_image'),
    path('shop_now/<int:it>/<int:shp>',views.shop_now,name='shop_now'),
    path('shop_now_address/<int:it>',views.shop_now_address,name='shop_now_address'),
    path('movie/',views.movie,name='movie'),
    path('hall/<slug:it>',views.hall_name,name= "hall"),
    path('bookmovie/<slug:chall>/<slug:movi>/<int:val>',views.bookmovie,name = "bookmovie"),
    path('no_of_user/<slug:chall>/<slug:movi>/<int:val>',views.no_of_user,name='userlist'),
    path('corona/',views.corona,name='corona'),
    

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# here i have imported settings 
# and  i have already defined the path for media
# so we are  accessing the value of the variable document_root as setttings.MEDIA_ROOT 
#I THINK SETTINGS NEED TWO ARGUMENTS ONE IS MEDIA_URL WHICH GIVES THE VALUE OF THE FOLDER MEDIA
# AND THE DOCUMENT_ROOT GIVES THE PATH TO MEDIA FOLDER