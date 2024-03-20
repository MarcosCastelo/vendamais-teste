from rest_framework import serializers
from transactions.models import Transaction

from accounts.serializers import AccountSerializer

class TransactionSerializer(serializers.ModelSerializer):
  source_account = AccountSerializer(read_only=True)
  class Meta:
    model = Transaction
    fields = ['id', 'transaction_type', 'source_account', 'destination_account', 'amount', 'created_at']
    read_only_fields = ['id', 'created_at']

class TransactionReportSerializer(serializers.Serializer):
  transactions = TransactionSerializer(many=True)
  balance = serializers.DecimalField(max_digits=10, decimal_places=2)
  total_in = serializers.DecimalField(max_digits=10, decimal_places=2)
  total_out = serializers.DecimalField(max_digits=10, decimal_places=2)