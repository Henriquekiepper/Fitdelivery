from django.db import models
from django.contrib.auth.models import User


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.store_name


class Supplement(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='supplements')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='supplements')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='supplements')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='supplements/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SupplementInventory(models.Model):
    total_products = models.IntegerField()
    total_value = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.total_products} produtos - R${self.total_value}'
    
    
class Gym(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='gym_logos/', blank=True, null=True)
    primary_color = models.CharField(max_length=7, default='#3498db')  # HEX Code
    secondary_color = models.CharField(max_length=7, default='#2ecc71')  # HEX Code
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
