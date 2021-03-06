import datetime
from email.policy import default
from unicodedata import category
from urllib import request
from autoslug import AutoSlugField
from django.db import models

from psikolog.models import CommentModel, CustomUserModel, favouriteCourseModel
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField


# Create your models here.




class topMenuModel(models.Model):
    name=models.CharField(max_length=100,blank=True,null=True)   
    url=models.CharField(max_length=150,blank=True,null=True)   
    userType=models.CharField(max_length=100,blank=True,null=True)   
    menuType=models.CharField(max_length=100,blank=True,null=True,default="Üst Menü")   
    menuSira=models.SmallIntegerField(default=0)
    meta_title=models.CharField(max_length=65,blank=True,null=True) 
    meta_description=models.CharField(max_length=170,blank=True,null=True)   
    meta_keywords=models.CharField(max_length=100,blank=True,null=True)    


    class Meta:
        db_table="topMenuModel"
        verbose_name ="Üst Menü"  
        verbose_name_plural ="Üst Menüler"

    def __str__(self):
        return self.name


    def get_bottom_menuler(self):
        return bottomMenuModel.objects.filter(topMenu=self).order_by("menuSira")
    

    def has_bottom_menu(self):
        menuler=bottomMenuModel.objects.filter(topMenu=self).all()
        if menuler.count()>0:
            return True
        else:
            return False



class bottomMenuModel(models.Model):
    topMenu=models.ForeignKey(topMenuModel,on_delete=models.CASCADE,related_name="bottomMenus")  
    name=models.CharField(max_length=100,blank=True,null=True)   
    url=models.CharField(max_length=150,blank=True,null=True)   
    userType=models.CharField(max_length=100,blank=True,null=True)   
    menuType=models.CharField(max_length=100,blank=True,null=True,default="Alt Menü") 
    menuSira=models.SmallIntegerField(default=0)
    meta_title=models.CharField(max_length=65,blank=True,null=True) 
    meta_description=models.CharField(max_length=170,blank=True,null=True)   
    meta_keywords=models.CharField(max_length=100,blank=True,null=True)    


    class Meta:
        db_table="bottomMenuModel"
        verbose_name ="Alt Menü"  
        verbose_name_plural ="Alt Menüler"

    def __str__(self):
        return self.name






class IletisimModel(models.Model):
    name=models.CharField(max_length=100)
    lastName=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    phone_number=models.CharField(max_length=20)
    subject=models.CharField(max_length=100,default="",blank=True,null=True)
    mesaj=models.TextField()
    olusturulma_tarihi=models.DateTimeField(auto_now_add=True)
    okundu_bilgisi = models.CharField(
        default="okunmadı",
        max_length=30,
    )
    class Meta:
        db_table="iletisim"
        verbose_name = "İletişim"
        verbose_name_plural = "İletişim"

    def __str__(self):
        return self.email




class CategoryModel(models.Model):
    name=models.CharField(max_length=200)
    image=models.ImageField(upload_to="categoryImages")
    videoCount=models.PositiveSmallIntegerField(default=0)
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_date=models.DateTimeField(auto_now=True,blank=True,null=True)
   
    class Meta:
        db_table="Kategori"
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

    def __str__(self):
        return self.name

    def countCourseOfCategory(self):
        return CourseModel.objects.filter(category=self).all().count()
    




