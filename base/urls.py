from django.urls import path
from . import views
from .views import MyTokenObtainPairview

#simplejwt authentification 
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

#url patterns 
urlpatterns =[
    #endpoint urls
    path('', views.endpoints),

    #token views
    path('token/', MyTokenObtainPairview.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 

    #login , logout and signup views
    # path('login/', views.login, name='login'),
    # path('logout/', views.logout, name='logout'),
    # path('sign_up/', views.sign_up, name='sign up'),

    #crud view urls
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