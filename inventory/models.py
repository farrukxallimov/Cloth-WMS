from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    
    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
    
    def __str__(self):
        return self.name

class Product(models.Model):
    SIZES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('3/4', '3/4'),
        ('5/6', '5/6'),
        ('7/8', '7/8'),
        ('9/10', '9/10'),
        ('11/12', '11/12'),
        ('13/14', '13/14'),
        ('2/10', '2/10'),
        ('2/20', '2/20'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Mahsulot nomi")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategoriya")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")
    size = models.CharField(max_length=10, choices=SIZES, verbose_name="O‘lcham")
    color = models.CharField(max_length=50, verbose_name="Rangi")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Miqdori")
    sku = models.CharField(max_length=50, unique=True, verbose_name="Artikul")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Tovar"
        verbose_name_plural = "Tovarlar"
    
    def __str__(self):
        return f"{self.name} - {self.size} - {self.color}"
    
    @property
    def is_in_stock(self):
        return self.quantity > 0

class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('IN', 'Kirim'),
        ('OUT', 'Chiqim'),
        ('RETURN', 'Qaytma'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Mahsulot")
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPES, verbose_name="Operatsiya turi")
    quantity = models.IntegerField(verbose_name="Miqdori")
    notes = models.TextField(blank=True, verbose_name="Izoh")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Mahsulot harakati"
        verbose_name_plural = "Mahsulot harakatlari"
