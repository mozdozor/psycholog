import calendar
import datetime
from email import message
import math
from unicodedata import category
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render,HttpResponse
from Admin.forms import CommentModelForm, IletisimModelForm, appointmentAdminModelForm, appointmentModelForm, footerMailModelForm
from Admin.models import CategoryModel, CourseModel, appointmentAdminModel, appointmentModel, aydinlatmaMetniModel, blogCategoryModel, blogModel, courseSessionModel, courseSessionVideoModel, footerMailModel, gizlilikMetniModel, hakkimizdaModel, kvkkMetniModel, mesafeliSatisModel, notificationModel, topMenuModel, whatWillYouLearnModel
from django.contrib.auth import logout
from Admin.templatetags.coutOfNoneWatched import getCountOfNoneWatchedVideo
from psikolog.forms import CommentModelStarsForm, registerUserForm, userSettingsProfileModelForm
from psikolog.models import CommentModel, CustomUserModel, billingCourseModel, favouriteCourseModel, hasWatchedModel, orderModel, sliderModel
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate,update_session_auth_hash,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.mail import send_mail,EmailMessage
from django.db.models import Avg
from django.db.models import Q
import base64
import hmac
import hashlib
import requests
import json
import environ
import secrets
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
UserModel = get_user_model()

# Create your views here.



def index(request):
    page=topMenuModel.objects.filter(url="/").all()
    sliders=sliderModel.objects.all().order_by("sira")
    courses=CourseModel.objects.all().order_by("created_date")
    categories=CategoryModel.objects.all().order_by("created_date")
    blogs=blogModel.objects.all().order_by("created_date")[:2]
    metinler=hakkimizdaModel.objects.all()
    metin=""
    if metinler:
        metin=metinler.first()
    context={
        "sliders":sliders,
        "courses":courses,
        "categories":categories,
        "blogs":blogs,
        "page":page.first(),
        "metin":metin
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







def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUserModel.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request,user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect("index")
    else:
        return HttpResponse('Activation link is invalid!')









def registerUser(request):
    if request.method == "POST":
        form = registerUserForm(request.POST or None)
        if form.is_valid():
            data=form.save(commit=False)
            data.username= form.cleaned_data.get("email")
            data.image="avatar/no-avatar.png"
            data.is_active = False
            data.save()

            current_site = request.META['HTTP_HOST']   
            mail_subject = 'Hesabını aktif et.'
            message = render_to_string('acc_active_email.html', {
                'user': data,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(data.pk)),
                'token': default_token_generator.make_token(data),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, "email_not.html",{"note":"Mail adresinizden linke tıklayarak kaydınızı tamamlayınız","class_name":"fas fa-envelope"})


            # email = form.cleaned_data.get("email")
            # password = form.cleaned_data.get("password1")
            # user = authenticate(username=email,password=password)
            # auth_login(request,user)
            # return redirect("index")
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
    nextCourse=""
    isNextPage=""
    if 'nextCourse' in request.session:
        nextCourse = request.session['nextCourse']
        del request.session['nextCourse']
    if 'nextPage' in request.session:
        isNextPage = request.session['nextPage']
        del request.session['nextPage']
    if nextCourse:
        pass
    else:
        nextCourse=request.GET.get("next",None)
    if request.method == "POST":
        form = userSettingsProfileModelForm(request.POST or None,request.FILES or None,instance=request.user)  	
        if form.is_valid():
            form.save()          
            if nextCourse:
                request.session['nextPage'] = nextCourse
                messages.success(request,'Bilgileriniz başarıyla güncellendi.Satın alma sayfasına yönlendiriliyorsunuz.Lütfen bekleyiniz.')
                return redirect("profileSettings")
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
        "nextCourse":nextCourse,
        "isNextPage":isNextPage
    }
    return render(request,"profileSettings.html",context)




def coursesGridList(request):
    page=topMenuModel.objects.filter(url="/tum-kurslar").all()
    selectedCategories=[]
    selectedStars=[]
    courses=CourseModel.objects.all()
    categories=CategoryModel.objects.all()
    secondCourses=list()
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
        if 'q' in request.POST.keys():
            q=request.POST.get("q",None)
            lower_map = {
                ord(u'I'): u'ı',
                ord(u'İ'): u'i',
            }
            q= q.translate(lower_map).lower()
            for co in courses:
                title= co.title.translate(lower_map).lower()
                if q in title:
                    secondCourses.append(co)
            courses=secondCourses
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
        "selectedStars":selectedStars,
        "page":page.first()
    }
    return render(request,"courses-grid-sidebar.html",context)




