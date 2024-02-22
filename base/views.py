from urllib import response
from django.shortcuts import render, redirect
from django.http import JsonResponse
#rest framework 
#rest decorators (view&class bassed)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

#models
from .models import Users,ChildInformation,Reports,MissingPersons,Alerts
from django.db.models import Q

#serializers
from base import serializers
from .serializers import UsersSerializer,ChildInformationSerializer, UserDetsilserializer, ReportsSerializer,MissinpersonSerializer,MissingchildreportSeriallzer,MissingpersonreportSerializer,AlertsSerializer


# Create your views here.
@api_view(['GET'])
def endpoints(request):
    data =['/users','/users/:username', 'child details','reports', 'missing person','alerts']
    return Response (data)

@api_view(['GET','POST'])
def users_list(request):
    if request.method == 'GET':
        query= request.GET.get('query')
        if query == None:
            query = ''
            user=Users.objects.filter(Q(username__icontains=query) | Q(email__icontains=query))

            serilaizer = UsersSerializer(user, many=False)
            return Response(serilaizer.data)
    
    if request.method =='POST':
        user = Users.objects.create(
            username = request.data['username'],
            email = request.data['email'],
            role = request.data['role']
        )

        serilaizer = UsersSerializer(user, many=False)
        return redirect('users')

@api_view(['GET','PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
def user_details(request, username):

    if request.method =='GET':
        user = Users.objects.get(username=username)
        serializer= UsersSerializer(user, many=False)
        return Response(serializer.data)
    
    if request.method =='PUT':
        user = Users.objects.get(username=username)
        if user.username == username:
            user= Users.objects.update(
            username = request.data['username'],
            email = request.data['email'],
            bio = request.data['bio'],
            role = request.data['role'])
        
        
        
        serializer = UserDetsilserializer(user, many=False)
        return Response (serializer.data)
    
    if request.method == 'DELETE':
        user = Users.objects.get(username=username)
        user.delete()
        return redirect('userdetails')
        

@api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])
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
            physical_description =request.data['physical description'],
            location = request.data['location'],
            parent_contact = request.data['parent contact'],

        )

        serializer = ChildInformationSerializer(child_information, many=False)
        return redirect ('childdetails')


@api_view(['GET','PUT','DELETE'])

def individual_child_details(request, child_name):
    if request.method =='GET':
        child_information = ChildInformation.objects.get(child_name=child_name)
        serializer = ChildInformationSerializer(child_information, many=False)
        return Response(serializer.data)

    if request.method == 'PUT':
        child_information=ChildInformation.objects.get(child_name=child_name)
        if child_information.child_name == child_name:
            child_information = ChildInformation.objects.update(
            child_name=request.data['child name'],
            location = request.data['location'],
            date_of_birth = request.data['date of birth'],
            gender = request.data['gender'],
            physical_description= request.data['physical description'],
            parent_contact= request.data['parent contact'])

        
        serializer = ChildInformationSerializer(child_information, many=False)
        return Response(serializer.data)

    if request.method == 'DELETE':        
        child_information = ChildInformation.objects.get(child_name= child_name)
        if child_name in child_information == child_name:
            child_information.delete()
        return redirect('childdetails')


@api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])
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
            physical_description= request.data['physical description'],
            family_contact = request.data['family contact']

        )
        serializer= MissinpersonSerializer(missing_person,many=False)
        return Response(serializer.data)    
    


@api_view(['GET','PUT','DELETE'])
def individual_missing_person(request, name):
    if request.method == 'GET':
        missing_person = MissingPersons.objects.get(name=name)
        serializer = MissinpersonSerializer(missing_person, many=False)
        return Response(serializer.data)

    if request.method =='PUT':
        missing_person = MissingPersons.objects.get(name=name)
        if missing_person.name == name:
            missing_person = MissingPersons.objects.update(
            name = request.data['name'],
            date_of_birth = request.data['date of birth'],
            gender = request.data['gender'],
            physical_description= request.data['physical description'],
            family_contact= request.data['family contact'])

        serializer= MissinpersonSerializer(missing_person, many = False)
        return Response (serializer.data)
    
    if request.method == 'DELETE':
        missing_person = MissingPersons.objects.get(name=name)
        if name in missing_person == name:
            missing_person.delete()
        return redirect('missingperson')


    
@api_view(['GET', 'POST'])
def reports(request):
    report= Reports.objects.all()

    if request.method =='GET':
        serializer = ReportsSerializer(report, many=True)
        return Response(serializer.data)
    
    if request.method =='POST':
        report = Reports.objects.create(
            child = request.data['child'],
            missing_person = request.data['missig person'],
            repot_type = request.data['report type'],
            report_body = request.data['report body'],
            location = request.data['location'],
            contact_information= request.data['contact information'],
            police_report_number = request.data['police report number']
        )

        serializer = ReportsSerializer(report, many = False)
        return Response(serializer.data)
    

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def report_types(request, report_type):
        
    if request.method =='GET':    
        report = Reports.objects.get(report_type=report_type)
        if report_type == 'Missing child':
            serializer = MissingchildreportSeriallzer(report, many=True)
        if report_type == 'Missing person':
            serializer = MissingpersonreportSerializer(report,many=True)
        
        
        return Response(serializer.data)


@api_view(['GET'])
def alerts(request):

    if request.method =='GET':
      
        alert = Alerts.objects.all()
        serializer = AlertsSerializer(alert,many=True)

        return Response(serializer.data)


