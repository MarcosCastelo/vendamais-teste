from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from common.exceptions.error_handler import ErrorHandler

class CustomUser(AbstractUser):
  pass

class Account(models.Model):
  user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='account')
  balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  is_active = models.BooleanField(default=True)
  
  def clean(self):
    if not self.is_active:
      raise ErrorHandler("The account balance cannot be negative.", code=400)
