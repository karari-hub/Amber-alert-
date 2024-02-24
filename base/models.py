from email.policy import default
from django.db import models


# Create your models here.
class Users(models.Model):
   ROLES= [
      ("Citizen","Citizen"),
      ("Parent", "parent"),
      ("Guardian","guardian"),
      ("Law_Enforcer","Law enforcer/police"),
   ] 
   
   username= models.CharField(unique=True, max_length=255, null=False)
   email= models.EmailField(unique=True, max_length=255, null=False) 
   bio = models.TextField(max_length=255,null=True, blank=True)

   role =models.CharField(max_length=30, choices=ROLES, null=True) 

   def __str__(self):
      return self.username
   

class Locationdata(models.Model):
   country = models.CharField(max_length=255,null=True)
   county = models.CharField(max_length=255,null=True)
   district = models.CharField(max_length=255,null=True)
   division = models.CharField(max_length=255,null=True)
   location = models.CharField(max_length=255,null=True)
   sublocation = models.CharField(max_length=255, null=True)
   town= models.CharField(max_length=255, null=True)

   def __str__(self):
      return self.country


class ChildInformation(models.Model):
   user= models.ForeignKey(Users,on_delete=models.SET_NULL,null=True,blank=True)
   child_name = models.CharField(max_length=255, null=True)
   location = models.ForeignKey(Locationdata, on_delete= models.SET_NULL, null=True)
   date_of_birth = models.DateField()
   gender = models.CharField(max_length=50, null=True)
   physical_description = models.TextField()
   parent_contact = models.CharField(max_length=255)
   

   def __str__(self):
      return f"{self.child_name} {self.date_of_birth}"



class MissingPersons(models.Model):
   user= models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True)
   location = models.ForeignKey(Locationdata, on_delete=models.SET_NULL,null=True)
   name= models.CharField(max_length=255, null=True)
   date_of_birth = models.DateField()
   gender = models.CharField(max_length=50)
   physical_description = models.TextField(max_length=255, null=True)
   family_contact = models.CharField(max_length=255, null=True,blank=True)

   def __str__(self):
      return self.name   


class Reports(models.Model):
   users = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True)
   child =models.ForeignKey(ChildInformation, on_delete=models.SET_NULL, null=True, blank=True)
   missing_person =models.ForeignKey(MissingPersons, on_delete=models.SET_NULL, null=True, blank=True)
   Location = models.ForeignKey(Locationdata, on_delete=models.SET_NULL,null=True, blank=True)
   created = models.DateTimeField(auto_now_add=True)
   updated = models.DateTimeField(auto_now=True)
   report_types=[
      ("Missing child","Missing child"),
      ("Missing Person", "Missing person"),
   ]
   report_type=models.CharField(max_length=50,choices=report_types)
   report_body =models.TextField(blank=True, null=True)
   contact_information= models.CharField(max_length=255, blank=True,null=True)
   police_report_number=models.CharField(max_length=255,null=True)
   # images = models.ImageField()

   def __str__(self) -> str:
      return f"{self.report_type} {self.report_body}"


class Alerts(models.Model):
   user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True)
   location = models.ForeignKey(Locationdata, on_delete=models.SET_NULL, null=True)
   alert_tittle = models.CharField(max_length=255, null=True)
   alert_types =[
      ("Missing_person","Missing person"),
      ("Missing_child","Missing child")
                 ]
   alert_type = models.CharField(max_length=50,null=True,choices=alert_types) 
   alert_body = models.TextField(max_length=255,null=True)
   report = models.ForeignKey(Reports,on_delete=models.SET_NULL, null=True, blank=True)
   created = models.DateTimeField(auto_now_add=True)
   updated = models.DateTimeField(auto_now=True)
   STATUS = (
      ("Pending", "Pending"),
      ("Found", "Found")
   ) 
   status = models.CharField(max_length=50, choices= STATUS, null=True)

   def __str__(self):
      return self.alert_tittle 
   

class Messages(models.Model):
   user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
   report = models.ForeignKey(Reports, on_delete=models.SET_NULL, null=True)
   alerts =models.ForeignKey(Alerts, on_delete=models.SET_NULL, null=True)
   created = models.DateTimeField(auto_now_add=True)
   updated = models.DateTimeField(auto_now=True)
   body = models.CharField(max_length=255,null=True, blank=True)


   def __str__(self):
      return self.body


class AlertRecipients(models.Model):
   user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
   alert = models.ForeignKey(Alerts, on_delete=models.SET_NULL,null=True)

   def __str__(self):
      return self
   

