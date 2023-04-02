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
        return render(request,'index.html',{"Revaluation":revaluation})
