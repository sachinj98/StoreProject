from rest_framework import serializers
from app.models import Product, Customer, Cart, Payment

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
	

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
	 
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer    
        fields = "__all__"
        

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
