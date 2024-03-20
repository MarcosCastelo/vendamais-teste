from django.db import transaction
from accounts.models import Account
from common.error_handler import ErrorHandler
from transactions.validators import PositiveAmountValidator, SufficientBalanceValidator
from transactions.models import Transaction
from django.core.exceptions import ValidationError


class TransactionService: 
  def __init__(self):
    self.positive_amount_validator = PositiveAmountValidator()
    self.sufficient_balance_validator = SufficientBalanceValidator()
  
  def _get_account(self, account_id: int):
    try:
      return Account.objects.get(id=account_id)
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
    except ValidationError as e:
      raise ErrorHandler(str(e), code=400)
  
  @transaction.atomic
  def deposit(self, account_id: int, amount: float):
    self.positive_amount_validator.validate(amount)
    account = self._get_account(account_id)
    account.balance += amount
    account.save()
    self._create_transaction(account, None, Transaction.DEPOSIT, amount)
    
  @transaction.atomic
  def withdraw(self, account_id: int, amount: float):
    self.positive_amount_validator.validate(amount)
    self.sufficient_balance_validator.validate(account_id, amount)
    account = self._get_account(account_id)
    account.balance -= amount
    account.save()
    self._create_transaction(account, None, Transaction.WITHDRAW, amount)
    
  @transaction.atomic
  def transfer(self, source_account_id: int, destination_account_id: int, amount: float):
    self.positive_amount_validator.validate(amount)
    self.sufficient_balance_validator.validate(source_account_id, amount)
    source_account = self._get_account(source_account_id)
    destination_account = self._get_account(destination_account_id)
    source_account.balance -= amount
    destination_account.balance += amount
    source_account.save()
    destination_account.save()
    self._create_transaction(source_account, destination_account, Transaction.TRANSFER, amount)
  