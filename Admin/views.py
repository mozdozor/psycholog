import datetime
import json
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate,update_session_auth_hash,logout
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from Admin.forms import CommentModelForm, CourseModelForm, PageModelForm, adminSettingsProfileModelForm, appointmentAdminModelForm, aydinlatmaMetniModelForm, blogCategoryModelForm, blogModelForm, categoryModelForm, courseSessionModelForm, courseSessionVideoModelForm, gizlilikMetniModelForm, hakkimizdaModelForm, kvkkMetniModelForm, logoModelForm, mesafeliSatisModelForm, socialModelForm, whatWillYouLearnModelForm
from psikolog.forms import sliderModelForm
from psikolog.models import CommentModel, CustomUserModel, billingCourseModel, hasWatchedModel, orderModel, sliderModel
from .models import CategoryModel, CourseModel, IletisimModel, LogoModel, PageModel, appointmentAdminModel, appointmentModel, aydinlatmaMetniModel, blogCategoryModel, blogModel, bottomMenuModel, courseSessionModel, courseSessionVideoModel, footerMailModel, gizlilikMetniModel, hakkimizdaModel, kvkkMetniModel, mesafeliSatisModel, notificationModel, socialModel, topMenuModel, whatWillYouLearnModel
from django.core.mail import send_mail




