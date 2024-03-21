from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from common.error_handler import ErrorHandler
from transactions.serializers import TransactionSerializer, TransactionReportSerializer
from transactions.services import TransactionService

transaction_service = TransactionService()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit_view(request):
  try:
    account_id = request.user.account.id
    amount = request.data.get('amount')
    
    transaction = transaction_service.deposit(account_id, float(amount))
    transaction_data = TransactionSerializer(transaction).data
    
    return Response({
      "message": "Deposit successful.",
      "transaction": transaction_data
    }, status=status.HTTP_200_OK)
  except ErrorHandler as e:
    return Response(e.to_dict(), status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def withdraw_view(request):
  try:
    account_id = request.user.account.id
    amount = request.data.get('amount')
    
    transaction = transaction_service.withdraw(account_id, float(amount))
    transaction_data = TransactionSerializer(transaction).data
    
    return Response({
      "message": "Withdraw successful.",
      "transaction": transaction_data
    }, status=status.HTTP_200_OK)
  except ErrorHandler as e:
    return Response(e.to_dict(), status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer_view(request):
  try:
    source_account_id = request.user.account.id
    destination_account_cpf = request.data.get('destination_cpf')
    amount = request.data.get('amount')
      
    transaction = transaction_service.transfer(source_account_id, destination_account_cpf, float(amount))
      
    transaction_data = TransactionSerializer(transaction).data
    
    return Response({
      "message": "Transfer successful.",
      "transaction": transaction_data
    }, status=status.HTTP_200_OK)
  except ErrorHandler as e:
    return Response(e.to_dict(), status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_report(request):
  account_id = request.user.account.id
  time_frame = request.query_params.get('time_frame', '24h')

  transactions_data = transaction_service.report(account_id, time_frame)

  serializer = TransactionReportSerializer({
      'transactions': transactions_data['transactions'],
      'balance': transactions_data['balance'],
      'total_in': transactions_data['total_in'],
      'total_out': transactions_data['total_out'],
  })
  
  return Response(serializer.data)
  