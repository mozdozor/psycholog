from django.shortcuts import redirect, render
from Admin.models import CategoryModel, CourseModel
from django.contrib.auth import logout
from psikolog.forms import registerUserForm, userSettingsProfileModelForm
from psikolog.models import CustomUserModel, sliderModel
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate,update_session_auth_hash,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.mail import send_mail

# Create your views here.



def index(request):
    sliders=sliderModel.objects.all().order_by("sira")
    courses=CourseModel.objects.all()
    categories=CategoryModel.objects.all()
    context={
        "sliders":sliders,
        "courses":courses,
        "categories":categories,
    }
    return render(request,"index.html",context)






def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)		
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("index")
            else:
                messages.error(request,"Kullanıcı adı ya da parolanız hatalıdır.")
        else:
            messages.error(request,"Kullanıcı adı ya da parolanız hatalıdır.")
    form = AuthenticationForm()
    context={
       
    }
    return render(request,"login.html",context)


def logoutIndex(request):
    logout(request)
    return redirect("login")




def getList(dict):
    list = []
    for key in dict.keys():
        list.append(str(key))
    return list




def registerUser(request):
    if request.method == "POST":
        form = registerUserForm(request.POST or None)
        if form.is_valid():
            data=form.save(commit=False)
            data.username= form.cleaned_data.get("email")
            data.image="avatar/no-avatar.png"
            data.save()
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=email,password=password)
            auth_login(request,user)
            return redirect("index")
        else:
            messages.error(request,form.errors,extra_tags="registerError")
            return render(request, "register.html",{"form":form,})
    else:
        form = registerUserForm()
    context = {
        "form":form,
    }
    return render(request, "register.html",context)







@login_required(login_url="login")
def changePassword(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user=form.save()           
            update_session_auth_hash(request, user)  # Important!
            messages.success(request,'Şifreniz başarıyla güncellendi!')
            return redirect("changePassword")
        else:
            messages.error(request,"Hata! Lütfen gereken yerleri aşağıda yazıldığı gibi doldurunuz")
            return redirect("changePassword")

    form=PasswordChangeForm(request.user)
    context={
        "form":form,
        "error_messages":PasswordChangeForm.error_messages,
    }
    return render(request,"changePassword.html",context)






@login_required(login_url="login")
def profileSettings(request):
    if request.method == "POST":
        form = userSettingsProfileModelForm(request.POST or None,request.FILES or None,instance=request.user)  	
        if form.is_valid():
            form.save()          
            messages.success(request,'Bilgileriniz başarıyla güncellendi!')
            return redirect("profileSettings")
        else:
            for i in form.errors:
                if i == "email":
                    messages.error(request,"Bu maile sahip başka bir kullanıcı bulunmakta.")
                else:
                    messages.error(request,form.errors.get(i).as_text())
            return redirect("profileSettings")
    form=userSettingsProfileModelForm(instance=request.user)
    context={
        "form":form,
    }
    return render(request,"profileSettings.html",context)