@permission_required('is_staff',login_url="loginAdmin")
def indexAdmin(request):
    newMessages=IletisimModel.objects.all().count()


    tod = datetime.datetime.now()
    d = datetime.timedelta(days = (30))
    a = tod - d
    totalMoneyThisMonth=0
    totalMoneyAllTime=0
    billsLastMonth=orderModel.objects.filter(created_date__date__gte=a.date(),status="yes").all()
    billAll=orderModel.objects.filter(status="yes").all()
    for i in billsLastMonth:
        totalMoneyThisMonth+=i.price
    for i in billAll:
        totalMoneyAllTime+=i.price
    outgoingThisMonth=(totalMoneyThisMonth*235)/10000
    incomingThisMonth=totalMoneyThisMonth-outgoingThisMonth
    outgoingAll=(totalMoneyAllTime*235)/10000
    incomingAll=totalMoneyAllTime-outgoingAll
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
        counts=orderModel.objects.filter(created_date__date=a.date(),status="yes").count()
        mylistraw.append(counts)
    tod = datetime.datetime.now()
    counts=orderModel.objects.filter(created_date__date=tod.date(),status="yes").count()
    mylistraw.append(counts)
  #  mylistraw=[0,0,0,0,2,0,0,1,0,0,1,0,0]

 #   mylist = json.dumps(mylistraw)  
    context={
        "messageCount":newMessages,
        "commentCount":CommentModel.objects.all().count(),
        "courseCount":CourseModel.objects.all().count(),
        "billingCount":orderModel.objects.filter(status="yes").count,
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
                return redirect("indexAdmin")
        else:
            messages.error(request,"Kullanıcı adı ya da parolanız hatalıdır.")
            return redirect("indexAdmin")
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
    new_messages=IletisimModel.objects.all().order_by("-olusturulma_tarihi")
    messages=list()
    if request.method == "POST":
        if "q" in request.POST.keys():
            q=request.POST.get("q",None)
            lower_map = {
                ord(u'I'): u'ı',
                ord(u'İ'): u'i',
            }
            q= q.translate(lower_map).lower()
            for co in new_messages:
                title= co.mesaj.translate(lower_map).lower()
                if q in title:
                    messages.append(co)
            new_messages=messages
    context={
        "new_messages":new_messages,
    }
    return render(request,"AdminTemplates/messagesAdmin.html",context)





@permission_required('is_staff',login_url="loginAdmin")
def deleteMessagesAdmin(request,pk):
    obj=get_object_or_404(IletisimModel,pk=pk)
    obj.delete()
    messages.success(request,"Mesaj başarıyla silindi")
    return redirect(request.META['HTTP_REFERER']) 







@permission_required('is_staff',login_url="loginAdmin")
def listMenu(request,sayfa):
    topMenuler=topMenuModel.objects.all()
    bottomMenuler=bottomMenuModel.objects.all()
    context={
        "topMenuler":topMenuler,
        "bottomMenuler":bottomMenuler,
        "sayfa":sayfa
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
            meta_title=request.POST.get("meta_title",None)
            meta_description=request.POST.get("meta_description",None)
            meta_keywords=request.POST.get("meta_keywords",None)
            if menuId:
                MenuObje.name=name
                MenuObje.url=url
                MenuObje.menuSira=menuSira
                MenuObje.userType=userType
                MenuObje.meta_title=meta_title
                MenuObje.meta_description=meta_description
                MenuObje.meta_keywords=meta_keywords
                MenuObje.save()
                messages.success(request,"Üst menü modeli başarıyla güncellendi")
            else:
                topMenuModel.objects.create(name=name,url=url,userType=userType,menuSira=menuSira,meta_title=meta_title,meta_description=meta_description,meta_keywords=meta_keywords)
                messages.success(request,"Üst menü modeli başarıyla oluşturuldu")
            return redirect("listMenu",sayfa="ust-menu")
        elif type=="alt-menu-ekle":
            pk=request.POST.get("baglıMenu",None)
            if pk:
                topMenu=topMenuModel.objects.get(pk=pk)
                name=request.POST.get("menuName",None)
                url=request.POST.get("menuUrl",None)
                userType=request.POST.get("userType",None)
                menuSira=request.POST.get("menuSira",None)
                meta_title=request.POST.get("meta_title",None)
                meta_description=request.POST.get("meta_description",None)
                meta_keywords=request.POST.get("meta_keywords",None)
                if menuId:
                    MenuObje.topMenu=topMenu
                    MenuObje.name=name
                    MenuObje.url=url
                    MenuObje.menuSira=menuSira
                    MenuObje.userType=userType
                    MenuObje.meta_title=meta_title
                    MenuObje.meta_description=meta_description
                    MenuObje.meta_keywords=meta_keywords
                    MenuObje.save()
                    messages.success(request,"Alt menü modeli başarıyla güncellendi")
                else:
                    bottomMenuModel.objects.create(topMenu=topMenu,name=name,url=url,userType=userType,menuSira=menuSira,meta_title=meta_title,meta_description=meta_description,meta_keywords=meta_keywords)
                    messages.success(request,"Alt menü modeli başarıyla oluşturuldu")
                return redirect("listMenu",sayfa="alt-menu")
            else:
                messages.error(request,"Lütfen önce bir üst menü seçimi yapınız eğer yoksa önce üst menü modeli oluşturunuz.")
                return redirect("listMenu",sayfa="alt-menu")
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
    show="false"
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
        show="true"
        course=get_object_or_404(CourseModel,pk=courseId)
        form = CourseModelForm(instance=course)
    else:
        form = CourseModelForm()
    context={
        "form":form,
        "course":course,
        "show":show
        
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
    typeObj=request.GET.get("type",None)
    if typeObj == "course":
        course=get_object_or_404(CourseModel,slug=slug)
    elif typeObj == "blog":
        blog=get_object_or_404(blogModel,slug=slug)
    parent=get_object_or_404(CommentModel,pk=pk)
    if request.method == "POST":
        form=CommentModelForm(data=request.POST)
        if form.is_valid():
            data=form.save(commit=False)
            data.comment_user=request.user
            if typeObj == "course":
                data.course=course
            elif typeObj == "blog":
                data.blog=blog
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
    notifications=notificationModel.objects.all().order_by("-created_date")
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
    billings=orderModel.objects.all()
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
        pass
    else:
        logo=LogoModel.objects.create(name="Turkaze")
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







@permission_required('is_staff',login_url="loginAdmin")
def aydinlatmaMetniAdmin(request):
    metinler=aydinlatmaMetniModel.objects.all()
    if request.method == 'POST':
        if metinler:
            form=aydinlatmaMetniModelForm(request.POST or None,request.FILES or None,instance=metinler.first())
        else:
            form=aydinlatmaMetniModelForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request,"Aydınlatma Metni başarıyla kaydedildi.")
            return redirect("aydinlatmaMetniAdmin")
        else:
            messages.error(request,"Bir hata oluştu.Yönetici ile iletişime geçiniz.")
            return redirect("aydinlatmaMetniAdmin")
    else:
        if metinler:
            form = aydinlatmaMetniModelForm(instance=metinler.first())
        else:
            form = aydinlatmaMetniModelForm()
    context={
        "form":form,
        "type":"aydinlatma",
        "metin":"Aydınlatma Metni"
    }
    return render(request,"AdminTemplates/aydinlatmaMetniAdmin.html",context)








@permission_required('is_staff',login_url="loginAdmin")
def kvkkMetniAdmin(request):
    metinler=kvkkMetniModel.objects.all()
    if request.method == 'POST':
        if metinler:
            form=kvkkMetniModelForm(request.POST or None,request.FILES or None,instance=metinler.first())
        else:
            form=kvkkMetniModelForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request,"KVKK Metni başarıyla kaydedildi.")
            return redirect("kvkkMetniAdmin")
        else:
            messages.error(request,"Bir hata oluştu.Yönetici ile iletişime geçiniz.")
            return redirect("kvkkMetniAdmin")
    else:
        if metinler:
            form = kvkkMetniModelForm(instance=metinler.first())
        else:
            form = kvkkMetniModelForm()
    context={
        "form":form,
        "type":"kvkk",
        "metin":"KVKK Metni"
    }
    return render(request,"AdminTemplates/aydinlatmaMetniAdmin.html",context)







@permission_required('is_staff',login_url="loginAdmin")
def gizlilikMetniAdmin(request):
    metinler=gizlilikMetniModel.objects.all()
    if request.method == 'POST':
        if metinler:
            form=gizlilikMetniModelForm(request.POST or None,request.FILES or None,instance=metinler.first())
        else:
            form=gizlilikMetniModelForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request,"Gizlilik politikası başarıyla kaydedildi.")
            return redirect("gizlilikMetniAdmin")
        else:
            messages.error(request,"Bir hata oluştu.Yönetici ile iletişime geçiniz.")
            return redirect("gizlilikMetniAdmin")
    else:
        if metinler:
            form = gizlilikMetniModelForm(instance=metinler.first())
        else:
            form = gizlilikMetniModelForm()
    context={
        "form":form,
        "type":"gizlilik",
        "metin":"Gizlilik Politikası"
    }
    return render(request,"AdminTemplates/aydinlatmaMetniAdmin.html",context)






