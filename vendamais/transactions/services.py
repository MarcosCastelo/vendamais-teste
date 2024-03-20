from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Sum

from common.error_handler import ErrorHandler

from accounts.models import Account

from transactions.validators import PositiveAmountValidator, SufficientBalanceValidator
from transactions.models import Transaction

from decimal import Decimal
from datetime import timedelta


class TransactionService: 
  def __init__(self):
    self.positive_amount_validator = PositiveAmountValidator()
    self.sufficient_balance_validator = SufficientBalanceValidator()
  
  def _calculate_start_date(self, time_frame):
    time_frames = {
      '24h': timedelta(days=1),
      'last_week': timedelta(weeks=1),
      'last_month': timedelta(days=30),
    }
    return timezone.now() - time_frames.get(time_frame, timedelta(days=0))
  
  def _get_account_by_id(self, account_id: int):
    try:
      return Account.objects.get(id=account_id)
    except Account.DoesNotExist:
      raise ErrorHandler("Account not found.", code=404)
  
  def _get_account_by_cpf(self, account_cpf: int):
    try:
      return Account.objects.get(user__cpf=account_cpf)
    except Account.DoesNotExist:
      raise ErrorHandler("Account not found.", code=404)
  
  def _create_transaction(self, source_account, destination_account, transaction_type, amount):
    transaction = Transaction(
      transaction_type=transaction_type,
      source_account=source_account,
      destination_account=destination_account,
      amount=amount
    )
    
    try:
      transaction.full_clean()
      transaction.save()
      return transaction
    except ValidationError as e:
      raise ErrorHandler(str(e), code=400)
  
  @transaction.atomic
  def deposit(self, account_id: int, amount: float):
    self.positive_amount_validator.validate(amount)
    account = self._get_account_by_id(account_id)
    account.balance += Decimal(str(amount))
    account.save()
    return self._create_transaction(account, None, Transaction.DEPOSIT, amount)
    
  @transaction.atomic
  def withdraw(self, account_id: int, amount: float):
    self.positive_amount_validator.validate(amount)
    self.sufficient_balance_validator.validate(account_id, amount)
    account = self._get_account_by_id(account_id)
    account.balance -= Decimal(str(amount))
    account.save()
    return self._create_transaction(account, None, Transaction.WITHDRAW, amount)
    
  @transaction.atomic
  def transfer(self, source_account_id: int, destination_account_cpf: str, amount: float):
    self.positive_amount_validator.validate(amount)
    self.sufficient_balance_validator.validate(source_account_id, amount)
    source_account = self._get_account_by_id(source_account_id)
    Account.objects.get_queryset
    destination_account = self._get_account_by_cpf(destination_account_cpf)
    source_account.balance -= Decimal(str(amount))
    destination_account.balance += Decimal(str(amount))
    source_account.save()
    destination_account.save()
    return self._create_transaction(source_account, destination_account, Transaction.TRANSFER, amount)
  
  def report(self, account_id, time_frame='24h'):
    start_date = self._calculate_start_date(time_frame)
    
    account = self._get_account_by_id(account_id)
    
    transactions_made = Transaction.objects.filter(
      source_account=account,
      created_at__gte=start_date
    ) if start_date else Transaction.objects.filter(source_account=account)

    transactions_received = Transaction.objects.filter(
      destination_account=account,
      created_at__gte=start_date,
      transaction_type=Transaction.TRANSFER
    ) if start_date else Transaction.objects.filter(destination_account=account, transaction_type=Transaction.TRANSFER)

    
    total_in_from_deposits = transactions_made.filter(transaction_type=Transaction.DEPOSIT).aggregate(Sum('amount'))['amount__sum'] or 0.00
    total_in_from_transfers = transactions_received.aggregate(Sum('amount'))['amount__sum'] or 0.00
    total_in = Decimal(str(total_in_from_deposits)) + Decimal(str(total_in_from_transfers)) 

    total_out = transactions_made.filter(transaction_type__in=[Transaction.WITHDRAW, Transaction.TRANSFER]).aggregate(Sum('amount'))['amount__sum'] or 0.00
    
    transactions = transactions_made | transactions_received
    
    return {
      'transactions': transactions,
      'balance': account.balance,
      'total_in': total_in,
      'total_out': total_out,
    }
      