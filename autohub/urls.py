from django.urls import path
from . import views
from .views import delete_request

urlpatterns = [
    path('', views.hubregister,name="hubregister"),
    path('hublogin/', views.hublogin, name="hublogin"),
    path('hubindex/', views.hubindex, name="hubindex"),
    path('hublogout/', views.hublogout, name="hublogout"),
    path('hubcollection/', views.hubcollection, name="hubcollection"),
    path('delete_request/<int:id>/', delete_request, name='delete_request'),

    path('hubprofileedit/', views.hubprofileedit, name='hubprofileedit'),
    path('hubprofile/', views.hubprofile, name='hubprofile'),
    path('get_nearest_autohub/', views.get_nearest_autohub, name="get_nearest_autohub"),
    path('add_mechanic/', views.add_mechanic, name="add_mechanic"),
    path('mechanic_list/', views.mechanic_list, name='mechanic_list'),
    # path('your-api-endpoint/<int:mechanic_id>/', views.delete_mechanic, name='delete_mechanic'),

    path('assign_mechanic/<int:request_id>/', views.assign_mechanic, name='assign_mechanic'),


]