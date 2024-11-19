"""
URL configuration for proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import home, CategoryView, ProductDetail, about, contact, CustomerRegistrationView, ProfileView, address, UpdateAddress, add_to_cart, show_cart, checkout, payment_done, orders, add_to_wishlist, show_wishlist, search, remove_from_cart, remove_from_wishlist, RequestBookView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from app.forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",home, name="home"),
    path('aboutus/', about, name="about"),
    path('contactus/', contact, name="contact"),
    path('genre/<slug:val>',CategoryView.as_view(),name="genre"),
    path("product-detail/<int:pk>",ProductDetail.as_view(),name="product-detail"),
    path("profile/", ProfileView.as_view(), name='profile'),
    path("address/",address, name='address'),
    path("UpdateAddress/<int:pk>", UpdateAddress.as_view(), name='UpdateAddress'),
    path("add-to-cart/", add_to_cart, name='add-to-cart'),
    path("cart/", show_cart, name='showcart'),
    path('checkout/', checkout.as_view(), name='checkout'),
    path('paymentdone/', payment_done, name='paymentdone'),
    path("orders/",orders, name='orders'),
    path('add-to-wishlist/', add_to_wishlist, name='add-to-wishlist'),
    path("wishlist/", show_wishlist, name='wishlist'),
    path('search/',search, name='search'),
    path('remove-from-cart/', remove_from_cart, name='remove-from-cart'),
    path('remove-from-wishlist/', remove_from_wishlist, name='remove-from-wishlist'),
    path("requestbook/",RequestBookView.as_view(), name='requestbook'),

    #authentications 
    path("registration/",CustomerRegistrationView.as_view(), name='customerregistration'),
    path("accounts/login/", auth_view.LoginView.as_view(template_name='login.html',authentication_form=LoginForm), name='login'),
    path("passwordchange/", auth_view.PasswordChangeView.as_view(template_name='changepassword.html',form_class=MyPasswordChangeForm, success_url='/passwordchangedone'),name='passwordchange'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'), name='passwordchangedone'),
    path("logout/", auth_view.LogoutView.as_view(next_page='login'), name='logout'),
    path("password-reset/", auth_view.PasswordResetView.as_view(template_name='password_reset.html',form_class=MyPasswordResetForm), name='password_reset'),
    path("password-reset/done/", auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path("password-reset-confirm/<uidb64>/<token>/", auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path("password-reset-complete/", auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Bibliogram"
admin.site.site_title = "Bibliogram"
admin.site.site_index_title = "Welcome to Bibliogram"