@login_required(login_url="login")
def favouritesCoursesGridList(request):
    page=topMenuModel.objects.filter(url="/favori-kurslar").all()
    courses=request.user.favouriteCourses.all()
    context={
        "courses":courses,
        "page":page.first()
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
    completed=""
    videoIds=list()
    form=CommentModelStarsForm()
    course=get_object_or_404(CourseModel,slug=slug)
    learns=whatWillYouLearnModel.objects.filter(course=course).order_by("created_date")
    sessions=courseSessionModel.objects.filter(course=course).order_by("created_date")
    comments=CommentModel.objects.filter(course=course,parent=None).order_by("created_date")
    has_bougth="false"
    for session in sessions:
        for video in session.getVideos():
            videoIds.append(video.pk)
    videoIds = json.dumps(videoIds)
    if request.user.is_authenticated:
        NoneWatched=getCountOfNoneWatchedVideo(request.user.pk,course.pk)
        if NoneWatched==0 and course.countOfVideos() != 0:
            completed="true"
        billings=orderModel.objects.filter(user=request.user,course=course,status="yes").all()
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
        "has_bougth":has_bougth,
        "videoIds":videoIds,
        "completed":completed,
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
    page=topMenuModel.objects.filter(url="/ogrenim-icerigim").all()
    courses=orderModel.objects.filter(user=request.user,status="yes")
    context={
        "courses":courses,
        "page":page.first()
    }
    return render(request,"learning-content.html",context)





def aboutUs(request):
    user=CustomUserModel.objects.filter(is_staff=True).first()
    metinler=hakkimizdaModel.objects.all()
    page=topMenuModel.objects.filter(url="/hakkimizda").all()
    courses=CourseModel.objects.all()
    metin=""
    if metinler:
        metin=metinler.first()
    context={
        "metin":metin,
        "metinType":"hakkimizda",
        "printMetin":"Hakkımızda",
        "page":page.first(),
        "user":user,
        "courseCount":courses.count(),
        "courses":courses
    }
   
    return render(request,"newAbout.html",context)




def contact(request):
    user=CustomUserModel.objects.filter(is_staff=1).first()
    page=topMenuModel.objects.filter(url="/iletisim").all()
    if request.method == "POST":
        form = IletisimModelForm(request.POST)
        if form.is_valid(): 
            form.save()
            try:
                send_mail(
                    form.cleaned_data["name"]+" "+ form.cleaned_data["lastName"],
                    "turkazepsikolog.com sitesinden yeni bir mailiniz var.\n\n"+form.cleaned_data["mesaj"]+"\n\n\n Gönderen kişi= "+form.cleaned_data["email"],
                    form.cleaned_data["phone_number"],
                    ["turkazepsikolog@gmail.com",],
                )
                messages.success(request,"Mesajınız başarıyla tarafımıza iletildi.En kısa sürede sizinle iletişime geçilecektir.Teşekkür ederiz.",extra_tags="contactMessages")
                return redirect("contact")  
            except:
                messages.error(request,"Mesajınız gönderilirken bir hata oldu.Lütfen yönetici ile iletişime geçiniz.",extra_tags="contactMessages")
                return redirect("contact")

            
    form = IletisimModelForm()
    context={
        "form":form,
        "address":user.address,
        "page":page.first()
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
        "categories":categories,
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
    page=topMenuModel.objects.filter(url="/tum-blog-yazilari").all()
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
        "searchKey":searchKey,
        "page":page.first()
        
    }
    return render(request,"blog-lists.html",context)






def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip




currentCourse=""
currentUser=""





@login_required(login_url="login")
def paymentPage(request,slug):
    course=get_object_or_404(CourseModel,slug=slug)
    has_created_order=orderModel.objects.filter(course=course,user=request.user,status="no")
    if has_created_order:
        orderOfUser=has_created_order.first()
    else:
        merchant_oid = "SPR"+secrets.token_hex(10)
        orderOfUser=orderModel.objects.create(course=course,user=request.user,status="no",merchant_oid=merchant_oid,price=course.price)
    env = environ.Env()
    environ.Env.read_env("../config/.env")
    merchant_id = env("merchant_id")
    merchant_key = env("merchant_key").encode('UTF-8')
    merchant_salt = env("merchant_salt").encode('UTF-8')
    email = request.user.email
    payment_amount = (course.price)* 100 
    user_name = request.user.get_full_name()
    user_address = request.user.address
    if user_address == None or user_address=="":
        messages.error(request,"Ödeme sayfasına girmek için lütfen önce adres bilginizi güncelleyiniz.")
        request.session['nextCourse'] = course.slug
        return redirect("profileSettings")
    user_phone = request.user.phone_number
    merchant_ok_url = 'http://'+request.META['HTTP_HOST']+'/basarili-odeme/'+course.slug+"?user="+request.user.slug  #turkaze olarak değiştirirelecek
    merchant_fail_url = 'http://'+request.META['HTTP_HOST']+'/hatali-odeme/'+course.slug  #turkaze olarak değiştirirelecek
    user_basket = base64.b64encode(json.dumps([[course.title, payment_amount, 1],]).encode('UTF-8'))
    user_ip = get_client_ip(request)  #canlıda test yap
    timeout_limit = '30'
    debug_on = '0'   #canlıda 0 yap
    test_mode = '0' # Mağaza canlı modda iken test işlem yapmak için 1 olarak gönderilebilir.
    no_installment = '0' # Taksit yapılmasını istemiyorsanız, sadece tek çekim sunacaksanız 1 yapın
    max_installment = '0'
    currency = 'TL'
        # Bu kısımda herhangi bir değişiklik yapmanıza gerek yoktur.
    hash_str = str(merchant_id) + str(user_ip) + str(orderOfUser.merchant_oid) + str(email) + str(payment_amount) + user_basket.decode() + no_installment + max_installment + currency + test_mode
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode('UTF-8') + merchant_salt, hashlib.sha256).digest())
    params = {
        'merchant_id': merchant_id,
        'user_ip': user_ip,
        'merchant_oid': orderOfUser.merchant_oid,
        'email': email,
        'payment_amount': payment_amount,
        'paytr_token': paytr_token,
        'user_basket': user_basket,
        'debug_on': debug_on,
        'no_installment': no_installment,
        'max_installment': max_installment,
        'user_name': user_name,
        'user_address': user_address,
        'user_phone': user_phone,
        'merchant_ok_url': merchant_ok_url,
        'merchant_fail_url': merchant_fail_url,
        'timeout_limit': timeout_limit,
        'currency': currency,
        'test_mode': test_mode
    }

    result = requests.post('https://www.paytr.com/odeme/api/get-token', params)
    res = json.loads(result.text)
    context={
        "course":course,
        'token': res['token']
        
    }
    if res['status'] == 'success':
        print("success")
      
    else:
        context["failMessage"]="Ödeme formu açılırken bir hata ile karşılaşıldı.Sistem yöneticiniz ile ileişime geçiniz"
        return render(request,"fail-payment.html",context)

    return render(request,"payment-page.html",context)










