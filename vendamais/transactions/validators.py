from common.error_handler import ErrorHandler
from accounts.models import Account

class PositiveAmountValidator:
  def validate(self, amount):
    if amount <= 0:
      raise ErrorHandler("The value must be positive.", code=400)

class SufficientBalanceValidator:
  def validate(self, account_id, amount):
    account = Account.objects.get(id=account_id)
    if account.balance < amount:
      raise ErrorHandler("Insufficient funds.", code=400)