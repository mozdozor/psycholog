import datetime
import json
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate,update_session_auth_hash,logout
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from Admin.forms import CommentModelForm, CourseModelForm, PageModelForm, adminSettingsProfileModelForm, categoryModelForm, courseSessionModelForm, courseSessionVideoModelForm, logoModelForm, whatWillYouLearnModelForm
from psikolog.forms import sliderModelForm
from psikolog.models import CommentModel, CustomUserModel, billingCourseModel, sliderModel
from .models import CategoryModel, CourseModel, IletisimModel, LogoModel, PageModel, bottomMenuModel, courseSessionModel, courseSessionVideoModel, notificationModel, topMenuModel, whatWillYouLearnModel





@permission_required('is_staff',login_url="loginAdmin")
def indexAdmin(request):
    newMessages=IletisimModel.objects.all().count()


    tod = datetime.datetime.now()
    d = datetime.timedelta(days = (30))
    a = tod - d
    totalMoneyThisMonth=0
    totalMoneyAllTime=0
    billsLastMonth=billingCourseModel.objects.filter(created_date__date__gte=a.date()).all()
    billAll=billingCourseModel.objects.all()
    for i in billsLastMonth:
        totalMoneyThisMonth+=i.price
    for i in billAll:
        totalMoneyAllTime+=i.price
    incomingThisMonth=totalMoneyThisMonth*0.8
    outgoingThisMonth=totalMoneyThisMonth*0.2
    incomingAll=totalMoneyAllTime*0.8
    outgoingAll=totalMoneyAllTime*0.2

    liste=[]
    liste.append(("%0.2f" % (incomingAll,)))
    liste.append(("%0.2f" % (outgoingAll,)))
    liste.append(("%0.2f" % (incomingThisMonth,)))
    liste.append(("%0.2f" % (outgoingThisMonth,)))
    mylistraw = list()
    for i in range(12):
        tod = datetime.datetime.now()
        d = datetime.timedelta(days = (12-i))
        a = tod - d
        counts=billingCourseModel.objects.filter(created_date__date=a.date()).count()
        mylistraw.append(counts)
    tod = datetime.datetime.now()
    counts=billingCourseModel.objects.filter(created_date__date=tod.date()).count()
    mylistraw.append(counts)
  #  mylistraw=[0,0,0,0,2,0,0,1,0,0,1,0,0]

 #   mylist = json.dumps(mylistraw)  
    context={
        "messageCount":newMessages,
        "commentCount":CommentModel.objects.all().count(),
        "courseCount":CourseModel.objects.all().count(),
        "billingCount":billingCourseModel.objects.all().count,
        'mylistjson': mylistraw,
        "totalMoneyThisMonth":totalMoneyThisMonth,
        "totalMoneyAllTime":totalMoneyAllTime,
        "list":liste
    }
    return render(request,"AdminTemplates/indexAdmin.html",context)




def loginAdmin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)		
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect("indexAdmin")
            else:
                messages.error(request,"Kullanıcı adı ya da parolanız hatalıdır.")
        else:
            messages.error(request,"Kullanıcı adı ya da parolanız hatalıdır.")
    form = AuthenticationForm()
    return render(request=request, template_name="AdminTemplates/loginAdmin.html", context={"form":form})




def logoutAdmin(request):
    logout(request)
    return redirect("loginAdmin")



@permission_required('is_staff',login_url="loginAdmin")
def showAllMessages(request):
    for i in IletisimModel.objects.all():
        i.okundu_bilgisi="okundu"
        i.save()
    new_messages=IletisimModel.objects.all()
    context={
        "new_messages":new_messages,
    }
    return render(request,"AdminTemplates/messagesAdmin.html",context)



@permission_required('is_staff',login_url="loginAdmin")
def listMenu(request):
    topMenuler=topMenuModel.objects.all()
    bottomMenuler=bottomMenuModel.objects.all()
    context={
        "topMenuler":topMenuler,
        "bottomMenuler":bottomMenuler,
    }
    return render(request,"AdminTemplates/listMenuAdmin.html",context)




