from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django.views import View
from urllib import request
from django.http import HttpResponse, JsonResponse
from . models import Product, Customer, Cart, Payment, OrderPlaced, Wishlist, BookRequest
from . forms import CustomerRegistrationForm, CustomerProfileForm, BookRequestForm
from django.contrib import messages
import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required

class CategoryView(View):
    def get(self, request, val):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(genre=val)
        title = Product.objects.filter(genre=val).values('title').annotate(total=Count('title'))
        return render(request, 'category.html', locals())
    
class CategoryTitle(View):
    def get(self, request, val):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(category = val)
        title = Product.objects.filter(category = val).values('title')
        return render(request, 'category.html', locals())

def home(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'home.html')

class ProductDetail(View):
    def get(self, request, pk):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        product=Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product)& Q(user = request.user))
        return render(request, 'productdetail.html', locals())
    
def about(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'aboutus.html', locals())

class RequestBookView(View):
    def get(self, request):
        form = BookRequestForm()
        return render(request, 'requestbook.html', {'form': form})

    def post(self, request):
        form = BookRequestForm(request.POST)
        if form.is_valid():
            book_request = form.save(commit=False)
            book_request.requested_by = request.user
            book_request.save()
            messages.success(request, 'Thanks a lot Reader! We will be sure to update soon')
        else:
            messages.warning(request, 'Sorry user, check your input data')
        return render(request, 'requestbook.html', {'form': form})
def contact(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'contactus.html', locals())

class CustomerRegistrationView(View):
    def get(self, request):
        form=CustomerRegistrationForm()
        return render(request, 'customerregistration.html', locals())
    def post(self, request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations reader, Welcome to the bibliogram fam!')
        else:
            messages.warning(request,'Sorry user, check your input data')
        return render(request, 'customerregistration.html', locals())
    
class ProfileView(View):
    def get(self, request):
        form=CustomerProfileForm()
        return render(request, 'profile.html',locals())
    def post(self, request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            birthday=form.cleaned_data['birthday']

            reg=Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state, zipcode=zipcode, birthday=birthday)
            reg.save()
            messages.success(request, 'Congratulations! Profile Saved Successfully')
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'profile.html',locals())
    
def address(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request, 'address.html', locals())

class UpdateAddress(View):
    def get(self, request, pk):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        add = Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        return render(request, 'UpdateAddress.html', locals())
    def post(self, request, pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.birthday=form.cleaned_data['birthday']
            add.save()
            messages.success(request,"Yay! Profile Updation Successful")
        else:
            messages.warning(request, "Invalid Data")
        return redirect("address")

def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id').strip('/')
    product=Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")

def show_cart(request):
    user=request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    for p in cart:
        value = p.quantity * p.product.selling_price
        amount = amount + value
    totalamount = amount + 80
    return render(request, 'addtocart.html', locals())

def add_to_wishlist(request):
    if request.method == "POST":
        user = request.user
        product_id = request.POST.get('prod_id') 
        product = Product.objects.get(id=product_id)
        if not Wishlist.objects.filter(user=user, product=product).exists():
            Wishlist.objects.create(user=user, product=product)
    return redirect('home')

def show_wishlist(request):
    user = request.user
    wishlist = Wishlist.objects.filter(user=user)
    total_wishlist_items = 0
    if request.user.is_authenticated:
        total_wishlist_items = len(wishlist)
    return render(request, 'wishlist.html', locals())


class checkout(View):
    def get(self, request):
        user=request.user
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        add  = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity* p.product.selling_price
            famount = famount + value
        totalamount = famount + 80
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_SECRET_KEY))
        data = {"amount":razoramount, "currency":"INR", "receipt": "order_rcptid_11"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        #{'amount': 75900, 'amount_due': 75900, 'amount_paid': 0, 'attempts': 0, 'created_at': 1731868893, 'currency': 'INR', 'entity': 'order', 'id': 'order_PMTUHt7uFPjQev', 'notes': [], 'offer_id': None, 'receipt': 'order_rcptid_11', 'status': 'created'}
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
        return render(request, "checkout.html", locals())
    
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    #print("payment_done : old =", order_id, "pid = ", payment_id, "cid = ", cust_id)
    user = request.user
    #return redirect("orders")
    customer = Customer.objects.get(id = cust_id)
    payment = Payment.objects.get(razorpay_order_id = order_id )
    payment.pid=True
    payment.razorpay_payment_id = payment_id
    payment.save()
    cart = Cart.objects.filter(user = user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=payment).save()
        c.delete()
        return redirect("orders")

def orders(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user = request.user)
    return render(request, 'orders.html', locals())

def search(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    query = request.GET['search']
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request,'search.html', locals())

@login_required
def remove_from_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)
        cart_item = Cart.objects.filter(user=request.user, product=product)
        if cart_item.exists():
            cart_item.delete()
    return redirect('showcart')  

def remove_from_wishlist(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)
        wish_item = Wishlist.objects.filter(user=request.user, product=product)
        if wish_item.exists():
            wish_item.delete()
    return redirect('wishlist')  