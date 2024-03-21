from django.test import TestCase
from accounts.models import Account
from transactions.services import TransactionService
from common.error_handler import ErrorHandler
from django.contrib.auth import get_user_model

User = get_user_model()

class TransactionServiceTests(TestCase):
  def setUp(self):  
    user1 = User.objects.create_user(username='user1', password='testpass123')
    user2 = User.objects.create_user(username='user2', password='testpass123')
    self.account1 = Account.objects.create(user=user1, balance=1000)
    self.account2 = Account.objects.create(user=user2, balance=500)
    self.service = TransactionService()
    
  def test_deposit_positive_amount(self):
        self.service.deposit(self.account1.id, 500)
        self.account1.refresh_from_db()
        self.assertEqual(self.account1.balance, 1500)

  def test_deposit_negative_amount(self):
      with self.assertRaises(ErrorHandler) as cm:
          self.service.deposit(self.account1.id, -100)
      self.assertEqual(cm.exception.code, 400)
      self.account1.refresh_from_db()
      self.assertEqual(self.account1.balance, 1000)  

  def test_withdraw_sufficient_balance(self):
      self.service.withdraw(self.account1.id, 200)
      self.account1.refresh_from_db()
      self.assertEqual(self.account1.balance, 800)

  def test_transfer_between_accounts(self):
      self.service.transfer(self.account1.id, self.account2.id, 200)
      self.account1.refresh_from_db()
      self.account2.refresh_from_db()
      self.assertEqual(self.account1.balance, 800)
      self.assertEqual(self.account2.balance, 700)