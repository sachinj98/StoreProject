from django.urls import path, include
from app.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('product',views.ProductViewsets, basename='product' )
router.register('payment',views.PaymentViewsets, basename='payment' )
router.register('customer',views.CustomerViewsets, basename='customer' )
router.register('cart',views.CartViewsets, basename='cart' )

urlpatterns = [
    path('', include(router.urls))
]
