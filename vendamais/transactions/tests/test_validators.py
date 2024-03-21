from django.test import TestCase
from common.error_handler import ErrorHandler
from accounts.models import Account
from transactions.validators import PositiveAmountValidator, SufficientBalanceValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class PositiveAmountValidatorTests(TestCase):
  def test_positive_amount(self):
    validator = PositiveAmountValidator()
    try: 
      validator.validate(100)
    except ErrorHandler:
      self.fail("Validator raised ErrorHandler unexpectedly")
  
  def test_negative_amount(self):
    validator = PositiveAmountValidator()
    with self.assertRaises(ErrorHandler):
      validator.validate(-100)

class SufficientBalanceValidatorTests(TestCase):
  def setUp(self):
    user = User.objects.create_user(username='user', password='testpass123')
    self.account = Account.objects.create(user=user, balance=200)
  
  def test_sufficient_balance(self):
    validator = SufficientBalanceValidator()
    try: 
      validator.validate(self.account.id, 100)
    except ErrorHandler:
      self.fail("Validator raised ErrorHandler unexpectedly")
  
  def test_insufficient_balance(self):
    validator = SufficientBalanceValidator()
    with self.assertRaises(ErrorHandler):
      validator.validate(self.account.id, 300)