from rest_framework import serializers,status
from sche.models import *
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from sche.tests import *
from django.http import JsonResponse

class user_serializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('first_name','last_name','email','account_type','specialization')


class appointment_serializer(serializers.ModelSerializer):
    class Meta:
        model=Appointment
        fields=('patient','doctor','appointment_date','status')

class registration_serializer(serializers.ModelSerializer):
    # Define a specialization field that is conditionally included
    account_type = serializers.ChoiceField(choices=User.ACCOUNT_TYPES)
    specialization = serializers.CharField(allow_null=True, allow_blank=True)
    class Meta:
        model=User
        fields=('first_name','last_name','email','password','account_type','specialization')
  

class login_serializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()

salt='ee4b2d2eff3c47b590cb8dbcdd53cbcd'
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()  

    def reset_password_email(self):
        email = self.validated_data['email']
        user=User.objects.get(email=email)
        
        # Generate a password reset token
        token=create_token(user,salt)

        # Construct the password reset URL
        reset_url = f"http://127.0.0.1:8000/api/password/reset/{token}/"

        # Send the password reset email
        subject = 'Password Reset'
        message = f'Click the following link to reset your password: {reset_url}'
        from_email = 'rahul2210085@akgec.ac.in'
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return True  
    


class PasswordResettokenSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)    
    