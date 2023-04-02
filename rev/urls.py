from django.urls import path
from . import views


app_name = 'rev'

urlpatterns = [
    path('data',views.data,name="data"),
    path('result',views.result,name="result"),
]
