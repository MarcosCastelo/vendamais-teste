from django.db import models
from common.error_handler import ErrorHandler
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
  phone = models.CharField(max_length=15, blank=True, null=True)
  
  def __str__(self):
    return self.username

class Account(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='account')
  balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  is_active = models.BooleanField(default=True)
  
  def clean(self):
    if not self.is_active:
      raise ErrorHandler("The account is not active.", code=400)
  
  def __str__(self):
    return f'Account for {self.user.username} with balance {self.balance}'
