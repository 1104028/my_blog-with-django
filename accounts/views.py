from django.shortcuts import render

# Create your views here.
from accounts.forms import UserForm


def registerUser(request):
    if request.method =="POST":
        userform= UserForm(request.POST)

        if userform.is_valid():
            newuser=userform.save(commit=False)
            newuser.set_password(userform.cleaned_data['password'])
            newuser.save()
            return render(request,'registration_completed.html',{'user':newuser})

    else:
        userform=UserForm()


    return render(request,'registration.html',{'userform':userform})