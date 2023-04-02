from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
# Create your views here.
def data(request):
    revaluation=Revaluation.objects.all()
    
    if request.method == 'GET':

        return render(request,'index.html',{"Revaluation":revaluation})
    elif request.method == 'POST':
        id=request.POST.getlist('id[]')
        sec_eval=request.POST.getlist('s_eval[]')
        third_eval=request.POST.getlist('t_eval[]')
        print(id,sec_eval,third_eval)
        for i in range(len(sec_eval)):
            r=Revaluation.objects.filter(id=id[i]).first()
            print(r,id[i],sec_eval[i],third_eval[i])
            r.Second_evaluation=sec_eval[i]
            r.Third_evaluation=third_eval[i]
            r.save()
        return render(request,'final.html',{"Revaluation":revaluation})

def result(request):
    results=Revaluation.objects.all()
    id=Revaluation.objects.values_list('id',flat=True)
    
    sec_eval=Revaluation.objects.values_list('Second_evaluation',flat=True)
    I_marks=Revaluation.objects.values_list('Internal_marks',flat=True)
    E_marks=Revaluation.objects.values_list('External_marks',flat=True)
    for i in range(len(id)):
        r=Revaluation.objects.filter(id=id[i]).first()
        total=I_marks[i]+E_marks[i]
        #print(total)
        c=total - sec_eval[i]
        if sec_eval[i]>=90:
            r.Grades="A+"
        elif 80<=sec_eval[i]<89:
            r.Grades="A"
        elif 70<=sec_eval[i]<79:
            r.Grades="B"
        elif 60<=sec_eval[i]<69:
            r.Grades="C"
        elif 50<=sec_eval[i]<59:
            r.Grades="D"
        elif 40<=sec_eval[i]<49:
            r.Grades="E"
        else:
            r.Grades="F"
        if r.Grades=="F":
            r.Credits=0
        if total==sec_eval[i]:
           r.Revaluation_Status="No Change"
        else:
           r.Revaluation_Status="Change"
        r.save()
    return render(request,'final.html',{"Revaluation":results})
