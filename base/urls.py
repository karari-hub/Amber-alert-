from django.urls import path
from . import views

#simplejwt authentification 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    # TokenRefreshView,
)

#url patterns 
urlpatterns =[
    #endpoint urls
    path('', views.endpoints),

    #token views
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 


    #view urls
    path('users/', views.users_list, name='users'),
    path('users/<username>/', views.user_details, name= 'userdetails '),
    path('child details/', views.child_details, name='childdetails'),
    path('child details/<child_name>/', views.individual_child_details, name='individualchilddetails'),
    path('reports/',views.reports, name = 'reports'),
    path('reports/<report_type>', views.report_types, name='reporttypes'),
    path('missing person/', views.missing_person_details, name='missingperson'),
    path('missing person/<name>/', views.individual_missing_person, name='individualmissingperson'),
    path('alerts/', views.alerts, name='alerts')

]