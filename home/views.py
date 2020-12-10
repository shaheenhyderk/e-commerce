from django.shortcuts import render
from super_admin.models import Processor, Brand, Category, Ram, Storage, Product


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
    pass