@permission_required('is_staff',login_url="loginAdmin")
def blogListAdmin(request):
    blogs=blogModel.objects.all().order_by("created_date")
    context={
        "blogs":blogs,
    }
    return render(request,"AdminTemplates/listBlogsAdmin.html",context)







@permission_required('is_staff',login_url="loginAdmin")
def createBlogModelAdmin(request):
    blog=""
    show="false"
    blogId=request.GET.get("blogId",None)
    if request.method == "POST":   
        if blogId:
            blog=get_object_or_404(blogModel,pk=blogId)
            form = blogModelForm(request.POST or None,request.FILES or None,instance=blog)	
        else:
            form = blogModelForm(request.POST or None,request.FILES or None)

        if form.is_valid(): 
            data=form.save(commit=False)            
            data.author=request.user
            data.save()
            form.save_m2m()   
            messages.success(request,"Blog başarıyla kaydedildi.")
            return redirect("blogListAdmin")
        else:
            messages.error(request,"İşleminiz gerçekleştirilemdi.Lütfen formu doğru doldurduğunuzdan emin olunuz.")
            return redirect("blogListAdmin")
    if blogId:
        show="true"
        blog=get_object_or_404(blogModel,pk=blogId)
        form = blogModelForm(instance=blog)
    else:
        form = blogModelForm()
    context={
        "form":form,
        "blog":blog,
        "show":show
    }
    return render(request,"AdminTemplates/addBlogAdmin.html",context)






@permission_required('is_staff',login_url="loginAdmin")
def deleteBlogAdmin(request,pk):
    obj=get_object_or_404(blogModel,pk=pk)
    obj.delete()
    messages.success(request,"Blog başarıyla silindi")
    return redirect(request.META['HTTP_REFERER']) 




@permission_required('is_staff',login_url="loginAdmin")
def blogCategoryListAdmin(request):
    categories=blogCategoryModel.objects.all().order_by("created_date")
    context={
        "categories":categories,
    }
    return render(request,"AdminTemplates/listBlogCategoriesAdmin.html",context)