@csrf_exempt
def callback(request):  
    env = environ.Env()
    environ.Env.read_env("../config/.env")
    if request.method != 'POST':
        return HttpResponse(str(''))

    post = request.POST


    # BURADA YAPILMASI GEREKENLER
    # 1) Siparişin durumunu post['merchant_oid'] değerini kullanarak veri tabanınızdan sorgulayın.
    # 2) Eğer sipariş zaten daha önceden onaylandıysa veya iptal edildiyse "OK" yaparak sonlandırın.
    order=orderModel.objects.get(merchant_oid=post['merchant_oid'])

    if post['status'] == 'success':  # Ödeme Onaylandı

        order.status="yes"
        order.save()
        """
        BURADA YAPILMASI GEREKENLER
        1) Siparişi onaylayın.
        2) Eğer müşterinize mesaj / SMS / e-posta gibi bilgilendirme yapacaksanız bu aşamada yapmalısınız.
        3) 1. ADIM'da gönderilen payment_amount sipariş tutarı taksitli alışveriş yapılması durumunda değişebilir. 
        Güncel tutarı post['total_amount'] değerinden alarak muhasebe işlemlerinizde kullanabilirsiniz.
        """
        print(request)
    else:  # Ödemeye Onay Verilmedi
        """
        BURADA YAPILMASI GEREKENLER
        1) Siparişi iptal edin.
        2) Eğer ödemenin onaylanmama sebebini kayıt edecekseniz aşağıdaki değerleri kullanabilirsiniz.
        post['failed_reason_code'] - başarısız hata kodu
        post['failed_reason_msg'] - başarısız hata mesajı
        """
        print(request)

    # Bildirimin alındığını PayTR sistemine bildir.
    return HttpResponse(str('OK'))











