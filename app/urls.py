from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, PasswordResetForm, MyPasswordChangeForm, MySetPasswordForm

urlpatterns = [
    path('',views.home, name = "home"),
    path('about/', views.about, name = "about"),
    path('contact/', views.contact, name = "contact"),
    path('feedback/', views.feedback_form, name='feedback_form'),
    path('feedback/submit/', views.feedback_submit, name='feedback_submit'),
    path('thank_you/', views.thank_you_page, name='thank_you_page'),
    path('category/<slug:val>', views.CategoryView.as_view(), name = "category"),
    path('product-detail/<int:pk>', views.ProductDetail.as_view(), name = "productdetail"),
    path('category-title/<val>', views.CategoryTitle.as_view(), name = "category-title"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('address/', views.address, name="address"),
    path('update-address/<int:pk>', views.UpdateAddress.as_view(), name='updateaddress'),
    
    path('search/', views.search, name="search"),
    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('cart/', views.show_cart, name="show_cart"),
    path('checkout/', views.Checkout.as_view(), name="checkout"),
    path('paymentdone/', views.payment_done, name="paymentdone"),
    path('orders/', views.orders, name="orders"),

    path('plus-cart/', views.plus_cart, name='plus-cart'),
    path('minus-cart/', views.minus_cart, name='minus-cart'),
    path('remove-cart/', views.remove_cart, name='remove-cart'),
    path('plus-wishlist/', views.plus_wishlist, name='plus-wishlist'),
    path('minus-wishlist/', views.minus_wishlist, name='minus-wishlist'),


    

# login authentication
    path('customer-registration/',views.CustomerRegistration.as_view(), name="customerregistration"),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='loginform'),
    path('password-change/', auth_view.PasswordChangeView.as_view(template_name='app/password_change.html', form_class=MyPasswordChangeForm, success_url='passwordchangedone'), name='password_change'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='/passwordchangedone'),
    path('logout/', auth_view.LogoutView.as_view(next_page = 'loginform'), name='logout'),

    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