@permission_required('is_staff',login_url="loginAdmin")
def addMenu(request):
    bottomMenus=""
    MenuObje=""
    type=request.GET.get("tip",None)
    menuId=request.GET.get("menuId",None)
    if type=="alt-menu-ekle":
        bottomMenus=topMenuModel.objects.all()
        if menuId:
            MenuObje=bottomMenuModel.objects.get(pk=menuId)
    if type=="ust-menu-ekle":
        if menuId:
            MenuObje=topMenuModel.objects.get(pk=menuId)
    
    context={
        "type":type,
        "bottomMenus":bottomMenus,
        "MenuObje":MenuObje,
    }
    if request.method == "POST":
        if type=="ust-menu-ekle":
            name=request.POST.get("menuName",None)
            url=request.POST.get("menuUrl",None)
            userType=request.POST.get("userType",None)
            menuSira=request.POST.get("menuSira",None)
            if menuId:
                MenuObje.name=name
                MenuObje.url=url
                MenuObje.menuSira=menuSira
                MenuObje.userType=userType
                MenuObje.save()
                messages.success(request,"Üst menü modeli başarıyla güncellendi")
            else:
                topMenuModel.objects.create(name=name,url=url,userType=userType,menuSira=menuSira)
                messages.success(request,"Üst menü modeli başarıyla oluşturuldu")
            return redirect("listMenu")
        elif type=="alt-menu-ekle":
            pk=request.POST.get("baglıMenu",None)
            if pk:
                topMenu=topMenuModel.objects.get(pk=pk)
                name=request.POST.get("menuName",None)
                url=request.POST.get("menuUrl",None)
                userType=request.POST.get("userType",None)
                menuSira=request.POST.get("menuSira",None)
                if menuId:
                    MenuObje.topMenu=topMenu
                    MenuObje.name=name
                    MenuObje.url=url
                    MenuObje.menuSira=menuSira
                    MenuObje.userType=userType
                    MenuObje.save()
                    messages.success(request,"Alt menü modeli başarıyla güncellendi")
                else:
                    bottomMenuModel.objects.create(topMenu=topMenu,name=name,url=url,userType=userType,menuSira=menuSira)
                    messages.success(request,"Alt menü modeli başarıyla oluşturuldu")
                return redirect("listMenu")
            else:
                messages.error(request,"Lütfen önce bir üst menü seçimi yapınız eğer yoksa önce üst menü modeli oluşturunuz.")
                return redirect("listMenu")
    return render(request,"AdminTemplates/addMenuAdmin.html",context)



@permission_required('is_staff',login_url="loginAdmin")
def deleteMenu(request,pk,str):
    if str=="ust-menu":
        obj=get_object_or_404(topMenuModel,pk=pk)
        obj.delete()
        messages.success(request,"Üst Menü başarıyla silindi")
    elif str=="alt-menu":
        obj=get_object_or_404(bottomMenuModel,pk=pk)
        obj.delete()
        messages.success(request,"Alt Menü başarıyla silindi")
    return redirect(request.META['HTTP_REFERER']) 





@permission_required('is_staff',login_url="loginAdmin")
def categoryListAdmin(request):
    categories=CategoryModel.objects.all().order_by("created_date")
    context={
        "categories":categories,
    }
    return render(request,"AdminTemplates/listCategoryAdmin.html",context)



@permission_required('is_staff',login_url="loginAdmin")
def addCategoryAdmin(request):
    category=""
    categoryId=request.GET.get("categoryId",None)
    if request.method == "POST":   
        if categoryId:
            category=get_object_or_404(CategoryModel,pk=categoryId)
            form = categoryModelForm(request.POST, request.FILES or None,instance=category)	
        else:
            form = categoryModelForm(request.POST, request.FILES or None)	
        if form.is_valid(): 
            form.save()            
            messages.success(request,"Kategori başarıyla kaydedildi.")
            return redirect("categoryListAdmin")
        else:
            messages.error(request,"İşleminiz gerçekleştirilemdi.Lütfen formu doğru doldurduğunuzdan emin olunuz.")
            return redirect("categoryListAdmin")
    if categoryId:
        category=get_object_or_404(CategoryModel,pk=categoryId)
        form = categoryModelForm(instance=category)
    else:
        form = categoryModelForm()
    context={
        "form":form,
        "category":category
        
    }
    
    return render(request,"AdminTemplates/addCategoryAdmin.html",context)



@permission_required('is_staff',login_url="loginAdmin")
def deleteCategoryAdmin(request,pk):
    obj=get_object_or_404(CategoryModel,pk=pk)
    obj.delete()
    messages.success(request,"Kategori başarıyla silindi")
    return redirect(request.META['HTTP_REFERER']) 





