from django.db.models import F
from django.shortcuts import render, redirect
from super_admin.models import *
from .models import *
from .forms import *
from django.contrib.auth.models import auth, User
from django.http import JsonResponse
import json
from uuid import uuid4


# Create your views here.
def home(request):
    processors = Processor.objects.all()
    brands = Brand.objects.all()
    categories = Category.objects.all()
    rams = Ram.objects.all()
    storages = Storage.objects.all()
    products = Product.objects.all()
    filters = {"category": categories, "brand": brands, "processor": processors, "ram": rams, "storage": storages}
    context = {"filters": filters, "products": products}
    return render(request, 'home/home.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect(home)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            data = {'status': 'valid'}
            return JsonResponse(data=data)
        else:
            data = {'status': 'invalid'}
            return JsonResponse(data=data)
    else:
        return render(request, 'home/login.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect(home)
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        print(request.POST)

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                data = {'status': 'Username already used'}
                return JsonResponse(data=data)
            elif User.objects.filter(email=email).exists():
                data = {'status': 'Email Already used'}
                return JsonResponse(data=data)
            else:
                User.objects.create_user(first_name=name, username=username, email=email, password=password1)
                data = {'status': 'valid'}
                return JsonResponse(data=data)
        else:
            data = {'status': 'Password mismatch'}
            return JsonResponse(data=data)
    else:
        return render(request, 'home/signup.html')


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect(home)


def view_profile(request):
    if not request.user.is_authenticated:
        return redirect(login)
    return render(request, 'home/profile.html')


def view_address(request):
    if not request.user.is_authenticated:
        return redirect(login)
    user = request.user
    addresses = Address.objects.filter(user=user)
    context = {"addresses": addresses}
    return render(request, 'home/address.html', context)


def create_address(request):
    if not request.user.is_authenticated:
        return redirect(login)
    if request.method == 'POST':
        user = request.user
        form = AddressForm(request.POST)
        address = form.save(commit=False)
        address.user = user
        address.save()
        return redirect('user_address')
    else:
        form = AddressForm()
        context = {"form": form}
        return render(request, 'home/create_address.html', context)


def view_product(request, id):
    product = Product.objects.get(id=id)
    context = {"product": product}
    return render(request, 'home/product.html', context)


def view_cart(request):
    if request.user.is_authenticated:
        user = request.user
        if 'cart' in request.COOKIES:
            cart_cookie = json.loads(request.COOKIES['cart'])
            create_carts = []
            existing_carts = Cart.objects.filter(user=user)
            for pro_id, qty in cart_cookie.items():
                if not any(x.product_id == int(pro_id) for x in existing_carts):
                    create_carts.append(Cart(user=user, product_id=int(pro_id), quantity=qty))
            Cart.objects.bulk_create(create_carts)
        carts = Cart.objects.filter(user=user)
        context = {"carts": carts}
        response = render(request, 'home/cart.html', context)
        response.delete_cookie('cart')
        return response
    else:
        cart_cookie = {}
        if 'cart' in request.COOKIES:
            cart_cookie = json.loads(request.COOKIES['cart'])
        carts = []
        for pro_id, qty in cart_cookie.items():
            carts.append(Cart(id=int(pro_id), quantity=qty, product_id=pro_id))
        context = {"carts": carts}
        return render(request, 'home/cart.html', context)


def add_to_cart(request, id):
    if request.user.is_authenticated:
        user = request.user
        if 'cart' in request.COOKIES:
            cart_cookie = json.loads(request.COOKIES['cart'])
            create_cart = []
            existing_cart = Cart.objects.filter(user=user)
            for pro_id, qty in cart_cookie.items():
                if not any(x.product_id == int(pro_id) for x in existing_cart):
                    create_cart.append(Cart(user=user, product_id=int(pro_id), quantity=qty))
            Cart.objects.bulk_create(create_cart)
        product = Product.objects.get(id=id)
        if Cart.objects.filter(user=user, product=product).exists():
            Cart.objects.filter(user=user, product=product).update(quantity=F('quantity') + 1)
        else:
            Cart.objects.create(user=user, product=product, quantity=1)
        data = {"status": "done"}
        response = JsonResponse(data=data)
        response.delete_cookie('cart')
        return response
    else:
        data = {"status": "done"}
        response = JsonResponse(data=data)
        cart_cookie = {id: 1}
        if 'cart' in request.COOKIES:
            cart_cookie = json.loads(request.COOKIES['cart'])
            if str(id) in cart_cookie:
                cart_cookie[str(id)] += 1
            else:
                cart_cookie[id] = 1
        response.set_cookie("cart", json.dumps(cart_cookie))
        return response


def cart_edit(request, id):
    if request.user.is_authenticated:
        user = request.user
        value = int(request.POST['value'])
        cart = Cart.objects.get(user=user, id=id)
        cart.quantity += value
        cart.save()
        data = {'id': id, 'quantity': cart.quantity, 'product_total': cart.product_total}
        return JsonResponse(data=data)
    else:
        if 'cart' in request.COOKIES:
            value = int(request.POST['value'])
            cart_cookie = json.loads(request.COOKIES['cart'])
            if str(id) in cart_cookie:
                cart_cookie[str(id)] += value
                quantity = cart_cookie[str(id)]
                product = Product.objects.get(id=id)
                data = {'id': id, 'quantity': quantity, 'product_total': quantity * product.price}
                response = JsonResponse(data=data)
                response.set_cookie("cart", json.dumps(cart_cookie))
                return response


def cart_delete(request, id):
    if request.user.is_authenticated:
        user = request.user
        Cart.objects.get(user=user, id=id).delete()
        return redirect(view_cart)
    else:
        if 'cart' in request.COOKIES:
            cart_cookie = json.loads(request.COOKIES['cart'])
            if str(id) in cart_cookie:
                cart_cookie.pop(str(id))
                response = redirect(view_cart)
                response.set_cookie("cart", json.dumps(cart_cookie))
                return response


def checkout(request):
    if not request.user.is_authenticated:
        return redirect(login)
    if request.method == 'POST':
        user = request.user
        payment_mode = int(request.POST['paymentMode'])
        address_id = request.POST['addressId']
        carts = Cart.objects.filter(user=user)
        paid = payment_mode != 1
        tid = uuid4()
        orders = []
        products = []
        for cart in carts:
            orders.append(Order(user=user, address_id=address_id, product=cart.product, quantity=cart.quantity,
                                product_total=cart.product_total, tid=tid, paid=paid,
                                order_status=Order.ORDER_PLACED, payment_mode=Order.PAYMENT_COD))
            cart.product.quantity -= 1
            products.append(cart.product)
        Order.objects.bulk_create(orders)
        Product.objects.bulk_update(products, ['quantity'])
        carts.delete()
        data = {'status': 'success'}
        return JsonResponse(data=data)
    else:
        user = request.user
        addresses = Address.objects.filter(user=user)
        carts = Cart.objects.filter(user=user)
        total_amount = 0
        for cart in carts:
            total_amount += cart.product_total
        context = {"addresses": addresses, "carts": carts, "total_amount": total_amount}
        return render(request, 'home/checkout.html', context)
