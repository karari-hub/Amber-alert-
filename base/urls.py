from django.urls import path
from . import views
from .views import MyTokenObtainPairview

#password reset import
from django.contrib.auth import views as auth_views

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

    # login , logout and signup views
    path('login/', views.login, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('sign_up/', views.sign_up, name='signup'),
    
    

    #crud view urls
    path('userprofile/', views.users_list, name='userprofile'),
    path('userprofile/<username>/', views.user_details, name= 'userprofiledetails '),
    path('child details/', views.child_details, name='childdetails'),
    path('child details/<child_name>/', views.individual_child_details, name='individualchilddetails'),
    path('reports/',views.reports, name = 'reports'),
    path('reports/<report_type>', views.report_types, name='reporttypes'),
    path('missing person/', views.missing_person_details, name='missingperson'),
    path('missing person/<name>/', views.individual_missing_person, name='individualmissingperson'),
    path('alerts/', views.alerts, name='alerts'),


    #reset password urls (classbasesviews url patterns)
    # (email body template)-Someone asked for password reset for email {{ email }}. Follow the link below:
    #{{ protocol}}://{{ domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}
    
    
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='reset_password_sent'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='reset_password_complete'),
    
]

  