@permission_required('is_staff',login_url="loginAdmin")
def courseListAdmin(request):
    courses=CourseModel.objects.all()
    context={
        "courses":courses,
    }
    return render(request,"AdminTemplates/listCoursesAdmin.html",context)




@permission_required('is_staff',login_url="loginAdmin")
def courseAddAdmin(request):
    course=""
    courseId=request.GET.get("courseId",None)
    if request.method == "POST":   
        if courseId:
            course=get_object_or_404(CourseModel,pk=courseId)
            form = CourseModelForm(request.POST, request.FILES or None,instance=course)	
        else:
            form = CourseModelForm(request.POST, request.FILES or None)	
        if form.is_valid(): 
            form.save()            
            messages.success(request,"Kurs başarıyla kaydedildi.")
            return redirect("courseListAdmin")
        else:
            messages.error(request,"İşleminiz gerçekleştirilemdi.Lütfen formu doğru doldurduğunuzdan emin olunuz.")
            return redirect("courseListAdmin")
    if courseId:
        course=get_object_or_404(CourseModel,pk=courseId)
        form = CourseModelForm(instance=course)
    else:
        form = CourseModelForm()
    context={
        "form":form,
        "course":course
        
    }
    return render(request,"AdminTemplates/addCourseAdmin.html",context)




@permission_required('is_staff',login_url="loginAdmin")
def courseDetailAdmin(request,pk):
    course=get_object_or_404(CourseModel,pk=pk)
    context={
        "course":course,
    }
    return render(request,"AdminTemplates/courseDetailAdmin.html",context)




@permission_required('is_staff',login_url="loginAdmin")
def deleteCourseAdmin(request,pk):
    obj=get_object_or_404(CourseModel,pk=pk)
    obj.delete()
    messages.success(request,"Kurs başarıyla silindi")
    return redirect("courseListAdmin") 







@permission_required('is_staff',login_url="loginAdmin")
def wwylListAdmin(request,slug):
    course=get_object_or_404(CourseModel,slug=slug)
    wwyl=whatWillYouLearnModel.objects.filter(course=course)
 
    context={
        "wwyl":wwyl,
        "course":course,
        
    }
    return render(request,"AdminTemplates/listWwylAdmin.html",context)




@permission_required('is_staff',login_url="loginAdmin")
def wwylAddAdmin(request):
    wwyl=""
    courseId=request.GET.get("courseId",None)
    ogrenId=request.GET.get("ogrenId",None)
    if request.method == "POST":   
        if ogrenId:
            wwyl=get_object_or_404(whatWillYouLearnModel,pk=ogrenId)
            form = whatWillYouLearnModelForm(request.POST or None,instance=wwyl)	
        else:
            form = whatWillYouLearnModelForm(request.POST or None)	
        if form.is_valid(): 
            course=get_object_or_404(CourseModel,pk=courseId)
            com=form.save(commit=False)            
            com.course=course
            com.save()
            messages.success(request,"Öğrencekleriniz modeli başarıyla kaydedildi.")
            domainName="http"+request.META['HTTP_HOST']+"?courseId="+courseId
            return redirect("wwylListAdmin",course.slug)
        else:
            messages.error(request,"İşleminiz gerçekleştirilemdi.Lütfen formu doğru doldurduğunuzdan emin olunuz.")
            domainName=request.META['HTTP_HOST']+"?courseId="+courseId
            return redirect("wwylListAdmin",course.slug)
    if ogrenId:
        wwyl=get_object_or_404(whatWillYouLearnModel,pk=ogrenId)
        form = whatWillYouLearnModelForm(instance=wwyl)
    else:
        form = whatWillYouLearnModelForm()
    context={
        "form":form,
        "wwyl":wwyl,
        "courseId":courseId
        
    }
    return render(request,"AdminTemplates/addWwylAdmin.html",context)




@permission_required('is_staff',login_url="loginAdmin")
def deleteWwylAdmin(request,pk):
    obj=get_object_or_404(whatWillYouLearnModel,pk=pk)
    url=obj.course.pk
    obj.delete()
    messages.success(request,"Öğrenecekleriniz modeli başarıyla silindi")
    response = redirect('wwylListAdmin')
    response['Location'] += '?courseId='+str(url)
    return response






