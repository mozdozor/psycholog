from unicodedata import category
from django.shortcuts import get_object_or_404, redirect, render
from Admin.forms import CommentModelForm
from Admin.models import CategoryModel, CourseModel, courseSessionModel, whatWillYouLearnModel
from django.contrib.auth import logout
from psikolog.forms import registerUserForm, userSettingsProfileModelForm
from psikolog.models import CustomUserModel, billingCourseModel, favouriteCourseModel, sliderModel
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




def coursesGridList(request):
    selectedCategories=[]
    selectedStars=[]
    courses=CourseModel.objects.all()
    categories=CategoryModel.objects.all()
    if request.method == "POST":
        if 'categoryName' in request.POST.keys():
            selectedCategories=request.POST.getlist("categoryName")
            if "all" in selectedCategories:
                pass
            else:
                catId=[]
                for i in selectedCategories:
                    id=CategoryModel.objects.get(name=i)
                    catId.append(id)
                courses=courses.filter(category__in=catId)
        if 'star' in request.POST.keys():
            selectedStars=request.POST.getlist("star")
            courses=courses.filter(average_star__in=selectedStars)
    else:
        categoryName=request.GET.get("kategori-adi",None)
        if categoryName:
            courses=courses.filter(category__name=categoryName)
        else:
            selectedCategories.append("all")
    context={
        "courses":courses,
        "categories":categories,
        "allCoursesCount":CourseModel.objects.all().count(),
        "selectedCategories":selectedCategories,
        "selectedStars":selectedStars
    }
    return render(request,"courses-grid-sidebar.html",context)




@login_required(login_url="login")
def favouritesCoursesGridList(request):
    courses=request.user.favouriteCourses.all()
    context={
        "courses":courses,
    }
    return render(request,"favourite-courses.html",context)




@login_required(login_url="login")
def AddFavouritesCoursesGridList(request,pk):
    course=get_object_or_404(CourseModel,pk=pk)
    is_exist=favouriteCourseModel.objects.filter(course=course,user=request.user)
    if is_exist:
        is_exist.all().delete()
        messages.error(request,"Kurs favorilerinizden kaldırılmıştır")
    else:
        favouriteCourseModel.objects.create(user=request.user,course=course)
        messages.success(request,"Kurs favorilerinize başarıyla eklenmiştir")
    return redirect("favouritesCoursesGridList")





def courseDetail(request,slug):
    form=CommentModelForm()
    course=get_object_or_404(CourseModel,slug=slug)
    learns=whatWillYouLearnModel.objects.filter(course=course).order_by("created_date")
    sessions=courseSessionModel.objects.filter(course=course).order_by("created_date")
    context={
        "course":course,
        "learns":learns,
        "sessions":sessions
    }
    # if request.method == "POST":
    #     form=CommentModelForm(data=request.POST)
    #     if form.is_valid():    
    #         data=form.save(commit=False)
    #         data.comment_user=request.user
    #         data.course=course
    #         data.none_star=5-data.star
    #         if len(data.comment)<130:
    #             lenData=130-len(data.comment)
    #             for i in range(lenData):
    #                 data.comment+=" "
    #         data.save()
    #         comments=CommentModel.objects.filter(doctor=doctor,parent=None,is_published=True)
    #         if data.parent is None:
    #             average_star=comments.aggregate(Avg('star'))
    #             if average_star["star__avg"] != None:
    #                 average_star=int(math.ceil(average_star["star__avg"]))
    #             else:
    #                 average_star=0
    #             doctor.average_star=average_star
    #             none_average_star=5-doctor.average_star 
    #             doctor.none_average_star=none_average_star
    #             doctor.parent_comments_count=comments.count()
    #         doctor.save()
    #         if doctor==request.user:
    #             messages.success(request,"Yorumunuz başarılı bir şekilde eklenmiştir.",extra_tags="addingcomment")
    #         else:
    #             messages.success(request,"Yorumunuz onaylandıktan sonra sitemize eklenecektir.",extra_tags="addingcomment")
    #         return redirect("showDoctorProfile",slug=slug)
            
    #     else:
    #         messages.error(request,"Yorumunuz onaylandıktansss sonra sitemize eklenecektir.",extra_tags="addingcomment")
    #         return redirect("showDoctorProfile",slug=slug)
    return render(request,"course-detail.html",context)






@login_required(login_url="login")
def learningContentList(request):
    courses=billingCourseModel.objects.filter(payment_user=request.user)
    context={
        "courses":courses,
    }
    return render(request,"learning-content.html",context)





def aboutUs(request):
    context={
    }
    return render(request,"about.html",context)




def contact(request):
    context={
    }
    return render(request,"contacts.html",context)
