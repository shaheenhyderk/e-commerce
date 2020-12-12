from django.shortcuts import render, redirect
from super_admin.models import Processor, Brand, Category, Ram, Storage, Product
from django.contrib.auth.models import auth, User
from django.http import JsonResponse


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
            return JsonResponse('valid', safe=False)
        else:
            return JsonResponse('invalid', safe=False)
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
                return JsonResponse('Username already used', safe=False)
            elif User.objects.filter(email=email).exists():
                return JsonResponse('Email Already used', safe=False)
            else:
                User.objects.create_user(first_name=name, username=username, email=email, password=password1)
            return JsonResponse('valid', safe=False)
        else:
            return JsonResponse('Password mismatch', safe=False)
    else:
        return render(request, 'home/signup.html')


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect(home)


def view_product(request, id):
    product = Product.objects.get(id=id)
    context = {"product": product}
    return render(request, 'home/product.html', context)
