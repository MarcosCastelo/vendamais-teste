from django.urls import path
from transactions.views import deposit_view, withdraw_view, transfer_view, transaction_report

urlpatterns = [
  path('deposit/', deposit_view, name='deposit'),
  path('withdraw/', withdraw_view, name='withdraw'),
  path('transfer/', transfer_view, name='transfer'),
  path('report/', transaction_report, name='report')
]