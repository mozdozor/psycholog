from email import message
import math
from unicodedata import category
from django.shortcuts import get_object_or_404, redirect, render
from Admin.forms import CommentModelForm, IletisimModelForm
from Admin.models import CategoryModel, CourseModel, aydinlatmaMetniModel, blogCategoryModel, blogModel, courseSessionModel, gizlilikMetniModel, kvkkMetniModel, notificationModel, whatWillYouLearnModel
from django.contrib.auth import logout
from psikolog.forms import CommentModelStarsForm, registerUserForm, userSettingsProfileModelForm
from psikolog.models import CommentModel, CustomUserModel, billingCourseModel, favouriteCourseModel, sliderModel
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate,update_session_auth_hash,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.mail import send_mail
from django.db.models import Avg
import urllib
import json


# Create your views here.



def index(request):
    sliders=sliderModel.objects.all().order_by("sira")
    courses=CourseModel.objects.all().order_by("created_date")
    categories=CategoryModel.objects.all().order_by("created_date")
    blogs=blogModel.objects.all().order_by("created_date")
    context={
        "sliders":sliders,
        "courses":courses,
        "categories":categories,
        "blogs":blogs,
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
    commentStatus=""
    form=CommentModelStarsForm()
    course=get_object_or_404(CourseModel,slug=slug)
    learns=whatWillYouLearnModel.objects.filter(course=course).order_by("created_date")
    sessions=courseSessionModel.objects.filter(course=course).order_by("created_date")
    comments=CommentModel.objects.filter(course=course,parent=None).order_by("created_date")
    has_bougth="false"
    if request.user.is_authenticated:
        billings=billingCourseModel.objects.filter(payment_user=request.user,course=course).all()
        if billings:
            has_bougth="true"
        for cs in comments:
            if cs.comment_user==request.user and cs.is_published==True:
                commentStatus="writtenBefore"
            elif cs.comment_user==request.user and cs.is_published==False:
                commentStatus="pendingComment"
    comments=comments.filter(is_published=True).order_by("created_date")
    context={
        "course":course,
        "learns":learns,
        "sessions":sessions,
        "comments":comments,
        "commentStatus":commentStatus,
        "has_bougth":has_bougth
    }
    if request.method == "POST":
        form=CommentModelStarsForm(data=request.POST)
        if form.is_valid():    
            data=form.save(commit=False)
            data.comment_user=request.user
            data.course=course
            data.none_star=0
            data.star=5
            message=request.user.first_name+" "+request.user.last_name+" adlı kullanıcıdan "+course.title+" isimli kursunuza yeni bir yorum gelmiştir."
            if request.user.is_superuser:
                data.is_published=True
            data.save()
            notificationModel.objects.create(title="Yorum isteğiniz",type="comment",noti_user=request.user,object=course,message=message)
            comments=CommentModel.objects.filter(course=course,parent=None,is_published=True)
            if data.parent is None:
                average_star=comments.aggregate(Avg('star'))
                if average_star["star__avg"] != None:
                    average_star=int(math.ceil(average_star["star__avg"]))
                else:
                    average_star=0
                course.average_star=average_star
                none_average_star=5-course.average_star 
                course.none_average_star=none_average_star
            course.save()
            if request.user.is_superuser:
                messages.success(request,"Yorumunuz başarılı bir şekilde eklenmiştir.",extra_tags="addingcomment")
            else:
                messages.success(request,"Yorumunuz onaylandıktan sonra sitemize eklenecektir.",extra_tags="addingcomment")
            return redirect("courseDetail",slug=slug)
            
        else:
            messages.error(request,"Bir hata ile karşılaştık.Sistem yöneticisi ile iletişime geçin",extra_tags="addingcomment")
            return redirect("courseDetail",slug=slug)
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
    if request.method == "POST":
        form = IletisimModelForm(request.POST)
        if form.is_valid(): 
            form.save()
           # print(form.cleaned_data["mesaj"])
            send_mail(
                form.cleaned_data["name"]+" "+ form.cleaned_data["lastName"]+" )",
                form.cleaned_data["mesaj"]+"\n\n\n ( "+form.cleaned_data["email"]+" )",
                form.cleaned_data["phone_number"],
                ["muhammetay651@gmail.com","muhammet19071340@gmail.com"],
            )
            messages.success(request,"Mesajınız başarıyla tarafımıza iletildi.En kısa sürede sizinle iletişime geçilecektir.Teşekkür ederiz.")
            return redirect("contact")
    form = IletisimModelForm()
    context={
        "form":form,
    }
    return render(request,"contacts.html",context)




def aydinlatmaMetni(request):
    metinler=aydinlatmaMetniModel.objects.all()
    metin=""
    if metinler:
        metin=metinler.first()
    context={
        "metin":metin,
        "metinType":"aydinlatma",
        "printMetin":"Aydınlatma Metni",
    }
    return render(request,"metinler.html",context)




def gizlilikPolitikası(request):
    metinler=gizlilikMetniModel.objects.all()
    metin=""
    if metinler:
        metin=metinler.first()
    context={
        "metin":metin,
        "metinType":"gizlilik",
        "printMetin":"Gizlilik Politikası",
    }
    return render(request,"metinler.html",context)




def kvkkMetni(request):
    metinler=kvkkMetniModel.objects.all()
    metin=""
    if metinler:
        metin=metinler.first()
    context={
        "metin":metin,
        "metinType":"kvkk",
        "printMetin":"KVKK Metni",
    }
    return render(request,"metinler.html",context)





def blogDetail(request,slug):
    blog=get_object_or_404(blogModel,slug=slug)
    hasAuthUserMadeComment=""
    categories=blogCategoryModel.objects.order_by("created_date").all()
    lastThreeBlogs=blogModel.objects.order_by("-created_date")[:3]
    comments=CommentModel.objects.filter(is_published=True,parent=None,blog=blog).order_by("created_date")
    if request.user.is_authenticated:
        filterComments=comments.filter(comment_user=request.user).all()
        if filterComments:
            hasAuthUserMadeComment="yes"

    form=CommentModelStarsForm()
    context={
        "blog":blog,
        "form":form,
        "comments":comments,
        "hasAuthUserMadeComment":hasAuthUserMadeComment,
        "lastThreeBlogs":lastThreeBlogs,
        "categories":categories
    }
    if request.method == "POST":
        form=CommentModelStarsForm(data=request.POST)
        if form.is_valid():    
            data=form.save(commit=False)
            data.comment_user=request.user
            data.blog=blog
            data.none_star=0
            data.star=5
            message=request.user.first_name+" "+request.user.last_name+" adlı kullanıcıdan "+blog.title+" isimli blogunuza yeni bir yorum gelmiştir."
            if request.user.is_superuser:
                data.is_published=True
            data.save()
            notificationModel.objects.create(title="Yorum isteğiniz",type="commentBlog",noti_user=request.user,blogObject=blog,message=message)
            if request.user.is_superuser:
                messages.success(request,"Yorumunuz başarılı bir şekilde eklenmiştir.",extra_tags="addingcomment")
            else:
                messages.success(request,"Yorumunuz onaylandıktan sonra sitemize eklenecektir.",extra_tags="addingcomment")
            return redirect("blogDetail",slug=slug)
            
        else:
            messages.error(request,"Bir hata ile karşılaştık.Sistem yöneticisi ile iletişime geçin",extra_tags="addingcomment")
            return redirect("blogDetail",slug=slug)
    return render(request,"blog-detail.html",context)






def allBlogs(request):
    blogs=blogModel.objects.all()
    queryCategory=request.GET.get("kategori",None)
    if queryCategory:
        newQ=list()
        for bl in blogs:
            for q in bl.categories.all():
                if q.name == queryCategory:
                    newQ.append(bl)
                    break
        blogs=newQ
    lastThreeBlogs=blogModel.objects.order_by("-created_date")[:3]
    categories=blogCategoryModel.objects.order_by("created_date").all()
    searchKey=""
    if request.method == "POST":
        searchKey=request.POST.get("keys",None)
        newQ=list()
        for bl in blogs:
            lower_map = {
                ord(u'I'): u'ı',
                ord(u'İ'): u'i',
            }
            searchKey=searchKey.translate(lower_map).lower()
            title=str(bl.title).translate(lower_map).lower()
            if searchKey in title:
                newQ.append(bl)
                break
        blogs=newQ
    context={
        "blogs":blogs,
        "lastThreeBlogs":lastThreeBlogs,
        "categories":categories,
        "searchKey":searchKey
        
    }
    return render(request,"blog-lists.html",context)


