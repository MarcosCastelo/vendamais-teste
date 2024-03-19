from django.db import models
from accounts.models import Account
from common.exceptions.error_handler import ErrorHandler

class Transaction(models.Model):
  TRANSACTION_TYPE_CHOICES = (
    ('deposit', 'Deposit'),
    ('withdraw', 'Withdraw'),
    ('transfer', 'Transfer'),
  )
  
  transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
  source_account = models.ForeignKey(Account, related_name='transactions_made', on_delete=models.CASCADE)
  destination_account = models.ForeignKey(Account, related_name='transactions_received', on_delete=models.CASCADE, null=True, blank=True)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def clean(self):
    if self.amount <= 0:
      raise ErrorHandler("The transaction amount must be positive.", code=400)
