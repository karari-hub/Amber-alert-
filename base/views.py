from email.mime import image
from inspect import isasyncgenfunction
from urllib import response
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

#rest framework 
#rest decorators (view&class bassed)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

#authorization
from .decorators import allowed_users

#login 
from base.forms import createUserForm
from django.contrib import messages
from django.contrib.auth import  authenticate , logout 
from django.contrib.auth.decorators import login_required

#models
from .models import CustomUser,CustomUserManager, LocationData, Messages,UserProfile, ChildInformation,MissingPersons,Reports,Alerts
from django.db.models import Q

#serializers
from base import serializers
from .serializers import CustomUserSerializer,CustomUsermanagerSerializer,UserProfileSerializer,ChildInformationSerializer, UserDetailserializer, ReportsSerializer,MissinpersonSerializer,MissingchildreportSeriallzer,MissingpersonreportSerializer,AlertsSerializer,LocationSerializer

#CUSTOM TOKEN IMPORT 
# from django.contrib.auth.models import User,AbstractBaseUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

#import forms
from django.contrib.auth.forms import UserCreationForm

#import geohash for alert filtering 
from geohash2 import encode , decode

# Create your views here.

#SIMPLE JWT CUSTOMIZING TOKEN CLAIM
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.get_email_field_name
        # ...

        return token
    
class MyTokenObtainPairview(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

#LOGIN/LOGOOUT/REGISTRATION AND AUTHORIZATION
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response (status= status.HTTP_200_OK )
            else:
                return Response ( status= status.HTTP_400_BAD_REQUEST )

    return


@api_view(['POST'])
def sign_up(request):
    if request.user.is_authenticated:
        return redirect ('login')
    else:

        form = createUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('email')
            messages.success(request, f'account was successfully created for {user}')
        return Response (status= status.HTTP_200_OK)

@api_view(['POST'])
def logoutuser(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)






#CRUD OPERATIONS

#reminder "add image upload function and connect it to s3"
@api_view(['GET'])
def endpoints(request):
    data =['/userprofile','/userprofile/:username', '/child details','/reports', '/missing person','/alerts', '/login', '/logout', '/signup']
    return Response (data)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_roles=[])
def users_list(request):
    if request.method == 'GET':
        users = UserProfile.objects.all()
        serilaizer = UserProfileSerializer(users, many=True)
        return Response(serilaizer.data)
    
    if request.method =='POST':
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()        
            return redirect('users')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET','PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_roles=[]) 
def user_details(request, username):
    user = get_object_or_404(UserProfile, username=username)

    if request.method =='GET':
        serializer = UserDetailserializer(user)
        return Response(serializer.data)
                                         
            
    
    if request.method =='PUT':
        serializer = UserDetailserializer(user, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    if request.method == 'DELETE':
    
        user.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

        

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_roles=[])
def child_details(request):
 
    if request.method == 'GET':
        query = request.GET.get('query')
        if query == None:
            query = ''
            child_information = ChildInformation.objects.filter(Q(child_name__icontains = query)|(Q(physical_description__icontains=query))|(Q(parent_contact__icontains=query)))        
        serializer = ChildInformationSerializer(child_information, many=True)
        return Response(serializer.data)
        
    if request.method =='POST':
        child_information = ChildInformation.objects.create(
            child_name =request.data['child name'],
            date_of_birth = request.data['date of birth'],
            gender = request.data['gender'],
            missingperson_image= request.data['missingperson_image'],
            physical_description =request.data['physical description'],
            location = request.data['location'],
            parent_contact = request.data['parent contact'],

        )

        serializer = ChildInformationSerializer(child_information, many=False)
        return redirect ('childdetails')