class CourseModel(models.Model):
    image=models.ImageField(upload_to="courseImages")
    author=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="userCourses",blank=True,null=True)  
    title=models.CharField(max_length=300)
    slug=AutoSlugField(populate_from="title",unique=True,blank=True,null=True)  
    category=models.ForeignKey(CategoryModel,on_delete=models.CASCADE,related_name="courses")  
    description=RichTextUploadingField(blank=False,null=False)
    bottomDescription=RichTextUploadingField(blank=False,null=False)
    videoCount=models.PositiveSmallIntegerField(default=0)
    price=models.PositiveSmallIntegerField(default=0)
    zoomDuration=models.PositiveSmallIntegerField(default=0,blank=True,null=True)
    average_star=models.PositiveSmallIntegerField(blank=True,null=True,default=0)
    none_average_star=models.PositiveSmallIntegerField(blank=True,null=True,default=5)
    meta_title=models.CharField(max_length=65,blank=True,null=True) 
    meta_description=models.CharField(max_length=170,blank=True,null=True)   
    meta_keywords=models.CharField(max_length=100,blank=True,null=True)    
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_date=models.DateTimeField(auto_now=True,blank=True,null=True)

    class Meta:
        db_table="Kurs"
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"

    def __str__(self):
        return self.title

        
    def countOfSession(self):
        return courseSessionModel.objects.filter(course=self).count()

   
    def countOfVideos(self):
        count=0
        courses=courseSessionModel.objects.filter(course=self).all()
        for i in courses:
            count+=i.videos.count()
        return count



    @property
    def getStar(self):
        return range(self.average_star)


    @property
    def getNoneStar(self):
        return range(self.none_average_star)

    
    @property
    def getStarsWithCommentCount(self):
        return CommentModel.objects.filter(is_published=True,parent=None,course=self).count()

    
   
    def getCategoryName(self):
        return self.category.name


    def getTotalVideoDuration(self):
        hour=0
        minute=0
        seconds=0
        sessions=courseSessionModel.objects.filter(course=self).all()
        for i in sessions:
            for video in i.videos.all():
                minute+=video.minute
                seconds+=video.seconds
        add=int(seconds/60)
        minute+=add
        if minute>=60:
            hour=int(minute/60)
            minute=minute%60
        if len(str(hour))==1:
            hour="0"+str(hour)
        if len(str(minute))==1:
            minute="0"+str(minute)
        seconds=seconds%60
        if len(str(seconds))==1:
            seconds="0"+str(seconds)
        return str(hour)+":"+str(minute)+":"+str(seconds)

    
    def save(self, *args, **kwargs):
        self.slug = f'{self.title}'
        super().save(*args, **kwargs)

    
  
    def countOfAllComments(self):
        return CommentModel.objects.filter(is_published=True,course=self).count()



class whatWillYouLearnModel(models.Model):
    course=models.ForeignKey(CourseModel,on_delete=models.CASCADE,related_name="whatWillYouLearns")  
    title=models.CharField(max_length=300)
    description=models.TextField(blank=True,null=True)
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
   
    class Meta:
        db_table="Ogrenecekleriniz"
        verbose_name = "Ogrenecekleriniz"
        verbose_name_plural = "Ogrenecekleriniz"

    def __str__(self):
        return self.title




class courseFeaturesModel(models.Model):
    course=models.ForeignKey(CourseModel,on_delete=models.CASCADE,related_name="features")  
    title=models.CharField(max_length=300)
    
   
    class Meta:
        db_table="Kurs_Ozellikleri"
        verbose_name = "Kurs_Ozellikleri"
        verbose_name_plural = "Kurs_Ozellikleri"

    def __str__(self):
        return self.title


class courseSessionModel(models.Model):
    course=models.ForeignKey(CourseModel,on_delete=models.CASCADE,related_name="sessions")  
    title=models.CharField(max_length=300)
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)


    def getVideos(self):
        return courseSessionVideoModel.objects.filter(courseSession=self).order_by("created_date")
   
    class Meta:
        db_table="Kurs_Bolumleri"
        verbose_name = "Kurs_Bolumleri"
        verbose_name_plural = "Kurs_Bolumleri"

    def __str__(self):
        return self.title




class courseSessionVideoModel(models.Model):
    courseSession=models.ForeignKey(courseSessionModel,on_delete=models.CASCADE,related_name="videos")  
    title=models.CharField(max_length=300)
    url=models.CharField(max_length=300)
    minute=models.PositiveSmallIntegerField(default=0,blank=True,null=True)
    seconds=models.PositiveSmallIntegerField(default=0,blank=True,null=True)
    video_type=models.CharField(max_length=300,default="everybody",blank=True,null=True)
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_date=models.DateTimeField(auto_now=True,blank=True,null=True)
    
   
    class Meta:
        db_table="Kurs_Bolum_Video"
        verbose_name = "Kurs_Bolum_Videosu"
        verbose_name_plural = "Kurs_Bolum_Videolari"

    def __str__(self):
        return self.title


    
    def getMinute(self):
        if len(str(self.minute))<2:
            return "0"+str(self.minute)
        else:
            return str(self.minute)


    def getSeconds(self):
        if len(str(self.seconds))<2:
            return "0"+str(self.seconds)
        else:
            return str(self.seconds)
            




class PageModel(models.Model):
    meta_title=models.CharField(max_length=65,blank=True,null=True) 
    meta_description=models.CharField(max_length=170,blank=True,null=True)   
    meta_keywords=models.CharField(max_length=100,blank=True,null=True)    
    
    class Meta:
        db_table="pageModel"
        verbose_name ="Sayfa Modeli"  
        verbose_name_plural ="Sayfa Modelleri"

    def __str__(self):
        return self.meta_title







