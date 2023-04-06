from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from django.urls import reverse
# Create your views here.
def data(request):
    revaluation=Revaluation.objects.all()
    
    if request.method == 'GET':

        return render(request,'index.html',{"Revaluation":revaluation})
    elif request.method == 'POST':
        id=request.POST.getlist('id[]')
        sec_eval=request.POST.getlist('s_eval[]')
        third_eval=request.POST.getlist('t_eval[]')
        #print(id,sec_eval,third_eval)
        for i in range(len(sec_eval)):
            r=Revaluation.objects.filter(id=id[i]).first()
            r.Second_evaluation=sec_eval[i]
            r.Third_evaluation=third_eval[i]
            r.save()
        return HttpResponseRedirect(reverse('rev:result'))

def result(request):
    results=Revaluation.objects.all()
    #reg_20=Regulations_20.objects.all()
    id=Revaluation.objects.values_list('id',flat=True)
    grade=Revaluation.objects.values_list('Grades',flat=True)
    sec_eval=Revaluation.objects.values_list('Second_evaluation',flat=True)
    I_marks=Revaluation.objects.values_list('Internal_marks',flat=True)
    E_marks=Revaluation.objects.values_list('External_marks',flat=True)
    lower_bound=Regulations_20.objects.values_list('Lower_limit',flat=True)
    upper_bound=Regulations_20.objects.values_list('Upper_limit',flat=True)
    grades=Regulations_20.objects.values_list('Grades',flat=True)

    # print(sec_eval)
    # print(I_marks)
    # print(E_marks)
    # print(lower_bound)
    # print(upper_bound)
    # print(grades)
    for i in range(len(id)):
        j=0
        r=Revaluation.objects.filter(id=id[i]).first()
        re=Regulations_20.objects.all()
        total=I_marks[i]+E_marks[i]
        # print(total)
        c=total - sec_eval[i]
        if sec_eval[i]>=upper_bound[j]: # >= 90
            r.Grades=grades[j]
            
        elif lower_bound[j+1]<=sec_eval[i]<upper_bound[j+1]: # 80 <= x <89
            r.Grades=grades[j+1]
        elif lower_bound[j+2]<=sec_eval[i]<upper_bound[j+2]: # 70 <= x <79
            r.Grades=grades[j+2]
        elif lower_bound[j+3]<=sec_eval[i]<upper_bound[j+3]: # 60 <= x <69
            r.Grades=grades[j+3]
        elif lower_bound[j+4]<=sec_eval[i]<upper_bound[j+4]: # 50 <= x <59
            r.Grades=grades[j+4]
        elif lower_bound[j+5]<=sec_eval[i]<upper_bound[j+5]: # 40 <= x <49
            r.Grades=grades[j+5]
        elif lower_bound[j+6]<=sec_eval[i]<upper_bound[j+6]: # 1 <= x <39
            r.Grades=grades[j+6]
        else:
            r.Grades=grades[j+7]
        if grade[i]=='F':
            print(grades)
            r.Credits=0
            print(r.Credits)
        if total==sec_eval[i]:
           r.Revaluation_Status="No Change"
        else:
           r.Revaluation_Status="Change"
        r.save()
    print(results)
    return render(request,'final.html',{"Revaluation":results})
