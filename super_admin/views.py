from django.shortcuts import render, redirect
from .models import Processor, Brand, Category, Ram, Storage, Product
from django.contrib.auth.models import User, auth
from django.http import JsonResponse
import base64
from django.core.files.base import ContentFile


# Create your views here.
def login(request):
    if 'isAdmin' in request.session:
        return redirect(options)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        admin = auth.authenticate(username=username, password=password)
        if admin is not None and admin.is_superuser:
            request.session['isAdmin'] = True
            data = {'status': 'valid'}
            return JsonResponse(data=data)
        else:
            data = {'status': 'invalid'}
            return JsonResponse(data=data)
    else:
        return render(request, 'super_admin/login.html')


def logout(request):
    if 'isAdmin' in request.session:
        request.session.flush()
        return redirect(login)


def products(request):
    if 'isAdmin' not in request.session:
        return redirect(login)
    products = Product.objects.all()
    processors = Processor.objects.all()
    brands = Brand.objects.all()
    categories = Category.objects.all()
    rams = Ram.objects.all()
    storages = Storage.objects.all()
    context = {"products": products, "categories": categories, "brands": brands, "processors": processors, "rams": rams,
               "storages": storages}
    return render(request, 'super_admin/products.html', context)


def create_product(request):
    if 'isAdmin' not in request.session:
        return redirect(login)
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        quantity = request.POST['quantity']
        category_id = request.POST['category']
        brand_id = request.POST['brand']
        processor_id = request.POST['processor']
        ram_id = request.POST['ram']
        storage_id = request.POST['storage']
        image_data = request.POST['image_base64']
        if image_data is not '':
            format, img_str = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image = ContentFile(base64.b64decode(img_str), name=name + '.' + ext)
        else:
            image = None

        Product.objects.create(name=name, description=description, price=price, quantity=quantity,
                               category_id=category_id, brand_id=brand_id, processor_id=processor_id, ram_id=ram_id,
                               storage_id=storage_id, image=image)
        return redirect(products)


def edit_product(request, id):
    if 'isAdmin' not in request.session:
        return redirect(login)
    if request.method == 'POST':
        product = Product.objects.get(id=id)
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.quantity = request.POST['quantity']
        product.category_id = request.POST['category']
        product.brand_id = request.POST['brand']
        product.processor_id = request.POST['processor']
        product.ram_id = request.POST['ram']
        product.storage_id = request.POST['storage']
        image_data = request.POST['image_base64']

        if image_data is not '':
            format, img_str = image_data.split(';base64,')
            ext = format.split('/')[-1]
            product.image = ContentFile(base64.b64decode(img_str), name=product.name + '.' + ext)

        product.save()
        return redirect(products)


def delete_product(request, id):
    if 'isAdmin' not in request.session:
        return redirect(login)
    Product.objects.get(id=id).delete()
    return redirect(products)


def options(request):
    if 'isAdmin' not in request.session:
        return redirect(login)
    processors = Processor.objects.all()
    brands = Brand.objects.all()
    categories = Category.objects.all()
    rams = Ram.objects.all()
    storages = Storage.objects.all()
    data = {"category": categories, "brand": brands, "processor": processors, "ram": rams, "storage": storages}
    context = {"data": data}
    return render(request, 'super_admin/options.html', context)


def create_category(request):
    if 'isAdmin' not in request.session:
        return redirect(login)
    if request.method == 'POST':
        name = request.POST['name']
        Category.objects.create(name=name)
        return redirect(options)


def create_brand(request):
    if 'isAdmin' not in request.session:
        return redirect(login)
    if request.method == 'POST':
        name = request.POST['name']
        Brand.objects.create(name=name)
        return redirect(options)


def create_processor(request):
    if 'isAdmin' not in request.session:
        return redirect(login)
    if request.method == 'POST':
        name = request.POST['name']
        Processor.objects.create(name=name)
        return redirect(options)


def create_ram(request):
    if 'isAdmin' not in request.session:
        return redirect(login)
    if request.method == 'POST':
        name = request.POST['name']
        Ram.objects.create(name=name)
        return redirect(options)


def create_storage(request):
    if 'isAdmin' not in request.session:
        return redirect(login)
    if request.method == 'POST':
        name = request.POST['name']
        Storage.objects.create(name=name)
        return redirect(options)


def edit_category(request, id):
    if 'isAdmin' not in request.session:
        return redirect(login)
    if request.method == 'POST':
        name = request.POST['name']
        category = Category.objects.get(id=id)
        category.name = name
        category.save()
        return redirect(options)


def edit_brand(request, id):
    if 'isAdmin' not in request.session:
        return redirect(login)
    if request.method == 'POST':
        name = request.POST['name']
        brand = Brand.objects.get(id=id)
        brand.name = name
        brand.save()
        return redirect(options)


def edit_processor(request, id):
    if 'isAdmin' not in request.session:
        return redirect(login)
    if request.method == 'POST':
        name = request.POST['name']
        processor = Processor.objects.get(id=id)
        processor.name = name
        processor.save()
        return redirect(options)


def edit_ram(request, id):
    if 'isAdmin' not in request.session:
        return redirect(login)
    if request.method == 'POST':
        name = request.POST['name']
        ram = Ram.objects.get(id=id)
        ram.name = name
        ram.save()
        return redirect(options)


def edit_storage(request, id):
    if 'isAdmin' not in request.session:
        return redirect(login)
    if request.method == 'POST':
        name = request.POST['name']
        storage = Storage.objects.get(id=id)
        storage.name = name
        storage.save()
        return redirect(options)


def delete_category(request, id):
    if 'isAdmin' not in request.session:
        return redirect(login)
    category = Category.objects.get(id=id)
    category.delete()
    return redirect(options)


def delete_brand(request, id):
    if 'isAdmin' not in request.session:
        return redirect(login)
    brand = Brand.objects.get(id=id)
    brand.delete()
    return redirect(options)


def delete_processor(request, id):
    if 'isAdmin' not in request.session:
        return redirect(login)
    processor = Processor.objects.get(id=id)
    processor.delete()
    return redirect(options)


def delete_ram(request, id):
    if 'isAdmin' not in request.session:
        return redirect(login)
    ram = Ram.objects.get(id=id)
    ram.delete()
    return redirect(options)


def delete_storage(request, id):
    if 'isAdmin' not in request.session:
        return redirect(login)
    storage = Storage.objects.get(id=id)
    storage.delete()
    return redirect(options)


def get_users(request):
    if 'isAdmin' not in request.session:
        return redirect(login)
    users = User.objects.filter(is_superuser=False)
    context = {"users": users}
    return render(request, 'super_admin/users.html', context)
