from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.hashers import make_password,check_password
import random
import string
from django.http import JsonResponse
from rest_framework import generics, status
salt='ee4b2d2eff3c47b590cb8dbcdd53cbcd'

#tables for all the users
class User(AbstractUser):
    ACCOUNT_TYPES = [
        ('Patient', 'Patient'),
        ('Doctor', 'Doctor'),
        ('Admin', 'Admin'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)  
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, default='Patient',null=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    appointments = models.ManyToManyField('Appointment', related_name='patients', blank=True)
    isDeleted = models.BooleanField(default=False)
    
    def clean(self):
        password=make_password(self.password)
        self.password=password
        if self.username=='':
            random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
            username = f"{self.first_name}{random_str}"
            self.username = username
        
        if self.account_type != 'Doctor':
            self.specialization = None
        super().clean()
       
    def checking(self, new_password):
        print(check_password(new_password,self.password))
        if check_password(new_password,self.password):
            return None
        else:
            self.password=make_password(new_password)
            return self.password

    def __str__(self):
        return self.first_name

    

#table for appointments
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_appointments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments')
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Appointment {self.id}"
    
    def clean(self):
    # validation for appointment is in future or not
        if self.appointment_date < timezone.now():
            raise ValidationError("Appointment date must be in the future.")