@login_required(login_url="login")
def successPayment(request,slug):
    userSlug=request.GET.get("user",None)
    user=get_object_or_404(CustomUserModel,slug=userSlug)
    course=get_object_or_404(CourseModel,slug=slug)
    message=str(course.title)+" adlı kursunuz "+user.get_full_name()+" tarafından satın alınmıştır.Sipariş kısmından kontrol edebilirsiniz"
    notificationModel.objects.create(title="Kurs Satın Alımı",message=message,type="billing",object=course)
    try:
        send_mail(
            "Yeni kurs satın alımı",
            "turkazepsikolog.com sitesinden "+ "yeni bir mailiniz var.\n\n"+message+"\n\n\n ",
             user.phone_number,
            ["turkazepsikolog@gmail.com",],
        )
    except:
        messages.error(request,"Mail Gönderilemedi.")
    context={
        "course":course,
        
    }
    return render(request,"success-payment.html",context)






@login_required(login_url="login")
def failPayment(request,slug):
    course=get_object_or_404(CourseModel,slug=slug)
    context={
        "course":course,
        
    }
    return render(request,"fail-payment.html",context)








def mesafeliSatis(request):
    metinler=mesafeliSatisModel.objects.all()
    metin=""
    if metinler:
        metin=metinler.first()
    context={
        "metin":metin,
        "metinType":"mesafeli",
        "printMetin":"Mesafeli Satış Sözleşmesi",
    }
    return render(request,"metinler.html",context)







@csrf_exempt
def footerMailSave(request):
    if request.method == 'POST':
        email=request.POST["email"]
        footerList=list(footerMailModel.objects.all().values_list('email', flat=True)) 
        if email in footerList:
            messages.error(request,"Email adresiniz daha önce kaydedilmiş",extra_tags="footerMail")
            return redirect(request.META['HTTP_REFERER'])
        footerMailModel.objects.create(email=email)
        messages.success(request,"Email adresiniz başarıyla kaydedildi",extra_tags="footerMail")
        return redirect(request.META['HTTP_REFERER'])
  






def get_days_from_today():
    days=[]
    my_date = datetime.date.today()
    a = calendar.day_name[my_date.weekday()]  
    if(a!="Monday" and a!="Tuesday" and a!="Wednesday" and a!="Thursday" and a!="Friday" and a!="Saturday" and a!="Sunday"):
        a=getDayEnglish(a)
    if a!="Sunday":
        days.append(a)
    weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    index=weekdays.index(a)
    for i in range(6-index):
        if (weekdays[i+index+1] != "Sunday"):
            days.append(weekdays[i+index+1])
    for i in range(index):
        if(weekdays[i]!="Sunday"):
            days.append(weekdays[i])
    return days





def getDayEnglish(day):
    if day == "Pazartesi":
        day="Monday"
    elif day == "Salı":
        day="Tuesday"
    elif day == "Çarşamba":
        day="Wednesday"
    elif day == "Perşembe":
        day="Thursday"
    elif day == "Cuma":
        day="Friday"
    elif day == "Cumartesi":
        day="Saturday"
    elif day == "Pazar":
        day="Sunday"
    return day




def getDayTurkish(day):
    if day == "Monday":
        day="Pazartesi"
    elif day == "Tuesday":
        day="Salı"
    elif day == "Wednesday":
        day="Çarşamba"
    elif day == "Thursday":
        day="Perşembe"
    elif day == "Friday":
        day="Cuma"
    elif day == "Saturday":
        day="Cumartesi"
    elif day == "Sunday":
        day="Pazar"
    return day





