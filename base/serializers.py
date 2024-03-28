from dataclasses import fields
from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import CustomUserManager, UserProfile, UserProfile,ChildInformation,Reports,MissingPersons,Alerts, CustomUser, CustomUserManager

#serializers 
class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomUsermanagerSerializer(ModelSerializer):
    class Meta:
        model = CustomUserManager
        fields = '__all__'


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields ='__all__'

class UserDetailserializer(ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['bio']
       

class ChildInformationSerializer(ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = ChildInformation
        fields = "__all__"


class MissinpersonSerializer(ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = MissingPersons
        fields ='__all__'



class ReportsSerializer(ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model= Reports
        fields = "__all__"


class MissingpersonreportSerializer(ModelSerializer):
    user= CustomUserSerializer()
    missing_person = MissinpersonSerializer()
    class Meta:
        model = Reports
        exclude = ['child']


class MissingchildreportSeriallzer(ModelSerializer):
    User=CustomUserSerializer()
    child = ChildInformationSerializer()
    class Meta:
        model = Reports
        exclude =['missing_person']

class AlertsSerializer(ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = Alerts
        fields = '__all__'