@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_roles=['admin','lawenforcer', 'parent','guardian'])
def individual_child_details(request, child_name):
    child_information = ChildInformation.objects.get(child_name=child_name)
    
    
    if request.method =='GET':
        serializer = ChildInformationSerializer(child_information, many=False)
        return Response(serializer.data)

    if request.method == 'PUT':
        child_information.child_name = request.data['child_name']
        child_information.location = request.data['location']
        child_information.date_of_birth = request.data['date_of_birth']
        child_information.gender = request.data['gender']
        child_information.physical_description = request.data['physical_description']
        child_information.parent_contact = request.data['parent_contact']

        
        serializer = ChildInformationSerializer(child_information, many=False)
        return Response(serializer.data)

    if request.method == 'DELETE':        
        child_information.delete()
        return redirect('childdetails')


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_roles=[])
def missing_person_details(request):

    if request.method == 'GET':
        query= request.GET.get('query')
        if query == None:
            query=''
        missing_person = MissingPersons.objects.filter(Q(name__icontains=query)|(Q(physical_description__icontains=query))|(Q(family_contact__icontains=query)))
        serializer = MissinpersonSerializer(missing_person, many=True)
        return Response (serializer.data)

        
    if request.method == 'POST':
        missing_person = MissingPersons.objects.create(
            name = request.data['name'],
            date_of_birth= request.data['date of birth'],
            gender = request.data['gender'],
            missingperson_image = request.data['missingperson_image'],
            physical_description= request.data['physical description'],
            family_contact = request.data['family contact']

        )
        serializer= MissinpersonSerializer(missing_person,many=False)
        return Response(serializer.data)    
    


@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_roles=[])
def individual_missing_person(request, name):
    missing_person = MissingPersons.objects.get(name=name)
    
    if request.method == 'GET':
        serializer = MissinpersonSerializer(missing_person, many=False)
        return Response(serializer.data)

    if request.method =='PUT':
        missing_person.name = request.data['name']
        missing_person.location = request.data['location']
        missing_person.date_of_birth = request.data['date of birth']
        missing_person.gender = request.data['gender']
        missing_person.physical_description = request.data['physical description']
        missing_person.family_contact=request.data['family_contact']


        serializer= MissinpersonSerializer(missing_person, many = False)
        return Response (serializer.data)
    
    if request.method == 'DELETE':
        missing_person.delete()
        return redirect('missingperson')


    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def reports(request):
    report= Reports.objects.all()

    if request.method =='GET':
        query= request.GET.get('query')
        if query == None:
            query=''
        report = Reports.objects.filter(Q(name__icontains=query)|(Q(child=query))|(Q(missing_person=query)))        
        serializer = ReportsSerializer(report, many=False)
        
        return Response(serializer.data)
    
    
    if request.method =='POST':
        report = Reports.objects.create(
            child = request.data['child'],
            missing_person = request.data['missig person'],
            missingperson_image = request.data['missingperson_image'],
            repot_type = request.data['report type'],
            report_body = request.data['report body'],
            location = request.data['location'],
            contact_information= request.data['contact information'],
            police_report_number = request.data['police report number']
            
        )
        
        serializer = ReportsSerializer(report, many = False)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        report = Reports.objects.update(
            child = request.data['child'],
            missing_person = request.data['missig person'],
            missingperson_image = request.data['missingperson_image'],
            image  = request.data['missingperson_image'],
            repot_type = request.data['report type'],
            report_body = request.data['report body'],
            location = request.data['location'],
            contact_information= request.data['contact information'],
            police_report_number = request.data['police report number']
        )
        
        serializer = ReportsSerializer(report, many = False)
        return Response(serializer.data)
    
    if request.method == 'DELETE':
        report.delete()
        return redirect('reports')

    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def report_types(request, report_type):
        
    if request.method =='GET':    
        report = Reports.objects.get(report_type=report_type)
        if report_type == 'Missing child':
            serializer = MissingchildreportSeriallzer(report, many=True)
        if report_type == 'Missing person':
            serializer = MissingpersonreportSerializer(report,many=True)
        
        
        return Response(serializer.data)






@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def alerts(request):
    def filter_alerts(user_latitude, user_longitude, user_precision, alerts):
        user_geohash = encode (user_latitude,user_longitude, precision=user_precision)
        filtered_alerts = []
        
        for alert in alerts:
            alert_latitude, alert_longitude = alert.latitude, alert.longitude
            alert_geohash = encode (alert_latitude,alert_longitude, precision=user_precision)
            if alert_geohash == user_geohash:
                filtered_alerts.append(alert)
        return filtered_alerts
    
    if request.method =='GET':
        user_latitude = float(request.query_params.get('latitude',0.0))
        user_longitude = float(request.query_params.get('longitude',0.0))
        user_precision =  int(request.query_params.get('precision', 7))
        
        alerts = Alerts.objects.all()
        filtered_alerts = filter_alerts(user_latitude, user_longitude, user_precision, alerts)
        serializer = AlertsSerializer(filtered_alerts)
        return Response(serializer.data)
    
    

    

        
        




        


 