@permission_required('is_staff',login_url="loginAdmin")
def sessionListAdmin(request,pk):
    course=get_object_or_404(CourseModel,pk=pk)
    sessions=courseSessionModel.objects.filter(course=course).order_by("created_date")
    context={
        "sessions":sessions,
        "courseId":pk
    }
    return render(request,"AdminTemplates/listSessionAdmin.html",context)






@permission_required('is_staff',login_url="loginAdmin")
def sessionAddAdmin(request,pk):
    session=""
    course=get_object_or_404(CourseModel,pk=pk)
    currentId=request.GET.get("currentId",None)
    if request.method == "POST":   
        if currentId:
            session=get_object_or_404(courseSessionModel,pk=currentId)
            form = courseSessionModelForm(request.POST or None,instance=session)	
        else:
            form = courseSessionModelForm(request.POST or None)	
        if form.is_valid(): 
            com=form.save(commit=False)            
            com.course=course
            com.save()
            messages.success(request,"Bölüm modeli başarıyla kaydedildi.")
            return redirect("sessionListAdmin",pk)
        else:
            messages.error(request,"İşleminiz gerçekleştirilemdi.Lütfen formu doğru doldurduğunuzdan emin olunuz.")
            return redirect("sessionListAdmin",pk)
    if currentId:
        session=get_object_or_404(courseSessionModel,pk=currentId)
        form = courseSessionModelForm(instance=session)
    else:
        form = courseSessionModelForm()
    context={
        "form":form,
        "course":course,
        "currentId":currentId
        
    }
    return render(request,"AdminTemplates/addSessionAdmin.html",context)





@permission_required('is_staff',login_url="loginAdmin")
def deleteSessionAdmin(request,pk):
    obj=get_object_or_404(courseSessionModel,pk=pk)
    obj.delete()
    messages.success(request,"Bölüm başarıyla silindi")
    return redirect(request.META['HTTP_REFERER']) 






@permission_required('is_staff',login_url="loginAdmin")
def sessionVideoListAdmin(request,pk):
    session=get_object_or_404(courseSessionModel,pk=pk)
    context={
        "session":session,
        "sessionId":pk
    }
    return render(request,"AdminTemplates/listSessionVideosAdmin.html",context)






@permission_required('is_staff',login_url="loginAdmin")
def sessionVideoAddAdmin(request,pk):
  #  session=""
    session=get_object_or_404(courseSessionModel,pk=pk)
    currentId=request.GET.get("currentId",None)
    if request.method == "POST":   
        if currentId:
            video=get_object_or_404(courseSessionVideoModel,pk=currentId)
            form = courseSessionVideoModelForm(request.POST or None,instance=video)	
        else:
            form = courseSessionVideoModelForm(request.POST or None)	
        if form.is_valid(): 
            com=form.save(commit=False)            
            com.courseSession=session
            com.save()
            messages.success(request,"Video başarıyla kaydedildi.")
            return redirect("sessionVideoListAdmin",pk)
        else:
            messages.error(request,"İşleminiz gerçekleştirilemdi.Lütfen formu doğru doldurduğunuzdan emin olunuz.")
            return redirect("sessionVideoListAdmin",pk)
    if currentId:
        video=get_object_or_404(courseSessionVideoModel,pk=currentId)
        form = courseSessionVideoModelForm(instance=video)
    else:
        form = courseSessionVideoModelForm()
    context={
        "form":form,
        "session":session,
        "currentId":currentId
        
    }
    return render(request,"AdminTemplates/addVideoAdmin.html",context)






@permission_required('is_staff',login_url="loginAdmin")
def deleteSessionVideoAdmin(request,pk):
    obj=get_object_or_404(courseSessionVideoModel,pk=pk)
    obj.delete()
    messages.success(request,"Video başarıyla silindi")
    return redirect(request.META['HTTP_REFERER']) 






@permission_required('is_staff',login_url="loginAdmin")
def profileSettingsAdmin(request):
    if request.method == "POST":
        form = adminSettingsProfileModelForm(request.POST or None,request.FILES or None,instance=request.user)  	
        if form.is_valid():
            form.save()          
            messages.success(request,'Bilgileriniz başarıyla güncellendi!')
            return redirect("profileSettingsAdmin")
        else:
            for i in form.errors:
                if i == "email":
                    messages.error(request,"Bu maile sahip başka bir kullanıcı bulunmakta.")
                elif i == "username":
                    messages.error(request,"Bu kullanıcı adına sahip başka bir kullanıcı bulunmakta.")
                else:
                    messages.error(request,form.errors.get(i).as_text())
            return redirect("profileSettingsAdmin")
    form=adminSettingsProfileModelForm(instance=request.user)
    context={
        "form":form,
    }
    return render(request,"AdminTemplates/adminProfileSettings.html",context)



