from dataclasses import fields
from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import Users,ChildInformation,Reports,MissingPersons,Alerts, CustomUser, UserManager

#serializers 
class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class UsermanagerSerializer(ModelSerializer):
    class Meta:
        model = UserManager
        fields = '__all__'


class UsersSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields =('username', 'email', 'bio', 'role')

class UserDetailserializer(ModelSerializer):
    class Meta:
        model = Users
        exclude = ['bio']
       

class ChildInformationSerializer(ModelSerializer):
    user = UsersSerializer()
    class Meta:
        model = ChildInformation
        fields = "__all__"


class MissinpersonSerializer(ModelSerializer):
    user = UsersSerializer()
    class Meta:
        model = MissingPersons
        fields ='__all__'



class ReportsSerializer(ModelSerializer):
    user = UsersSerializer()
    class Meta:
        model= Reports
        fields = "__all__"


class MissingpersonreportSerializer(ModelSerializer):
    user=UsersSerializer()
    missing_person = MissinpersonSerializer()
    class Meta:
        model = Reports
        exclude = ['child']


class MissingchildreportSeriallzer(ModelSerializer):
    User=UsersSerializer()
    child = ChildInformationSerializer()
    class Meta:
        model = Reports
        exclude =['missing_person']

class AlertsSerializer(ModelSerializer):
    user =UsersSerializer()
    class Meta:
        model = Alerts
        fields = '__all__'