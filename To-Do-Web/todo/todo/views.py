from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from todo import models
from todo.models import TODOO

def signup(request):
    if request.method == 'POST':
     fnm=request.POST.get('fnm')
     emailid=request.POST.get('email')
     pwd=request.POST.get('pwd')
     print(fnm,emailid,pwd)
     my_user=User.objects.create_user(fnm,emailid,pwd)
     my_user.save()
     return redirect('/login')
     
    return render(request,'sign.html')