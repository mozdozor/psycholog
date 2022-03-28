from unicodedata import category
from urllib import request
from autoslug import AutoSlugField
from django.db import models

from psikolog.models import CommentModel, CustomUserModel, favouriteCourseModel

# Create your models here.




class topMenuModel(models.Model):
    name=models.CharField(max_length=100,blank=True,null=True)   
    url=models.CharField(max_length=150,blank=True,null=True)   
    userType=models.CharField(max_length=100,blank=True,null=True)   
    menuType=models.CharField(max_length=100,blank=True,null=True,default="Üst Menü")   
    menuSira=models.SmallIntegerField(default=0)


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
    subject=models.CharField(max_length=100)
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
    description=models.TextField()
    bottomDescription=models.TextField()
    videoCount=models.PositiveSmallIntegerField(default=0)
    price=models.PositiveSmallIntegerField(default=0)
    average_star=models.PositiveSmallIntegerField(blank=True,null=True,default=0)
    none_average_star=models.PositiveSmallIntegerField(blank=True,null=True,default=5)
    meta_title=models.CharField(max_length=500,blank=True,null=True) 
    meta_description=models.CharField(max_length=500,blank=True,null=True)   
    meta_keywords=models.CharField(max_length=500,blank=True,null=True)    
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



class whatWillYouLearnModel(models.Model):
    course=models.ForeignKey(CourseModel,on_delete=models.CASCADE,related_name="whatWillYouLearns")  
    title=models.CharField(max_length=300)
    description=models.TextField()
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
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_date=models.DateTimeField(auto_now=True,blank=True,null=True)
    
   
    class Meta:
        db_table="Kurs_Bolum_Video"
        verbose_name = "Kurs_Bolum_Videosu"
        verbose_name_plural = "Kurs_Bolum_Videolari"

    def __str__(self):
        return self.title




class PageModel(models.Model):
    meta_title=models.CharField(max_length=500,blank=True,null=True) 
    meta_description=models.CharField(max_length=500,blank=True,null=True)   
    meta_keywords=models.CharField(max_length=500,blank=True,null=True)    
    view_name=models.CharField(max_length=100,blank=True,null=True)    
    
    class Meta:
        db_table="pageModel"
        verbose_name ="Sayfa Modeli"  
        verbose_name_plural ="Sayfa Modelleri"

    def __str__(self):
        return self.meta_title







class notificationModel(models.Model):
    title=models.CharField(max_length=200)
    message=models.CharField(max_length=400,blank=True,null=True)
    type=models.CharField(max_length=200)
    noti_user=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="allNotifications")  
    object=models.ForeignKey(CourseModel,on_delete=models.CASCADE,related_name="notificationsOfCourse")  
    has_readen=models.CharField(max_length=200,default="no")
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_date=models.DateTimeField(auto_now=True,blank=True,null=True)
   
    class Meta:
        db_table="Bildirim"
        verbose_name = "Bildirim"
        verbose_name_plural = "Bildirimler"

    def __str__(self):
        return self.title
