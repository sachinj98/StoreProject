from django.shortcuts import render
from django.views import View
from .models import Product , Feedback, Customer, Cart, Payment, OrderPlaced, Wishlist
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .import forms
from django.contrib import messages
import razorpay
from django.conf import settings
# Create your views here.

@login_required
def home(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    # return render(request, 'app/base.html')
    return render(request, 'app/index.html', locals())


@login_required
def about(request):
    totalitem = 0    # this code is used here to show the number of cart item in cart and we have to write this code in every view fuction
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/about.html', locals())

@login_required
def contact(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/contact.html', locals())


@login_required
def feedback_form(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/feedbackform.html', locals())


@login_required
def feedback_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        feedback_text = request.POST.get('feedback_text')
        Feedback.objects.create(name=name, email=email, feedback_text=feedback_text)
        return redirect('thank_you_page')
    

@login_required
def thank_you_page(request):
    return render(request, 'app/thank_you.html')    


@method_decorator(login_required, name='dispatch')
class CategoryView(View):
    def get(self, request, val):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title').annotate(total=Count('title'))
        return render(request, 'app/category.html', locals())
    

@method_decorator(login_required, name='dispatch')
class CategoryTitle(View):
    def get(self, request, val):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, 'app/category.html', locals())


@method_decorator(login_required, name='dispatch')
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
       
        return render(request, 'app/productdetail.html', locals())


@method_decorator(login_required, name='dispatch')
class CustomerRegistration(View):
    def get(self, request):
        form = forms.CustomerRegistrationForm()
        return render(request, 'app/customer_registration.html', {'form':form})
  
    def post(self, request):
        if request.method == 'POST':
            form = forms.CustomerRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Congratulations! User Register Successfully")
            else: 
                messages.warning(request, "Provide valid Input Data")
        return render(request, 'app/customer_registration.html', locals())


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm
        return render(request, 'app/profile.html', locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, locality=locality, city=city, mobile=mobile, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulations! Profile Save Syccessfully")
        else:
            messages.warning(request, "Invalid Input Data")    
        return render(request, 'app/profile.html', locals())
        

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', locals())


@method_decorator(login_required, name='dispatch')
class UpdateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)            # To get data in update form for updating
        form = CustomerProfileForm(instance=add)       
        return render(request, 'app/updateaddress.html', locals())

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratulations! Profile Update Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect("address")       

        # return render(request, 'app/updateaddress.html', locals())

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")

@login_required
def buy_now(request, product_id):
    product = Product.objects.get(pk=product_id)
    product_image_url = product.product_image.url if product.product_image else ''
    request.session['buy_now_product'] = {
        'id': product.id,
        'title': product.title,
        'discounted_price': product.discounted_price,
        'selling_price': product.selling_price,
        'description': product.description,
        'composition': product.composition,
        'category' : product.category,
        'product_image_url' : product_image_url,
    }
    return redirect('show_cart')

@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity*p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40    
    return render(request, 'app/addtocart.html', locals())


@method_decorator(login_required, name='dispatch')
class Checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity*p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40   
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount": razoramount, "currency": "INR", "receipt": "order_receipt_11"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        # {'id': 'order_MI1NDsBoYBrieH', 'entity': 'order', 'amount': 67000, 'amount_paid': 0, 'amount_due': 67000, 'currency': 'INR', 'receipt': 'order_receipt_11', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1690285266}
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user = user, 
                amount = totalamount,
                razorpay_order_id = order_id,
                razorpay_payment_status = order_status
            )
            payment.save()
        return render(request, 'app/checkout.html', locals())


@login_required
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    user = request.user
    customer = Customer.objects.get(id=cust_id)
    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=payment).save()
        c.delete()
    return redirect('orders')        


@login_required
def orders(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', locals())  

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user) 
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        # print(prod_id)
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user) 
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        # print(prod_id)
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)
    

@login_required
# def remove_cart(request):
#     if request.method == 'POST':
#         prod_id = request.GET['prod_id']
#         c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
#         c.delete()
#         user = request.user
#         cart = Cart.objects.filter(user=user) 
#         amount = 0
#         for p in cart:
#             value = p.quantity * p.product.discounted_price
#             amount = amount + value
#         totalamount = amount + 40
#         # print(prod_id)
#         data = {
#             'amount': amount,
#             'totalamount': totalamount
#         }
#         return JsonResponse(data)

def remove_cart(request):
    if request.method == 'POST':
        prod_id = request.POST.get('product_id')
        c = Cart.objects.filter(user=request.user, product=prod_id).first()
        if c:
            c.delete()

        cart = Cart.objects.filter(user=request.user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value

        totalamount = amount + 40

        data = {
            'amount': amount,
            'totalamount': totalamount,
            'success': True
        }
        return JsonResponse(data)
    else:
        data = {
            'success': False
        }
        return JsonResponse(data)
    



@login_required
def plus_wishlist(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)   # object of that product
        user = request.user             # This is the log in user
        Wishlist(user=user, product=product).save()    # save the data in Wishlist table
        data = {
            'message': 'Wishlist Added Successfully..!',
        }    
        return JsonResponse(data)
    
@login_required
def minus_wishlist(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)   # object of that product
        user = request.user             # This is the log in user
        Wishlist(user=user, product=product).delete()    # to delete the data from Wishlist table
        data = {
            'message': 'Wishlist Remove Successfully..!',
        }    
        return JsonResponse(data)    
    

@login_required
def search(request):
    query = request.GET['search']
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request, 'app/search.html', locals())