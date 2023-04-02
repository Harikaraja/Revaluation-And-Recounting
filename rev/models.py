from django.db import models

# Create your models here.
class Revaluation(models.Model):
    Application_type=models.CharField(max_length=100)
    Hallticket=models.CharField(max_length=20)
    Student_Name=models.CharField(max_length=250)
    Subject_code=models.CharField( max_length=50)
    Subject=models.CharField(max_length=200)
    Mobile=models.CharField(max_length=10)
    Dhondi_id=models.IntegerField()
    Amount=models.IntegerField()
    Internal_marks=models.IntegerField()
    External_marks=models.IntegerField()
    Second_evaluation=models.IntegerField(null=True,blank=True)
    Third_evaluation=models.IntegerField(null=True,blank=True)
    Credits=models.IntegerField()
    Grades=models.CharField(max_length=2)
    Revaluation_Status=models.CharField(max_length=20)