class notificationModel(models.Model):
    title=models.CharField(max_length=200,blank=True,null=True)
    message=models.CharField(max_length=400,blank=True,null=True)
    type=models.CharField(max_length=200)
    noti_user=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="allNotificationsUser",blank=True,null=True)  
    object=models.ForeignKey(CourseModel,on_delete=models.CASCADE,related_name="notificationsOfCourse",blank=True,null=True)  
    blogObject=models.ForeignKey("Admin.blogModel",on_delete=models.CASCADE,related_name="notificationsOfBlogs",blank=True,null=True)  
    appointmentObject=models.ForeignKey("Admin.appointmentModel",on_delete=models.CASCADE,related_name="notificationsOfAppo",blank=True,null=True)  
    has_readen=models.CharField(max_length=200,default="no")
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_date=models.DateTimeField(auto_now=True,blank=True,null=True)
   
    class Meta:
        db_table="Bildirim"
        verbose_name = "Bildirim"
        verbose_name_plural = "Bildirimler"

    def __str__(self):
        return self.title







class LogoModel(models.Model):
    name=models.CharField(max_length=500,blank=True,null=True) 
    image=models.ImageField(upload_to="logoImages",default='logo/logo.png')    
    
    class Meta:
        db_table="logoModel"
        verbose_name ="Logo Modeli"  
        verbose_name_plural ="Logo Modelleri"

    def __str__(self):
        return self.name






class aydinlatmaMetniModel(models.Model):
    description=RichTextUploadingField(blank=True,null=True) 
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_date=models.DateTimeField(auto_now=True,blank=True,null=True)
    
    class Meta:
        db_table="aydinlatmaMetniModel"
        verbose_name ="Aydınlatma Metni"  
        verbose_name_plural ="Aydınlatma Metni"

    def __str__(self):
        return self.description




class kvkkMetniModel(models.Model):
    description=RichTextUploadingField(blank=True,null=True) 
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_date=models.DateTimeField(auto_now=True,blank=True,null=True)
    
    class Meta:
        db_table="kvkkMetniModel"
        verbose_name ="KVKK Metni"  
        verbose_name_plural ="KVKK Metni"

    def __str__(self):
        return self.description





class gizlilikMetniModel(models.Model):
    description=RichTextUploadingField(blank=True,null=True) 
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_date=models.DateTimeField(auto_now=True,blank=True,null=True)
    
    class Meta:
        db_table="gizlilikMetniModel"
        verbose_name ="Gizlilik Metni"  
        verbose_name_plural ="Gizlilik Metni"

    def __str__(self):
        return self.description







class blogCategoryModel(models.Model):
    name=models.CharField(max_length=100,blank=False,null=False)
    slug=AutoSlugField(populate_from='name',unique=True)
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_date=models.DateTimeField(auto_now=True,blank=True,null=True)

    class Meta:
        db_table="BlogCategory"
        verbose_name ="Blog Kategori"
        verbose_name_plural ="Blog Kategoriler"

    def __str__(self):
        return self.name

    
    def getBlogCount(self):
        count=0
        for blog in blogModel.objects.all():
            for cat in blog.categories.all():
                if cat.name==self.name:
                    count+=1
        return count






