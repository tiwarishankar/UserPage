from rest_framework import serializers
from .models import Account

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username' ,'phone_number','email' ]
        
class UserEditInfoSerializer(serializers.ModelSerializer):
    class Meta:
         model = Account
         fields= '__all__'
         
class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
         model = Account
         fields = '__all__'