@permission_required('is_staff',login_url="loginAdmin")
def addBlogCategoryAdmin(request):
    category=""
    categoryId=request.GET.get("categoryId",None)
    if request.method == "POST":   
        if categoryId:
            category=get_object_or_404(blogCategoryModel,pk=categoryId)
            form = blogCategoryModelForm(request.POST, request.FILES or None,instance=category)	
        else:
            form = blogCategoryModelForm(request.POST, request.FILES or None)	
        if form.is_valid(): 
            form.save()            
            messages.success(request,"Kategori başarıyla kaydedildi.")
            return redirect("blogCategoryListAdmin")
        else:
            messages.error(request,"İşleminiz gerçekleştirilemdi.Lütfen formu doğru doldurduğunuzdan emin olunuz.")
            return redirect("blogCategoryListAdmin")
    if categoryId:
        category=get_object_or_404(blogCategoryModel,pk=categoryId)
        form = blogCategoryModelForm(instance=category)
    else:
        form = blogCategoryModelForm()
    context={
        "form":form,
        "category":category
        
    }
    
    return render(request,"AdminTemplates/addBlogCategoryAdmin.html",context)






@permission_required('is_staff',login_url="loginAdmin")
def deleteCategoryBlogAdmin(request,pk):
    obj=get_object_or_404(blogCategoryModel,pk=pk)
    obj.delete()
    messages.success(request,"Kategori başarıyla silindi")
    return redirect(request.META['HTTP_REFERER']) 







@permission_required('is_staff',login_url="loginAdmin")
def socialMediaAdmin(request):
    metinler=socialModel.objects.all()
    if request.method == 'POST':
        if metinler:
            form=socialModelForm(request.POST or None,request.FILES or None,instance=metinler.first())
        else:
            form=socialModelForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request,"Sosyal medya ayarlarınız başarıyla kaydedildi.")
            return redirect("socialMediaAdmin")
        else:
            messages.error(request,"Bir hata oluştu.Yönetici ile iletişime geçiniz.")
            return redirect("socialMediaAdmin")
    else:
        if metinler:
            form = socialModelForm(instance=metinler.first())
        else:
            form = socialModelForm()
    context={
        "form":form,
    }
    return render(request,"AdminTemplates/socialMediaAdmin.html",context)







@permission_required('is_staff',login_url="loginAdmin")
def mesafeliSatisAdmin(request):
    metinler=mesafeliSatisModel.objects.all()
    if request.method == 'POST':
        if metinler:
            form=mesafeliSatisModelForm(request.POST or None,request.FILES or None,instance=metinler.first())
        else:
            form=mesafeliSatisModelForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request,"Mesafeli satış sözleşmesi başarıyla kaydedildi.")
            return redirect("mesafeliSatisAdmin")
        else:
            messages.error(request,"Bir hata oluştu.Yönetici ile iletişime geçiniz.")
            return redirect("mesafeliSatisAdmin")
    else:
        if metinler:
            form = mesafeliSatisModelForm(instance=metinler.first())
        else:
            form = mesafeliSatisModelForm()
    context={
        "form":form,
        "type":"mesafeli",
        "metin":"Mesafeli Satış Sözleşmesi"
    }
    return render(request,"AdminTemplates/aydinlatmaMetniAdmin.html",context)






@permission_required('is_staff',login_url="loginAdmin")
def listFooterMailAdmin(request):
    emails=footerMailModel.objects.all()
    context={
        "emails":emails,
    }
    return render(request,"AdminTemplates/listFooterMailAdmin.html",context)





@permission_required('is_staff',login_url="loginAdmin")
def deleteFooterMail(request,pk):
    obj=get_object_or_404(footerMailModel,pk=pk)
    obj.delete()
    messages.success(request,"Email başarıyla silindi")
    return redirect(request.META['HTTP_REFERER']) 








@permission_required('is_staff',login_url="loginAdmin")
def hakkimizdaAdmin(request):
    metinler=hakkimizdaModel.objects.all()
    if request.method == 'POST':
        if metinler:
            form=hakkimizdaModelForm(request.POST or None,request.FILES or None,instance=metinler.first())
        else:
            form=hakkimizdaModelForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request,"Hakkımızda modeli başarıyla kaydedildi.")
            return redirect("hakkimizdaAdmin")
        else:
            messages.error(request,"Bir hata oluştu.Yönetici ile iletişime geçiniz.")
            return redirect("hakkimizdaAdmin")
    else:
        if metinler:
            form = hakkimizdaModelForm(instance=metinler.first())
        else:
            form = hakkimizdaModelForm()
    context={
        "form":form,
        "type":"hakkimizda",
        "metin":"Hakkımızda"
    }
    return render(request,"AdminTemplates/aydinlatmaMetniAdmin.html",context)





