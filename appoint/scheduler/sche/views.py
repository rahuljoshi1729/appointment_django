from rest_framework import generics, status
from rest_framework.response import Response
from sche.models import *
from sche.serializers import *
import uuid
from rest_framework.views import APIView
from rest_framework.views import Response
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
import logging

from sche.models import User
from .serializers import PasswordResetSerializer

from sche.tests import *



class registration_api(APIView):
    def post(self,request):
        try:
            data=request.data
            serializer=registration_serializer(data=data)
            if serializer.is_valid():
                email=serializer.validated_data['email']
                if User.objects.filter(email=email).exists():
                    return JsonResponse({"error":"email already exists"},status=status.HTTP_400_BAD_REQUEST)
                else:
                    user=User(**serializer.validated_data)
                    user.clean()
                    user.save()
                    return JsonResponse({"message":"user created successfully"},status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return JsonResponse({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)    


class login_api(APIView):
    def post(self,request):
        try:
            data=request.data
            serializer=login_serializer(data=data)
            if serializer.is_valid():
                email=serializer.validated_data['email']
                password=serializer.validated_data['password']
                user=authenticate(email=email,password=password)
                
                if user is None:
                    logging.error("Authentication failed for email: {} {} {}".format(email,password,user))
                    return Response({
                            'status':400,
                            'message':'invalid password or email',
                            'data':{}
                    })
                    
                refresh = RefreshToken.for_user(user)
                return  Response({ 
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    })


            return Response({
                'status':400,
                'message':'invalid input',
                'data':{}
            })
        
        except Exception as e:
            print(e)
            return Response({
                'status': 500,
                'message': 'Internal server error',
                'data': {}
            })


# to get the list of doctors or patient
class ListAPI(APIView):
    def get(self, request,type):
        try:
            if type=="doctor":
                if User.objects.filter(account_type="Doctor").exists():
                    return JsonResponse({"data":user_serializer(User.objects.filter(account_type="Doctor"),many=True).data},status=status.HTTP_200_OK)
                else:
                    return JsonResponse({"message":"No doctor found"},status=status.HTTP_404_NOT_FOUND)
            elif type=="patient":
                    if User.objects.filter(account_type="Patient").exists():
                        return JsonResponse({"data":user_serializer(User.objects.filter(account_type="Patient"),many=True).data},status=status.HTTP_200_OK)
                    else:
                        return JsonResponse({"message":"No patient found"},status=status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse({"message":"Invalid type"},status=status.HTTP_400_BAD_REQUEST)        
        except Exception as e:
            print(e)
            return Response({
                'status': 500,
                'message': 'Internal server error',
                'data': {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     


# to reset the password
class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if not User.objects.filter(email=email).exists():
                return Response({"message": "user not found"},status=status.HTTP_404_NOT_FOUND)
            
            serializer.reset_password_email()
            return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


salt='ee4b2d2eff3c47b590cb8dbcdd53cbcd'
class PasswordResetConfirmView(APIView):
    def post(self, request, token):
        a=decode_token(token)
        if a is None:
            return JsonResponse({"message":"Invalid token"},status=status.HTTP_400_BAD_REQUEST)
        
        serializer = PasswordResettokenSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            if User.objects.get(pk=a):
                user=User.objects.get(pk=a)
                b=user.checking(new_password)
                if b is None:
                    return JsonResponse({"message":"same password"},status=status.HTTP_400_BAD_REQUEST)
                user.save()
                return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)