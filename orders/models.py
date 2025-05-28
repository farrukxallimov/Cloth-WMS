from django.db import models
from django.contrib.auth.models import User
from inventory.models import Product


class Customer(models.Model):
    name = models.CharField(max_length=200, verbose_name="FIO")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    address = models.TextField(verbose_name="Manzil")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'Yangi'),
        ('PROCESSING', 'Ishlovda'),
        ('SHIPPED', 'Yuborildi'),
        ('DELIVERED', 'Yetkazildi'),
        ('CANCELLED', 'Bekor qilindi'),
    ]

    DELIVERY_STATUS_CHOICES = [
        ('PENDING', 'Kutilmoqda'),
        ('PREPARING', 'Tayorgarlik'),
        ('IN_TRANSIT', 'Yo`lga tushdi'),
        ('DELIVERED', 'Yetib keldi'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Ta'minotchi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW', verbose_name="Status")
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='PENDING',
                                       verbose_name="Yetkazib berish statusi")
    delivery_date = models.DateField(verbose_name="Yetkazib berish sanasi", null=True, blank=True)
    tracking_number = models.CharField(max_length=100, verbose_name="Kuzatuv raqami", blank=True, editable=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="To'lov summasi")
    notes = models.TextField(blank=True, verbose_name="Izoh")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Yaratdi")

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"

    def __str__(self):
        return f"Заказ #{self.id} - {self.customer.name}"

    def save(self, *args, **kwargs):
        if not self.tracking_number:
            from django.utils import timezone
            date_str = self.created_at.strftime('%d%m%Y%H%M%S')
            self.tracking_number = f'TRACK-{date_str}-{self.id}'
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Buyurtma")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Mahsulot")
    quantity = models.PositiveIntegerField(verbose_name="Miqdori")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")

    class Meta:
        verbose_name = "Buyurtma pozitsiyasi"
        verbose_name_plural = "Buyurtma pozitsiyalari"

    @property
    def total_price(self):
        return self.quantity * self.price