@permission_required('is_staff',login_url="loginAdmin")
def pastAppointmentsAdmin(request):
    appointments1=appointmentModel.objects.filter(status="yes",date__lte=datetime.datetime.today().date()).order_by("-date")
    appointments=list()
    for i in appointments1:
        if i.date==datetime.datetime.today().date():
            if i.finishing_time>datetime.datetime.now().time():
                pass
            else:
                appointments.append(i)
        else:
            appointments.append(i)
   
    context={
        "appointments":appointments,
        "type":"past",
    }
    return render(request,"AdminTemplates/listAppointmentsAdmin.html",context)









@permission_required('is_staff',login_url="loginAdmin")
def nextAppointmentsAdmin(request):
    appointments1=appointmentModel.objects.filter(status="yes",date__gte=datetime.datetime.today().date()).order_by("-date")
    appointments=list()
    for i in appointments1:
        if i.date==datetime.datetime.today().date():
            if i.finishing_time<datetime.datetime.now().time():
                pass
            else:
                appointments.append(i)
        else:
            appointments.append(i)
   
    context={
        "appointments":appointments,
        "type":"next",
    }
    return render(request,"AdminTemplates/listAppointmentsAdmin.html",context)






@permission_required('is_staff',login_url="loginAdmin")
def listAppointmentsAdmin(request):
    appointments=appointmentModel.objects.filter(status="pending").order_by("-date")
    context={
        "appointments":appointments,
        "type":"requests",
    }
    return render(request,"AdminTemplates/listAppointmentsAdmin.html",context)




@permission_required('is_staff',login_url="loginAdmin")
def acceptAppointmentsAdmin(request,pk):
    appointment=get_object_or_404(appointmentModel,pk=pk)
    appointment.status="yes"
    appointment.save()
    try:
        send_mail(
            "Merhaba, "+appointment.fullname,
            "turkazepsikolog.com sitesine göndermiş olduğunuz "+str(appointment.date)+" tarihli "+str(appointment.starting_time)+" / "+str(appointment.finishing_time)+" saatine gönderilmiş randevu talebiniz onaylanmıştır.Bilginize sunarız..\n\n",
             appointment.phone_number,
            [appointment.email,]
        )
        messages.success(request,"Randevunuz başarıyla oluşturuldu.Kullanıcının iletişimin bilgileriyle iletişime geçebilirsiniz.")
    except:
        messages.success(request,"Randevu başarıyla oluşturuldu fakat kullanıcının mail hesabına bilgilendirme maili iletilemedi.")
    return redirect("listAppointmentsAdmin")





@permission_required('is_staff',login_url="loginAdmin")
def deleteAppointmentRequestAdmin(request,pk):
    appointment=get_object_or_404(appointmentModel,pk=pk)
    appointment.status="no"
    appointment.save()
    try:
        send_mail(
            "Merhaba, "+appointment.fullname,
            "turkazepsikolog.com sitesine göndermiş olduğunuz "+str(appointment.date)+" tarihli "+str(appointment.starting_time)+" / "+str(appointment.finishing_time)+" saatine gönderilmiş randevu talebiniz reddedilmiştir.Bilginize sunarız..\n\n",
             appointment.phone_number,
            [appointment.email,]
        )
        messages.success(request,"Randevunuz başarıyla reddedildi ve kullanıcıya mail gönderildi.")
    except:
        messages.success(request,"Randevu başarıyla oluşturuldu fakat kullanıcının mail hesabına bilgilendirme maili iletilemedi.")
    return redirect("listAppointmentsAdmin")





@permission_required('is_staff',login_url="loginAdmin")
def listUsersAndVideosStat(request,pk):
    course=get_object_or_404(CourseModel,pk=pk)
    users=CustomUserModel.objects.all()
    lastUsers=list()
    for user in users:
        isExist=orderModel.objects.filter(user=user,course=course,status="yes").all()
        if isExist:
            lastUsers.append(user)
            
    context={
        "users":lastUsers,
        "course":course
    }
    return render(request,"AdminTemplates/listUsersAndVideosStat.html",context)






@permission_required('is_staff',login_url="loginAdmin")
def listCoursesStat(request):
    courses=CourseModel.objects.all()
    context={
        "courses":courses,
    }
    return render(request,"AdminTemplates/listCoursesStat.html",context)






