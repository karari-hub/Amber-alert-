from email.policy import default
from enum import unique
from sys import maxsize
from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

# Create your models here.

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_parent=False, is_guardian=False, is_law_enforcer=False, **extra_fields):
        if not email or not password:
            raise ValueError("Please provide a valid email address and password")

        if is_law_enforcer:
            extra_fields.setdefault('is_admin', True)
            extra_fields.setdefault('is_staff', True)
            

         
         
        user = self.model(
            email=self.normalize_email(email),
            is_active=is_active,
            is_parent=is_parent,
            is_guardian=is_guardian,
            is_law_enforcer=is_law_enforcer,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255, null=False)
    fullname = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)
    is_guardian = models.BooleanField(default=False)
    is_law_enforcer = models.BooleanField(default=False)
    is_citizen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    module_perms = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = 'base_customuser'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
    
    
class Images(models.Model):
    missingperson_image = models.ImageField(null=True, blank=True, upload_to=upload_to)
    profile_image=models.ImageField(null=True, blank=True, upload_to=upload_to)
    
    def __str__(self):
        return self.missingperson_image and self.profile_image



class LocationData(models.Model):
    user_location = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    country = models.CharField(max_length=255, null=True)
    county = models.CharField(max_length=255, null=True)
    district = models.CharField(max_length=255, null=True)
    division = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    sublocation = models.CharField(max_length=255, null=True)
    town = models.CharField(max_length=255, null=True)
    
    latitude = models.FloatField(null = True,blank=True)
    logitude = models.FloatField(null = True, blank=True)

    def __str__(self):
        return self.county


class UserProfile(models.Model):

    username = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    bio = models.TextField(max_length=255, null=True, blank=True)
    profle_image = models.ForeignKey(Images, null=True, on_delete=models.SET_NULL)
    user_location = models.ForeignKey(LocationData, null=True, on_delete=models.SET_NULL, blank=True)
    def __str__(self):
        return str(self.username)



class ChildInformation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    child_name = models.CharField(max_length=255, null=True)
    location = models.ForeignKey(LocationData, on_delete=models.SET_NULL, null=True)
    date_of_birth = models.DateTimeField()
    gender = models.CharField(max_length=50, null=True)
    physical_description = models.TextField()
    parent_contact = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.child_name} {self.date_of_birth}"

class MissingPersons(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(LocationData, on_delete=models.SET_NULL, null=True)
    missingperson_image = models.ForeignKey(Images, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255, null=True)
    date_of_birth = models.DateTimeField()
    gender = models.CharField(max_length=50)
    physical_description = models.TextField(max_length=255, null=True)
    family_contact = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class Reports(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255, null=True,blank=True)
    child = models.ForeignKey(ChildInformation, on_delete=models.SET_NULL, null=True, blank=True)
    missing_person = models.ForeignKey(MissingPersons, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(LocationData, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    report_types = [
        ("Missing child", "Missing child"),
        ("Missing Person", "Missing person"),
    ]
    report_type = models.CharField(max_length=50, choices=report_types)
    report_body = models.TextField(blank=True, null=True)
    contact_information = models.CharField(max_length=255, blank=True, null=True)
    police_report_number = models.CharField(max_length=255, null=True)
    
    class Meta:
        ordering = ('-created','-updated')

    def __str__(self):
        return f"{self.report_type} {self.report_body}"

class Alerts(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(LocationData, on_delete=models.SET_NULL, null=True)
    alert_title = models.CharField(max_length=255, null=True)
    alert_types = [
        ("Missing_person", "Missing person"),
        ("Missing_child", "Missing child")
    ]
    alert_type = models.CharField(max_length=50, null=True, choices=alert_types)
    alert_body = models.TextField(max_length=255, null=True)
    report = models.ForeignKey(Reports, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    STATUS = [
        ("Pending", "Pending"),
        ("Found", "Found")
    ]
    status = models.CharField(max_length=50, choices=STATUS, null=True)
    
    class Meta:
        ordering = ('-created','-updated')

    def __str__(self):
       return f'{self.alert_title} {self.alert_type} {self.alert_body} {self.created} {self.updated}'
    
class Messages(models.Model):
   user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
   report = models.ForeignKey(Reports, on_delete=models.SET_NULL, null=True)
   alerts =models.ForeignKey(Alerts, on_delete=models.SET_NULL, null=True)
   created = models.DateTimeField(auto_now_add=True)
   updated = models.DateTimeField(auto_now=True)
   body = models.CharField(max_length=255,null=True, blank=True)
   
   class Meta:
       ordering = ('-updated',)


   def __str__(self):
      return self.body
  
