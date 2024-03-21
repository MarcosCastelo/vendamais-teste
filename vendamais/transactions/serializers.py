from rest_framework import serializers
from transactions.models import Transaction

from accounts.serializers import AccountSerializer

class TransactionSerializer(serializers.ModelSerializer):
  source_account = AccountSerializer(read_only=True)
  destination_account = serializers.SerializerMethodField()
  class Meta:
    model = Transaction
    fields = ['id', 'transaction_type', 'source_account', 'destination_account', 'amount', 'created_at']
    read_only_fields = ['id', 'created_at']
    
  def get_destination_account(self, obj):
    if obj.destination_account and obj.destination_account.user:
        return obj.destination_account.user.username
    return None

class TransactionReportSerializer(serializers.Serializer):
  transactions = TransactionSerializer(many=True)
  balance = serializers.DecimalField(max_digits=10, decimal_places=2)
  total_in = serializers.DecimalField(max_digits=10, decimal_places=2)
  total_out = serializers.DecimalField(max_digits=10, decimal_places=2)