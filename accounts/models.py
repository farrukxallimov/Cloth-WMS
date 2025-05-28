from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    position = models.CharField(max_length=100, blank=True, verbose_name="Lavozim")
    
    class Meta:
        verbose_name = "Foydalanuvchi profili"
        verbose_name_plural = "Foydalanuvchilar profillari"
    
    def __str__(self):
        return f"Profil - {self.user.username}"