def getList(dict):
    list = []
    for key in dict.keys():
        list.append(str(key))
    return list


@permission_required('is_staff',login_url="loginAdmin")
def changePasswordAdmin(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user=form.save()           
            update_session_auth_hash(request, user)  # Important!
            messages.success(request,'Şifreniz başarıyla güncellendi!')
            return redirect("changePasswordAdmin")
        else:
           # messages.error(request,"Hata! Lütfen gereken yerleri aşağıda yazıldığı gibi doldurunuz")
            for mes in getList(form.error_messages):
                if mes=="password_mismatch":
                    messages.error(request,"İki parola alanı eşleşmedi.")
                elif mes=="password_incorrect":
                    messages.error(request,"Eski şifrenizi yanlış girdiniz")
            return redirect("changePasswordAdmin")

    form=PasswordChangeForm(request.user)
    context={
        "form":form,
        "error_messages":getList(PasswordChangeForm.error_messages),
    }
    return render(request,"AdminTemplates/passwordChangeAdmin.html",context)





@permission_required('is_staff',login_url="loginAdmin")
def commentsAdmin(request):
    comments=CommentModel.objects.filter(is_published=True,parent=None).all()
    context={
        "comments":comments,
        "replyComment":"asd",
        "type":"comments",
        "form":CommentModelForm()
    }
    return render(request,"AdminTemplates/commentsAdmin.html",context)




@permission_required('is_staff',login_url="loginAdmin")
def commentsRequestAdmin(request):
    comments=CommentModel.objects.filter(is_published=False).all()
    context={
        "comments":comments,
        "type":"comingRequest",
    }
    return render(request,"AdminTemplates/commentsAdmin.html",context)



@permission_required('is_staff',login_url="loginAdmin")
def acceptCommentsRequestAdmin(request,pk):
    comment=get_object_or_404(CommentModel,pk=pk)
    comment.is_published=True
    comment.save()
    messages.success(request,"Yorum başarıyla siteye eklendi.")
    return redirect("commentsRequestAdmin")








@permission_required('is_staff',login_url="loginAdmin")
def deleteComingRequestAdmin(request,pk):
    obj=get_object_or_404(CommentModel,pk=pk)
    obj.delete()
    messages.success(request,"Yorum başarıyla silindi")
    return redirect(request.META['HTTP_REFERER']) 




@permission_required('is_staff',login_url="loginAdmin")
def showPagesAdmin(request):
    pages=PageModel.objects.all()
    return render(request,"AdminTemplates/pagesAdmin.html",{"pages":pages,})




@permission_required('is_staff',login_url="loginAdmin")
def createPageModelAdmin(request):
    page=""
    pageId=request.GET.get("pageId",None)
    if request.method == "POST":   
        if pageId:
            page=get_object_or_404(PageModel,pk=pageId)
            form = PageModelForm(request.POST or None,instance=page)	
        else:
            form = PageModelForm(request.POST or None)	
        if form.is_valid(): 
            form.save()            
            messages.success(request,"Sayfa modeli başarıyla kaydedildi.")
            return redirect("showPagesAdmin")
        else:
            messages.error(request,"İşleminiz gerçekleştirilemdi.Lütfen formu doğru doldurduğunuzdan emin olunuz.")
            return redirect("showPagesAdmin")
    if pageId:
        page=get_object_or_404(PageModel,pk=pageId)
        form = PageModelForm(instance=page)
    else:
        form = PageModelForm()
    context={
        "form":form,
        "page":page
    }
    return render(request,"AdminTemplates/addPageAdmin.html",context)





@permission_required('is_staff',login_url="loginAdmin")
def deletePageModelAdmin(request,pk):
    obj=get_object_or_404(PageModel,pk=pk)
    obj.delete()
    messages.success(request,"Sayfa Seo Modeli başarıyla silindi")
    return redirect(request.META['HTTP_REFERER']) 




@permission_required('is_staff',login_url="loginAdmin")
def userListAdmin(request):
    users=CustomUserModel.objects.all()
    return render(request,"AdminTemplates/listUsersAdmin.html",{"users":users,})



@permission_required('is_staff',login_url="loginAdmin")
def addReplyCommentAdmin(request,slug,pk):
    course=get_object_or_404(CourseModel,slug=slug)
    parent=get_object_or_404(CommentModel,pk=pk)
    if request.method == "POST":
        form=CommentModelForm(data=request.POST)
        if form.is_valid():
            data=form.save(commit=False)
            data.comment_user=request.user
            data.course=course
            data.parent=parent
            data.star=0
            data.none_star=5
            data.is_published=True
            data.save()
            messages.success(request,"Yorumunuz başarılı bir şekilde eklenmiştir.",extra_tags="addingcomment")
            return redirect("commentsAdmin")
        else:
            messages.error(request,"Bir hata oluştu.Lütfen tekrar deneyiniz.",extra_tags="addingcomment")
            return redirect("commentsAdmin")




@permission_required('is_staff',login_url="loginAdmin")
def listNotificationsAdmin(request):
    notifications=notificationModel.objects.all()
    for i in notifications:
        i.has_readen="yes"
        i.save()
    return render(request,"AdminTemplates/listNotifications.html",{"notifications":notifications,})



@permission_required('is_staff',login_url="loginAdmin")
def deleteNotificationsAdmin(request,pk):
    obj=get_object_or_404(notificationModel,pk=pk)
    obj.delete()
    messages.success(request,"Bildirim başarıyla silindi")
    return redirect(request.META['HTTP_REFERER']) 



@permission_required('is_staff',login_url="loginAdmin")
def listBillingsAdmin(request):
    billings=billingCourseModel.objects.all()
    context={
        "billings":billings,

    }
    return render(request,"AdminTemplates/listBillingAdmin.html",context)





@permission_required('is_staff',login_url="loginAdmin")
def listSlidersAdmin(request):
    sliders=sliderModel.objects.order_by("sira")
    context={
        "sliders":sliders,
    }
    return render(request,"AdminTemplates/listSlidersAdmin.html",context)





@permission_required('is_staff',login_url="loginAdmin")
def createSliderModelAdmin(request):
    slider=""
    sliderId=request.GET.get("sliderId",None)
    if request.method == "POST":   
        if sliderId:
            slider=get_object_or_404(sliderModel,pk=sliderId)
            form = sliderModelForm(request.POST or None,request.FILES or None,instance=slider)	
        else:
            form = sliderModelForm(request.POST or None,request.FILES or None)	
        if form.is_valid(): 
            form.save()            
            messages.success(request,"Slider başarıyla kaydedildi.")
            return redirect("listSlidersAdmin")
        else:
            messages.error(request,"İşleminiz gerçekleştirilemdi.Lütfen formu doğru doldurduğunuzdan emin olunuz.")
            return redirect("listSlidersAdmin")
    if sliderId:
        slider=get_object_or_404(sliderModel,pk=sliderId)
        form = sliderModelForm(instance=slider)
    else:
        form = sliderModelForm()
    context={
        "form":form,
        "slider":slider
    }
    return render(request,"AdminTemplates/addSliderAdmin.html",context)





@permission_required('is_staff',login_url="loginAdmin")
def deleteSliderAdmin(request,pk):
    obj=get_object_or_404(sliderModel,pk=pk)
    obj.delete()
    messages.success(request,"Slider başarıyla silindi")
    return redirect(request.META['HTTP_REFERER']) 






@permission_required('is_staff',login_url="loginAdmin")
def listLogoAdmin(request):
    logo=LogoModel.objects.all()
    if logo:
        print("logo var")
       
    else:
        logo=LogoModel.objects.create(name="Udema")
        print("logo yok")
    context={
        "logo":logo,
    }
    return render(request,"AdminTemplates/listLogoAdmin.html",context)





@permission_required('is_staff',login_url="loginAdmin")
def updateLogoAdmin(request):
    logo=LogoModel.objects.all().first()
    if request.method == "POST":   
        form = logoModelForm(request.POST or None,request.FILES or None,instance=logo)	
        if form.is_valid(): 
            form.save()
            messages.success(request,"Logo başarıyla kaydedildi.")
            return redirect("listLogoAdmin")
        else:
            messages.error(request,"İşleminiz gerçekleştirilemdi.Lütfen formu doğru doldurduğunuzdan emin olunuz.")
            return redirect("listLogoAdmin")
    form = logoModelForm(instance=logo)
    context={
        "form":form,
        
    }
    return render(request,"AdminTemplates/addLogoAdmin.html",context)
