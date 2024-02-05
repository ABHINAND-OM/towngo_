from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('userregister/', views.userregister, name="uregister"),
    path('userlogin/', views.userlogin, name="userlogin"),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('contactus/', views.contactus,name="contactus"),
    path('services/', views.services,name='services'),
    path('tire/', views.tire,name="tire")

]
