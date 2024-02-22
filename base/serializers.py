from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import Users,ChildInformation,Reports,MissingPersons,Alerts

#serializers 
class UsersSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'username', 'email', 'bio', 'role')

class UserDetsilserializer(ModelSerializer):
    model = Users
    fields= "__all__" # type: ignore
       

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