@permission_required('is_staff',login_url="loginAdmin")
def showVideoStatusDetail(request,slug):
    user=get_object_or_404(CustomUserModel,slug=slug)
    courseId=request.GET.get("courseId",None)
    course=get_object_or_404(CourseModel,pk=courseId)
    videos=list()
    for watched in hasWatchedModel.objects.filter(user=user).all():
        if watched.video.courseSession.course == course:
            videos.append(watched)
    context={
        "user":user,
        "videos":videos,
    }
    return render(request,"AdminTemplates/showVideoStatusDetail.html",context)





@permission_required('is_staff',login_url="loginAdmin")
def appointmentsAdmin(request):
    appointments=appointmentAdminModel.objects.all().order_by("date")
    context={
        "appointments":appointments,
    }
    return render(request,"AdminTemplates/appointmentsAdmin.html",context)
    





@permission_required('is_staff',login_url="loginAdmin")
def addAppointmentsAdmin(request):
    if request.method == "POST":   
        form = appointmentAdminModelForm(request.POST, request.FILES or None)		
        if form.is_valid(): 
            data=form.save(commit=False)         
            finish=form.cleaned_data.get('finishing_time')
            start=form.cleaned_data.get('starting_time')
            date=form.cleaned_data.get('date')
            today=datetime.date.today()
            if today > date:
                messages.error(request,"Girilen tarih bilgisi bugünden önce olamaz.")
                return redirect("addAppointmentsAdmin")
            if start >= finish:
                messages.error(request,"Bitiş zamanı başlangıç zamanından önce  veya eşit olamaz.")
                return redirect("addAppointmentsAdmin")
            start = datetime.datetime.strptime(start, '%H:%M')
            finish = datetime.datetime.strptime(finish, '%H:%M')
            difference=datetime.datetime.combine(date.today(), finish.time()) - datetime.datetime.combine(date.today(), start.time())
            dd=str(difference).split(":")
            x=0
            oldAppointments=appointmentAdminModel.objects.filter(date=date)
            oldAppointmentListTimes=list()
            if oldAppointments:
                oldAppoinment=oldAppointments.first()
                data=oldAppoinment
                oldAppointmentList=appointmentModel.objects.filter(top=oldAppoinment)
                for old in oldAppointmentList:
                    oldAppointmentListTimes.append(old.starting_time)
            else:
                data.save()
            for i in range(int(dd[0])):
                ss=start+datetime.timedelta(hours=x)
                isBreak=str(ss.time()).split(":")[0]
                if isBreak!="13" and ss.time() not in oldAppointmentListTimes :
                    appointmentModel.objects.create(top=data,date=date,starting_time=ss.time(),finishing_time=(start+datetime.timedelta(hours=x+1)).time())
                x+=1
        
           
            messages.success(request,"Randevularınız başarıyla kaydedildi.")
            return redirect("appointmentsAdmin")
        else:
            messages.error(request,"İşleminiz gerçekleştirilemdi.Lütfen formu doğru doldurduğunuzdan emin olunuz.")
            return redirect("appointmentsAdmin")
    form = appointmentAdminModelForm()
    context={
        "form":form,
    }
    return render(request,"AdminTemplates/addAppointmentAdmin.html",context)







@permission_required('is_staff',login_url="loginAdmin")
def deleteAppointmentOfAdmin(request,pk):
    obj=get_object_or_404(appointmentAdminModel,pk=pk)
    obj.delete()
    messages.success(request,"Randevu tarihi ve o tarihli randevular başarıyla silindi")
    return redirect(request.META['HTTP_REFERER']) 





@permission_required('is_staff',login_url="loginAdmin")
def showAppointmentsScheduleAdmin(request,pk):
    add=get_object_or_404(appointmentAdminModel,pk=pk)
    schedules=appointmentModel.objects.filter(date=add.date).order_by("starting_time")
    context={
        "schedules":schedules,
    }
    return render(request,"AdminTemplates/detailOfAppointmentsAdminModel.html",context)
    




@permission_required('is_staff',login_url="loginAdmin")
def showDetailOrderAdmin(request,pk):
    order=get_object_or_404(orderModel,pk=pk)
    context={
        "order":order,
    }
    return render(request,"AdminTemplates/billingDetailAdmin.html",context)
    