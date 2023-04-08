from django.urls import path
from . import views


app_name = 'rev'

urlpatterns = [
    path("",views.home),
    
    path('data',views.data,name="data"),
    path('result',views.result,name="result"),
    path('Third_eval',views.Third_eval,name="Third_eval")
]