def get_dates():
    dates={
        "Pazartesi":find_date("Pazartesi"),
        "Salı":find_date("Salı"),
        "Çarşamba":find_date("Çarşamba"),
        "Perşembe":find_date("Perşembe"),
        "Cuma":find_date("Cuma"),
        "Cumartesi":find_date("Cumartesi"),
        "Pazar":find_date("Pazar"),
    }
    return dates




def find_date(week_day):
    day=getDayEnglish(week_day)
    my_date = datetime.date.today()
    a = calendar.day_name[my_date.weekday()]  
    if(a!="Monday" and a!="Tuesday" and a!="Wednesday" and a!="Thursday" and a!="Friday" and a!="Saturday" and a!="Sunday"):
        a=getDayEnglish(a)
    weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    now = weekdays.index(a)
    coming_day_index = weekdays.index(day)
    if coming_day_index<now:
        date = my_date + datetime.timedelta(days= 7+coming_day_index-now)
    else:
        date=my_date + datetime.timedelta(days= coming_day_index-now)
    # if coming_day_index>=now:
    #     date = my_date - timedelta(days= now - coming_day_index)
    # else:
    #     date = my_date + timedelta(days= 6)
    return date





def getShorNameOfDays(days):
    for i in days:
        if i=="Pazartesi":
            i="Ptesi"
        elif i == "Çarşamba":
            i="Çrş"
        elif i == "Perşembe":
            i="Prş"
        elif i == "Cumartesi":
            i="Ctesi"
    return days






def times(request):
    page=topMenuModel.objects.filter(url="/uygun-zamanlar").all()
    todaySchedules=appointmentModel.objects.filter(date=datetime.datetime.today().date())
    form = appointmentModelForm()
    engdays=get_days_from_today()
    days=[]
    for i in engdays:
        days.append(getDayTurkish(i))
    schedules1=appointmentModel.objects.filter(date=find_date(days[0]))
    schedules2=appointmentModel.objects.filter(date=find_date(days[1]))
    schedules3=appointmentModel.objects.filter(date=find_date(days[2]))
    schedules4=appointmentModel.objects.filter(date=find_date(days[3]))
    schedules5=appointmentModel.objects.filter(date=find_date(days[4]))
    schedules6=appointmentModel.objects.filter(date=find_date(days[5]))
    # schedules7=appointmentModel.objects.filter(date=find_date(days[6]))
    for dd, item in enumerate(days):
        if days[dd]=="Pazartesi":
            item = "Ptesi"
        elif days[dd] == "Çarşamba":
            item = "Çrş"
        elif days[dd] == "Perşembe":
            item = "Prş"
        elif days[dd] == "Cumartesi":
            item="Ctesi"
        days[dd]=item
    context={
        "days":days,
        "schedules1":schedules1,
        "schedules2":schedules2,
        "schedules3":schedules3,
        "schedules4":schedules4,
        "schedules5":schedules5,
        "schedules6":schedules6,
        "form":form,
        "todaySchedules":todaySchedules,
        "page":page.first()
        # "schedules7":schedules7,
    }
    return render(request,"times.html",context)







def appointment(request,randevuId):
    page=topMenuModel.objects.filter(url="/randevu-talebi").all()
    user=CustomUserModel.objects.filter(is_staff=1).first()
    schedule=get_object_or_404(appointmentModel,pk=randevuId)
    isFree="yes"
    if schedule.status!="no":
        isFree="notNo"

    if request.method == "POST":
        form = appointmentModelForm(request.POST)
        if form.is_valid(): 
            data=form.save(commit=False)
            if schedule.status!="no":
                return redirect("times")
            schedule.status="pending"
            schedule.phone_number=form.cleaned_data["phone_number"]
            schedule.email=form.cleaned_data["email"]
            schedule.message=form.cleaned_data["message"]
            schedule.fullname=form.cleaned_data["fullname"]
            schedule.save()
            message=form.cleaned_data["fullname"]+" adlı kişiden "+form.cleaned_data["category"].name+" kategorisi ile ilgili " +str((schedule.date).strftime('%d/%m/%Y'))+" tarihinde "+str(schedule.starting_time)+"/"+str((schedule.finishing_time))+" saatlerinde bir randevu isteiğiniz bulunmaktadır."
            notificationModel.objects.create(title="Randevu Talebi",message=message,type="appointment",appointmentObject=schedule)
            try:
                send_mail(
                    form.cleaned_data["fullname"],
                    "turkazepsikolog.com sitesinden "+ "yeni bir mailiniz var.\n\n"+message+"\n\n\n Gönderen kişi= "+form.cleaned_data["email"]+"\n Telefon = "+form.cleaned_data["phone_number"]+"\n Mesaj = "+form.cleaned_data["message"],
                    form.cleaned_data["phone_number"],
                    ["turkazepsikolog@gmail.com",],
                )
                messages.success(request,"Mesajınız başarıyla tarafımıza iletildi.En kısa sürede sizinle iletişime geçilecektir.Teşekkür ederiz.",extra_tags="appointmentMessages")
                data.save()
                
                return redirect("appointment",randevuId=randevuId)
            except:
                messages.error(request,"Bir hata ile karşılaşıldı.",extra_tags="appointmentMessages")
                return redirect("appointment",randevuId=randevuId)
      
    form = appointmentModelForm()
    context={
        "form":form,
        "address":user.address,
        "page":page.first(),
        "isFree":isFree,
        "randevuId":randevuId
    }
    return render(request,"appointment.html",context)







