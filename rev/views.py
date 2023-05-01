from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from django.urls import reverse
from django.db.models import Case, When
from .forms import UploadForm
import csv
import math
# Create your views here.
def home(request):
    status=0
    message = ''
    
    if request.method == 'POST':

        print(request.FILES['file'])
        form = UploadForm(request.POST, request.FILES)

        
        if form.is_valid():
            
            file = form.cleaned_data['file']
            file2 = form.cleaned_data['file2']

            Revaluation.objects.all().delete()
            Revaluation_copy.objects.all().delete()
            orginal_Result.objects.all().delete()

            csv_data = csv.reader(file2.read().decode('utf-8').splitlines())
            for columns in csv_data:
                orginal_Result.objects.create(Hallticket=columns[0],subject_code=columns[1],subject_type=columns[2],subject_name=columns[3],Internal=columns[4],External=columns[5],Total=columns[6],grade_letter = columns[9],credits=columns[7])

                
           
            csv_data = csv.reader(file.read().decode('utf-8').splitlines())
            for columns in csv_data:
                result=orginal_Result.objects.filter(Hallticket=columns[2]).first()
                revaluation = Revaluation(id=columns[0],Application_type=columns[1], Hallticket=columns[2],Student_Name=columns[3],Subject_code=columns[4],Subject=columns[5],Mobile=columns[6],Dhondi_id=columns[7],Amount=columns[8])
                revaluation_copy = Revaluation_copy(id=columns[0] ,Hallticket=columns[2],Subject_code=columns[4],Subject=columns[5],Internal_marks=result.Internal,External_marks=result.External,Grades=result.grade_letter,Credits=result.credits)
                
                revaluation.save()
                revaluation_copy.save()
            revaluation=Revaluation.objects.all()
            
            select_value=request.POST.get('Regulation')
            if select_value == None:
                
                message='Please Select the Regulation'
                context = {'message': message,'status':status}
                return render(request, 'home.html',context)
            
            revaluation=Revaluation_copy.objects.all()
            grades=Revaluation_copy.objects.values_list('Grades',flat=True)
            subjects=Revaluation_copy.objects.values_list('Subject_code',flat=True)
            subjects_info=Subject_max_marks.objects.filter(subject_code__in=subjects)
            original_results=orginal_Result.objects.all()
            print(grades)
            return render(request,'index.html',{"Revaluation_copy":revaluation,"Regulation":select_value,"subjects_info":subjects_info})


        else:
            print(form.errors)
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
        # internal_marks=request.POST.getlist('i_marks[]')
        # external_marks=request.POST.getlist('e_marks[]')
        # credits=request.POST.getlist('credits[]')
        # grades=request.POST.getlist('grades[]')
        sec_eval=request.POST.getlist('s_eval[]')
        sec_eval=[int(i) for i in sec_eval]
        third_eval=request.POST.getlist('t_eval[]')
        third_eval=[int(i) for i in third_eval]
        Regulation=request.POST.get('Regulation')
        #print(id,sec_eval,third_eval)
        for i in range(len(sec_eval)):
            r=Revaluation_copy.objects.filter(id=id[i]).first()
            subject_info = Subject_max_marks.objects.filter(subject_code=r.Subject_code).first()
            
            # diff >15 , now find nearest 2 evals and take average
            diff = abs(r.External_marks-sec_eval[i])
            final_eval_result=0
            if(diff>=15):
                diff_2_3 =abs(sec_eval[i]-third_eval[i])
                diff_1_3 =abs(r.External_marks-third_eval[i])
                if diff<diff_2_3 and diff<diff_1_3:
                    final_eval_result=math.ceil((r.External_marks+sec_eval[i])/2)
                elif(diff_1_3<diff_2_3):
                    final_eval_result=math.ceil((r.External_marks+third_eval[i])/2)
                else:
                    final_eval_result=math.ceil((sec_eval[i]+third_eval[i])/2)
            else:
                final_eval_result=sec_eval[i]

            
            # if fails in 2nd eval and diff < 15 then first eval will be final
            status="No Change"
            Grade=r.Grades
            Credits=0 if r.Grades=='F' else r.Credits
            if final_eval_result>=subject_info.pass_external_marks:
                # if passes in 2nd eval then final marks= 2nd eval + internal and check grade change
                if final_eval_result>r.External_marks:
                    total_marks=r.Internal_marks+final_eval_result
                    total_perc=math.ceil((total_marks/subject_info.max_total_marks)*100)
                    grade=Regulations_with_Grades.objects.filter(Lower_limit__lte=total_perc,Upper_limit__gte=total_perc,Regulation=Regulation).first().Grades
                    if grade!=r.Grades:
                        status="Change"
                        Grade=grade
                        Credits=subject_info.credits
                    else:
                        final_eval_result=r.External_marks
                else:
                    final_eval_result=r.External_marks
            else:
                final_eval_result=r.External_marks
            r.Second_evaluation=sec_eval[i]
            r.Third_evaluation=third_eval[i]
            r.Total_after_revaluation=final_eval_result+r.Internal_marks
            r.Credits=Credits
            r.Grades=Grade
            r.Revaluation_Status=status
            r.save()
        return render(request,"final.html",{"Revaluation_copy":Revaluation_copy.objects.all()})

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
        temp=0

        p=E_marks[i]
        q=sec_eval[i]
        t=third_eval[i]
        difpq=abs(p-q)
        difqt=abs(q-t)
        diftp=abs(t-p)
    
        if E_marks[i] > sec_eval[i]:
            None
        
        elif(sec_eval[i]>min_marks):
            r.External_marks=sec_eval[i]
        elif(sec_eval[i]>third_eval[i]):
            r.External_marks=sec_eval[i]      #no direct assignment 
        elif(E_marks[i]>third_eval[i]):
            if(difpq>difqt and difpq>diftp):
                temp=difpq
            elif(difqt>difpq and difqt>diftp):
                temp=difqt
            elif(diftp>difpq and diftp>difqt):
                temp=diftp

        else:
            #print("hello")
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
    subject=Subject_max_marks.objects.all()
    revaluation=Revaluation_copy.objects.all()
    id=Revaluation_copy.objects.values_list('id',flat=True)
    subject_code=Revaluation_copy.objects.values_list('Subject_code',flat=True)
    grades=Revaluation_copy.objects.values_list('Grades',flat=True)
    sec_eval=Revaluation_copy.objects.values_list('Second_evaluation',flat=True)
    third_eval=Revaluation_copy.objects.values_list('Third_evaluation',flat=True)
    I_marks=Revaluation_copy.objects.values_list('Internal_marks',flat=True)
    E_marks=Revaluation_copy.objects.values_list('External_marks',flat=True)
    for i in range(len(id)):
        e_marks=0
        i_marks=0
        message=''
        
        if subject:
            i_marks=subject.Max_internal
            e_marks=subject.Max_external
        #print("marks: ",sec_eval[i]-E_marks[i])
        '''if(I_marks[i]>=i_marks):
            ids.append(id[i])
            message='Invalid Internal Marks'
            context = {'message': message}
        if(E_marks[i]>=e_marks):
            ids.append(id[i])
            message='Invalid External Marks'
            context = {'message': message}'''
        if ((sec_eval[i]-E_marks[i])>=15):
            count+=1
            ids.append(id[i])
            message='Third Evaluation is required'
            context = {'message': message}
    
    if(count>0):
        
        return render(request,'index.html',{"Revaluation_copy":revaluation,"ids":ids,"context":context})
    
    else:
        return HttpResponseRedirect(reverse('rev:result'))
