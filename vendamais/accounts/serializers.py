from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import Account
from common.error_handler import ErrorHandler

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
  cpf = serializers.CharField(max_length=11, allow_blank=False, required=True)
  password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
  
  class Meta:
    model = User
    fields = ('username', 'password', 'cpf', 'email')

  @transaction.atomic
  def create(self, validated_data):
    user = User.objects.create_user(
      username=validated_data['username'],
      email=validated_data.get('email'),
      cpf=validated_data.get('cpf')
    )
    user.set_password(validated_data['password'])
    user.save()
    Account.objects.create(user=user)
    return user
  
class LoginSerializer(serializers.Serializer):
  username = serializers.CharField(required=True)
  password = serializers.CharField(required=True, write_only=True)
  
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
  @classmethod
  def get_token(cls, user):
    token = super().get_token(user)
    return token
  
  def validate(self, attrs):
    data = super().validate(attrs)
    
    try:
      account = Account.objects.get(user=self.user)
      user_details = {
        'username': self.user.username,
        'cpf': self.user.cpf,
        'balance': account.balance,
        'is_active': account.is_active
      }
    except Account.DoesNotExist:
      raise ErrorHandler("Account not found.", code=404)
    
    data.update({'user': user_details})
    return data
  
class AccountSerializer(serializers.ModelSerializer):
  cpf = serializers.SerializerMethodField()
  username = serializers.SerializerMethodField()
  class Meta:
    model = Account
    fields = ['id', 'balance', 'cpf', 'username']
  
  def get_username(self, obj):
    return obj.user.username
    
  def get_cpf(self, obj):
    return obj.user.cpf