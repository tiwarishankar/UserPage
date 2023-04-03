from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.authtoken.models import Token
import json
from rest_framework import generics ,permissions
from rest_framework.decorators import *
from .serializers import UserSerializer , UserEditInfoSerializer, UserDataSerializer
from api.models import *

class RegisterAPIView(APIView):
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            data : dict = json.loads(request.body)
            assert data["username"] and data["password"] and data["email"] and data["phone_number"], KeyError()
            username = data["username"]
            password = data["password"]
            email = data["email"]
            phone_number = data["phone_number"]
            user = Account.objects.filter(username=username) or Account.objects.filter(email=email) or Account.objects.filter(phone_number=phone_number)
            if user:
                return Response({"error" : "Account already exist with given username or email"}, status=HTTP_403_FORBIDDEN)
            account = Account.objects.create(**data)
            account.set_password(password)
            account.is_active = True
            account.save()
            token = Token.objects.create(user=account)
            return Response({'token': token.key, 'phone_number': account.phone_number, 'username': account.username, 'email': account.email},
                            status=HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"error" : "Invalid Fields"}, status=HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        data: dict = json.loads(request.body)
        accounts = Account.objects.filter(
            username=data['username'])
        if not accounts.exists():
            return Response({'error': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)
        account: Account = accounts.first()
        token: Token = Token.objects.get(user=account)
        if not account.check_password(data['password']) or not token:
            return Response({"error": "Invalid Credentials"}, status=HTTP_401_UNAUTHORIZED)
        return Response({'email': account.email, 'token': token.key, 'phone_number': account.phone_number, 'username': account.username, }, status=HTTP_200_OK)



class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    queryset = Account.objects.all()
    
    def list(self, request, query):
        data = self.get_queryset().filter(phone_number=query) | self.get_queryset().filter(email=query) | \
            self.get_queryset().filter(username=query)
        response = UserSerializer(data, many=True)
        return Response({"data": response.data})
        


class UserDetail(generics.RetrieveAPIView):
    permission_classes =[permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = UserDataSerializer 
    def get (self, request):
        
        data = Account.objects.filter(username=request.user.username).first()
        response = UserDataSerializer(data)
        return Response({"data":response.data})

class EditUserProfile(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = UserEditInfoSerializer
    def edit_user_info(self,request):
        response = UserEditInfoSerializer(data=request.data)
        if response.is_valid():
            response.save()
            return Response(response.data)
        else:
            return Response(response.errors, status=HTTP_400_BAD_REQUEST)

