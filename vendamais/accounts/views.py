from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from common.error_handler import ErrorHandler
from accounts.serializers import RegisterSerializer, CustomTokenObtainPairSerializer

@api_view(['POST'])
def register_view(request):
  try:
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
  except ErrorHandler as e:
    return Response(e.to_dict(), status=e.code if e.code else status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
  serializer = CustomTokenObtainPairSerializer(data=request.data)

  if serializer.is_valid(raise_exception=True):
      return Response(serializer.validated_data, status=status.HTTP_200_OK)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)