from django.db import models

# Create your models here.
class orginal_Result(models.Model):
    Hallticket = models.CharField(max_length=20)
    Name = models.CharField(max_length=250)
    subject_code = models.CharField(max_length=30)
    subject_type = models.CharField(max_length=50)
    subject_name = models.CharField(max_length=50)
    Internal = models.IntegerField()
    External = models.IntegerField()
    Total = models.IntegerField()
    grade_letter = models.CharField(max_length=2)
    credits = models.IntegerField()

class Revaluation(models.Model):
    Application_type=models.CharField(max_length=100)
    Hallticket=models.CharField(max_length=20)
    Student_Name=models.CharField(max_length=250)
    Subject_code=models.CharField( max_length=50)
    Subject=models.CharField(max_length=200)
    Mobile=models.CharField(max_length=10)
    Dhondi_id=models.IntegerField()
    Amount=models.IntegerField()
    


class Regulations_with_Grades(models.Model):
    Regulation=models.CharField(max_length=20)
    Lower_limit=models.IntegerField()
    Upper_limit=models.IntegerField()
    Grades=models.CharField(max_length=2)


class Subject_max_marks(models.Model):
    Subject_codes=models.CharField(max_length=50)
    Subjects=models.CharField(max_length=50)
    Brach_code=models.CharField(max_length=20)
    Max_marks=models.IntegerField()
    Max_Total_marks=models.IntegerField()
    Max_internal=models.IntegerField()
    Min_external=models.IntegerField()
    Credit=models.IntegerField()
    Subject_type=models.IntegerField()

class Revaluation_copy(models.Model):
    Hallticket=models.CharField(max_length=20)
    Student_Name=models.CharField(max_length=250)
    Subject_code=models.CharField( max_length=50)
    Subject=models.CharField(max_length=200)
    Internal_marks=models.IntegerField(null=True,blank=True)
    External_marks=models.IntegerField(null=True,blank=True)
    Second_evaluation=models.IntegerField(null=True,blank=True)
    Third_evaluation=models.IntegerField(null=True,blank=True)
    Credits=models.IntegerField(null=True,blank=True)
    Grades=models.CharField(max_length=2,null=True,blank=True)
    Revaluation_Status=models.CharField(max_length=20)

    