class blogModel(models.Model):
    title=models.CharField(max_length=500,blank=True,null=True) 
    author=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="blogs",blank=True,null=True) 
    slug=AutoSlugField(populate_from="title",unique=True,blank=True,null=True)   
    categories=models.ManyToManyField(blogCategoryModel,related_name="posts")
    image=models.ImageField(upload_to="blogImages")    
    description=RichTextUploadingField(blank=True,null=True) 
    meta_title=models.CharField(max_length=65,blank=True,null=True) 
    meta_description=models.CharField(max_length=170,blank=True,null=True)   
    meta_keywords=models.CharField(max_length=100,blank=True,null=True)    
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_date=models.DateTimeField(auto_now=True,blank=True,null=True)
    
    class Meta:
        db_table="blogModel"
        verbose_name ="Blog"  
        verbose_name_plural ="Bloglar"


    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        self.slug = f'{self.title}'
        super().save(*args, **kwargs)

    
    def getCreatedMonth(self):
        monthIndex=self.created_date.month
        months=["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran","Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
        return months[monthIndex-1]

    
    def totalCommentCount(self):
        return CommentModel.objects.filter(is_published=True,blog=self).all().count()

    
    def get_categories(self):
        return ", ".join([str(p) for p in self.categories.all()])










class socialModel(models.Model):
    facebook=models.CharField(max_length=200,blank=True,null=True)
    twitter=models.CharField(max_length=400,blank=True,null=True)
    pinterest=models.CharField(max_length=200,blank=True,null=True)
    instagram=models.CharField(max_length=200,blank=True,null=True)
    phone_number=models.CharField(max_length=200)
    email=models.EmailField(max_length=200)
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_date=models.DateTimeField(auto_now=True,blank=True,null=True)
   
    class Meta:
        db_table="SosyalMedya"
        verbose_name = "Sosyal Medya"
        verbose_name_plural = "Sosyal Medya"

    def __str__(self):
        return self.email







class mesafeliSatisModel(models.Model):
    description=RichTextUploadingField(blank=True,null=True) 
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_date=models.DateTimeField(auto_now=True,blank=True,null=True)
    
    class Meta:
        db_table="mesafeliSatisModel"
        verbose_name ="Mesafelili Satis"  
        verbose_name_plural ="Mesafelili Satis"

    def __str__(self):
        return self.description








class randevuSatisModel(models.Model):
    description=RichTextUploadingField(blank=True,null=True) 
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_date=models.DateTimeField(auto_now=True,blank=True,null=True)
    
    class Meta:
        db_table="randevuSatisModel"
        verbose_name ="Randevu Satis Bilgisi"  
        verbose_name_plural ="Randevu Satis Bilgileri"

    def __str__(self):
        return self.description








class footerMailModel(models.Model):
    email=models.EmailField(max_length=200)
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_date=models.DateTimeField(auto_now=True,blank=True,null=True)
   
    class Meta:
        db_table="fotoerMail"
        verbose_name = "Footer Mail"
        verbose_name_plural = "Footer Mailler"

    def __str__(self):
        return self.email







class appointmentModel(models.Model):
    top=models.ForeignKey("Admin.appointmentAdminModel",on_delete=models.CASCADE,related_name="bottomsAppo",blank=True,null=True) 
    category=models.ForeignKey("Admin.appointmentCategoryModel",on_delete=models.CASCADE,related_name="modelssOfCategory",blank=True,null=True) 
    fullname=models.CharField(max_length=250)
    phone_number=models.CharField(max_length=250)
    email=models.EmailField(max_length=250)
    address=models.CharField(max_length=250)
    date=models.DateField(max_length=250,blank=True,null=True)
    status=models.CharField(max_length=200,blank=True,null=True,default="no")
    merchant_oid=models.CharField(max_length=250,blank=True,null=True,default="asd")
    starting_time=models.TimeField(max_length=250,blank=True,null=True)
    finishing_time=models.TimeField(max_length=250,blank=True,null=True)
    message=models.TextField(blank=True,null=True)
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
   
    class Meta:
        db_table="appointment"
        verbose_name = "Randevu"
        verbose_name_plural = "Randevular"


    















class hakkimizdaModel(models.Model):
    image=models.ImageField(upload_to="hakkimizdaImages",blank=True,null=True)
    description=RichTextUploadingField(blank=True,null=True) 
    description2=RichTextUploadingField(blank=True,null=True) 
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_date=models.DateTimeField(auto_now=True,blank=True,null=True)
    
    class Meta:
        db_table="hakkimzida"
        verbose_name ="Hakkımızda"  
        verbose_name_plural ="Hakkımızda"

    def __str__(self):
        return self.description







class appointmentAdminModel(models.Model):
    whois=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="relatedAppointmentAdminModels",blank=True,null=True)  
    date=models.DateField(max_length=250,blank=True,null=True)
    starting_time=models.TimeField(max_length=250,blank=True,null=True)
    finishing_time=models.TimeField(max_length=250,blank=True,null=True)
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
   
    class Meta:
        db_table="appointmentAdmin"
        verbose_name = "RandevuAdmin"
        verbose_name_plural = "RandevularAdmin" 

    def __str__(self):
        return str(self.date)






class appointmentCategoryModel(models.Model):
    whois=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="relatedAppointmentCategoryModels",blank=True,null=True)  
    name=models.CharField(max_length=500,blank=True,null=True) 
    price=models.SmallIntegerField(default=0,blank=True,null=True)
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_date=models.DateTimeField(auto_now=True,blank=True,null=True) 
    
    class Meta:
        db_table="appointmentCategoryModel"
        verbose_name ="Randevu Kategori"  
        verbose_name_plural ="Randevu Kategori"

    def __str__(self):
        return str(self.name)+" ("+str(self.price)+" ₺)"