def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'





@csrf_exempt
def addWatchedList(request):
    if request.user.is_authenticated:
        if is_ajax(request=request):
            videoId=request.POST["videoId"]
            courseId=request.POST["courseId"]
            video=courseSessionVideoModel.objects.get(id=videoId)
            listOfAllWatched=hasWatchedModel.objects.filter(user=request.user,video=video)
            if listOfAllWatched:
                pass
            else:
                hasWatchedModel.objects.create(user=request.user,video=video)
            NoneWatched=getCountOfNoneWatchedVideo(request.user.pk,courseId)
            if NoneWatched==0:
                return JsonResponse({"complete":"success"}, status = 200)
            else:
                return JsonResponse({"complete":"fail"}, status = 200)
        else:
            return JsonResponse({}, status = 400)
        print(message)
    return JsonResponse({}, status = 400)








@csrf_exempt
def getAppointments(request):
    if is_ajax(request=request):
            dateLong=request.POST["date"]
            date=dateLong.split("T")[0]
            date=datetime.datetime.strptime(date, "%Y-%m-%d").date()
            schedules=appointmentModel.objects.filter(date=date).order_by("starting_time").values()
            return JsonResponse({"schedules":list(schedules)}, status = 200)
    else:
        return JsonResponse({}, status = 400)








@csrf_exempt
def submitAppointmentForm(request,randevuId):
    if is_ajax(request=request):
        if request.method == "POST":
            schedule=get_object_or_404(appointmentModel,pk=randevuId)
            form = appointmentModelForm(request.POST, request.FILES or None,instance=schedule)	
            if form.is_valid(): 
                form.save()  
                schedule.status="pending"
                schedule.save()
                message=form.cleaned_data["fullname"]+" adlı kişiden "+form.cleaned_data["category"].name+" kategorisi ile ilgili " +str((schedule.date).strftime('%d/%m/%Y'))+" tarihinde "+str(schedule.starting_time)+"/"+str((schedule.finishing_time))+" saatlerinde bir randevu isteiğiniz bulunmaktadır."
                notificationModel.objects.create(title="Randevu Talebi",message=message,type="appointment",appointmentObject=schedule)
                try:
                    send_mail(
                        form.cleaned_data["fullname"],
                        "turkazepsikolog.com sitesinden "+ "yeni bir mailiniz var.\n\n"+message+"\n\n\n Gönderen kişi= "+form.cleaned_data["email"]+"\n Telefon = "+form.cleaned_data["phone_number"]+"\n Mesaj = "+form.cleaned_data["message"],
                        form.cleaned_data["phone_number"],
                        ["turkazepsikolog@gmail.com",],
                    )
                    messages.success(request,"Mesajınız başarıyla tarafımıza iletildi.En kısa sürede sizinle iletişime geçilecektir.Teşekkür ederiz.",extra_tags="appointmentMessages")
                    schedules=appointmentModel.objects.filter(date=schedule.date).order_by("starting_time").values()
                    return JsonResponse({"status":"success","randevuId":randevuId,"schedules":list(schedules)}, status = 200)
                except:
                    return JsonResponse({"status":"error","randevuId":randevuId}, status = 200)
                
    else:
        return JsonResponse({}, status = 400)