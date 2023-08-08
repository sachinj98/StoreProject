from app.models import Product, Customer, Cart, Payment
from app.api.serializers import ProductSerializer, CartSerializer, CustomerSerializer, PaymentSerializer
from rest_framework import viewsets



class ProductViewsets(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class PaymentViewsets(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class CustomerViewsets(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CartViewsets(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
