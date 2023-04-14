from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from django.urls import reverse
from django.db.models import Case, When
from .forms import UploadForm
import csv
# Create your views here.
def home(request):
    status=0
    message = ''
    
    if request.method == 'POST':

        
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            
            file = form.cleaned_data['file']
            Revaluation.objects.all().delete()
            Revaluation_copy.objects.all().delete()
            csv_data = csv.reader(file.read().decode('utf-8').splitlines())
            for columns in csv_data:
                revaluation = Revaluation(id=columns[0],Application_type=columns[1], Hallticket=columns[2],Student_Name=columns[3],Subject_code=columns[4],Subject=columns[5],Mobile=columns[6],Dhondi_id=columns[7],Amount=columns[8],Internal_marks=columns[9],External_marks=columns[10],Credits=columns[11],Grades=columns[12],Revaluation_Status=columns[13])
                revaluation_copy = Revaluation_copy(id=columns[0] ,Hallticket=columns[2],Student_Name=columns[3],Subject_code=columns[4],Subject=columns[5],Internal_marks=columns[9],External_marks=columns[10],Credits=columns[11],Grades=columns[12],Revaluation_Status=columns[13])
                
                revaluation.save()
                revaluation_copy.save()
            revaluation=Revaluation.objects.all()
            
            select_value=request.POST.get('Regulation')
            if select_value == None:
                
                message='Please Select the Regulation'
                context = {'message': message,'status':status}
                return render(request, 'home.html',context)
            
            revaluation=Revaluation_copy.objects.all()
            return render(request,'index.html',{"Revaluation_copy":revaluation,"Regulation":select_value})


        else:
            
            message='Error in Uploading File'
            context = {'message': message,'status':status}
            return render(request, 'home.html',context)
    return render(request, 'home.html')
def data(request):
    revaluation=Revaluation_copy.objects.all()

    if request.method == 'GET':

        return render(request,'index.html',{"Revaluation_copy":revaluation})
    elif request.method == 'POST':
        id=request.POST.getlist('id[]')
        sec_eval=request.POST.getlist('s_eval[]')
        third_eval=request.POST.getlist('t_eval[]')
        #print(id,sec_eval,third_eval)
        for i in range(len(sec_eval)):
            r=Revaluation_copy.objects.filter(id=id[i]).first()
            r.Second_evaluation=sec_eval[i]
            r.Third_evaluation=third_eval[i]
            r.save()
        return HttpResponseRedirect(reverse('rev:Third_eval'))

def result(request):
    Reg=request.GET.get('Regulation')
    results=Revaluation.objects.all()
    #reg_20=Regulations_20.objects.all()
    id=Revaluation_copy.objects.values_list('id',flat=True)
    grades=Revaluation_copy.objects.values_list('Grades',flat=True)
    sec_eval=Revaluation_copy.objects.values_list('Second_evaluation',flat=True)
    third_eval=Revaluation_copy.objects.values_list('Third_evaluation',flat=True)
    I_marks=Revaluation_copy.objects.values_list('Internal_marks',flat=True)
    E_marks=Revaluation_copy.objects.values_list('External_marks',flat=True)
    
    regulation=Regulations_with_Grades.objects.values_list('Regulation',flat=True)
    #print(sec_eval)
    for i in range(len(sec_eval)):
        j=0
        #print(id)
        r = Revaluation_copy.objects.get(id=id[i])
        min_marks = 0
        subject=Subject_max_marks.objects.filter(Subjects=r.Subject,Subject_codes=r.Subject_code).first()
        if subject:
            min_marks=subject.min_marks
        
        total=I_marks[i]+E_marks[i]
        if E_marks[i] > sec_eval[i]:
            None
        
        elif(sec_eval[i]>min_marks):
            r.External_marks=sec_eval[i]
        elif(sec_eval[i]>third_eval[i]):
            r.External_marks=sec_eval[i]      #no direct assignment 
        elif(E_marks[i]>third_eval[i]):
            None
        
        else:
            r=Revaluation_copy.objects.filter(id=id[i]).first()
            re=Regulations_with_Grades.objects.filter(Regulation=Reg,Lower_limit__lte=sec_eval[i],Upper_limit__gte=sec_eval[i]).first()
            grade=re.Grades if re else None
            r.Grades=grade
        
            
        # print(total)
            '''c=total - sec_eval[i]
            d=sec_eval[i]-third_eval[i]
            if c>=15:
                return render(request,'index.html',{"Revaluation":result})'''
            
            
            if grades[i]=='F':
            #print(grades)
                r.Credits=0
                print(r.Credits)
            if E_marks[i]==sec_eval[i]:
                r.Revaluation_Status="No Change"
            else:
                r.Revaluation_Status="Change"
        
        
    #print(results)
            r.save()
            j=j+1
    return render(request,'final.html',{"Revaluation_copy":results})

def Third_eval(request):
    count = 0
    ids=[]
    j=0
    revaluation=Revaluation_copy.objects.all()
    id=Revaluation_copy.objects.values_list('id',flat=True)
    grades=Revaluation_copy.objects.values_list('Grades',flat=True)
    sec_eval=Revaluation_copy.objects.values_list('Second_evaluation',flat=True)
    third_eval=Revaluation_copy.objects.values_list('Third_evaluation',flat=True)
    I_marks=Revaluation_copy.objects.values_list('Internal_marks',flat=True)
    E_marks=Revaluation_copy.objects.values_list('External_marks',flat=True)
    for i in range(len(id)):
        total=I_marks[i]+E_marks[i]
        #print("marks: ",sec_eval[i]-E_marks[i])
        if ((sec_eval[i]-E_marks[i])>=15):
            count+=1
            ids.append(id[i])
    
    #print("ids: ",ids)
    #print("count is: ",count)
    if(count>0):
        
        return render(request,'index.html',{"Revaluation_copy":revaluation,"ids":ids})
    
    else:
        return HttpResponseRedirect(reverse('rev:result'))
