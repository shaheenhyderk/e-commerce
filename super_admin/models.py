from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Processor(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Ram(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Storage(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=5000)
    price = models.IntegerField()
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    processor = models.ForeignKey(Processor, on_delete=models.CASCADE)
    ram = models.ForeignKey(Ram, on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)

    @property
    def image_url(self):
        try:
            url = self.image.url
        except ValueError:
            url = ''
        return url
