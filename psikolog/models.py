from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser









# Create your models here.

    # def calculateAge(request,self):
    #     return now().year - ExtractYear(self.date_of_birth)



    
class CustomUserModel(AbstractUser):
    slug=AutoSlugField(populate_from="get_full_name",unique=True)  #düzgün çalaışıyormu kontrol et
    date_of_birth=models.DateField(blank=True,null=True)
    email=models.EmailField(max_length=250,blank=False,null=False,unique=True)
    phone_number=models.CharField(max_length=250,blank=False,null=False)
    image=models.ImageField(
        upload_to="profile_images",default='avatar/no-avatar.png'
    )
    about=models.TextField(blank=True,null=True,default="")
    city=models.CharField(max_length=50,blank=True,null=True,default="")              # il adı döndürür 
    state=models.CharField(max_length=100,blank=True,null=True,default="") 
    country=models.CharField(max_length=50,blank=True,null=True,default="Türkiye")                   #ilçe
    address=models.CharField(max_length=450,blank=True,null=True,default="")
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    


    class Meta:
        db_table="customUser"
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'

    def __str__(self):
        return self.get_full_name()






class CommentModel(models.Model):
    course=models.ForeignKey("Admin.CourseModel",on_delete=models.CASCADE,related_name="all_comments",blank=True,null=True) 
    blog=models.ForeignKey("Admin.blogModel",on_delete=models.CASCADE,related_name="blog_comments",blank=True,null=True) 
    comment_user= models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="his_comments")
    is_recommend=models.BooleanField(default=False)
    star=models.PositiveSmallIntegerField(blank=True,null=True,default=0)
    none_star=models.PositiveSmallIntegerField(blank=True,null=True,default=5)
    comment=models.TextField(blank=True,null=True,default="")
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies',on_delete=models.CASCADE)
    is_published=models.BooleanField(default=False)

  
    def children(self):
        return CommentModel.objects.filter(parent=self,is_published=True).order_by("created_date").all()
    

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    
    @property
    def getStar(self):
        return range(self.star)

    @property
    def getNoneStar(self):
        return range(self.none_star)


    

    class Meta:
        ordering = ('-created_date',)
        db_table="comment"
        verbose_name ="Yorum"  
        verbose_name_plural ="Yorumlar"

    def __str__(self):
        return self.comment_user.email







class billingCourseModel(models.Model):
    image=models.ImageField(upload_to="billingCourseImage")
    author=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="userBillingCourses",blank=True,null=True)  
    payment_user=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="paymentAllCourse")  
    title=models.CharField(max_length=300)
    slug=AutoSlugField(populate_from="title",unique=True,blank=True,null=True)  
    course=models.ForeignKey("Admin.CourseModel",on_delete=models.CASCADE,related_name="billingCourses",blank=True,null=True)  
    description=models.TextField()
    bottomDescription=models.TextField()
    videoCount=models.PositiveSmallIntegerField(default=0)
    average_star=models.PositiveSmallIntegerField(blank=True,null=True,default=0)
    none_average_star=models.PositiveSmallIntegerField(blank=True,null=True,default=5)
    price=models.PositiveSmallIntegerField(default=0)
    meta_title=models.CharField(max_length=500,blank=True,null=True) 
    meta_description=models.CharField(max_length=500,blank=True,null=True)   
    meta_keywords=models.CharField(max_length=500,blank=True,null=True) 
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_date=models.DateTimeField(auto_now=True,blank=True,null=True)

    class Meta:
        db_table="Fatura"
        verbose_name = "Fatura"
        verbose_name_plural = "Faturalar"

    def __str__(self):
        return self.title





class sliderModel(models.Model):
    image=models.ImageField(upload_to="sliderImages")
    top_title=models.CharField(max_length=300)
    bottom_title=models.CharField(max_length=300)
    url=models.CharField(max_length=300,blank=True,null=True)
    sira=models.PositiveSmallIntegerField(default=0,blank=True,null=True)
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_date=models.DateTimeField(auto_now=True,blank=True,null=True)

    class Meta:
        db_table="Slider"
        verbose_name = "Slider"
        verbose_name_plural = "Sliderlar"

    def __str__(self):
        return self.top_title





class favouriteCourseModel(models.Model):
    course=models.ForeignKey("Admin.CourseModel",on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="favouriteCourses")


    class Meta:
        db_table="Favori_Kurslar"
        verbose_name = "Favori Kurs"
        verbose_name_plural = "Favori Kurslar"

    def __str__(self):
        return self.course.title









class orderModel(models.Model):
    course=models.ForeignKey("Admin.CourseModel",on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="orderCourses")
    price=models.PositiveSmallIntegerField(default=0,blank=True,null=True)
    status=models.CharField(max_length=10)
    merchant_oid=models.CharField(max_length=250)
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_date=models.DateTimeField(auto_now=True,blank=True,null=True)

    class Meta:
        db_table="siparis"
        verbose_name = "Siparis"
        verbose_name_plural = "Siparisler"

    def __str__(self):
        return self.course.title








class hasWatchedModel(models.Model):
    video=models.ForeignKey("Admin.courseSessionVideoModel",on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="watchedVideos")
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_date=models.DateTimeField(auto_now=True,blank=True,null=True)

    class Meta:
        db_table="watchedVideos"
        verbose_name = "İzlenen Video"
        verbose_name_plural = "İzlenen Videolar"

    def __str__(self):
        return self.video.title










class mediaGalleryImageModel(models.Model):
    image=models.ImageField(upload_to="mediaGalleryImages")
    image2=models.ImageField(upload_to="mediaGalleryImages",blank=True,null=True)
    title=models.CharField(max_length=300)
    sira=models.PositiveSmallIntegerField(default=0,blank=True,null=True)
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_date=models.DateTimeField(auto_now=True,blank=True,null=True)

    class Meta:
        db_table="MediaGalleryImages"
        verbose_name = "MediaGalleryImage"
        verbose_name_plural = "MediaGalleryImages"

    def __str__(self):
        return self.title





class mediaGalleryVideoModel(models.Model):
    url=models.CharField(max_length=300)
    image=models.ImageField(upload_to="mediaGalleryVideoImages")
    title=models.CharField(max_length=300)
    sira=models.PositiveSmallIntegerField(default=0,blank=True,null=True)
    created_date=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_date=models.DateTimeField(auto_now=True,blank=True,null=True)

    class Meta:
        db_table="MediaGalleryVideos"
        verbose_name = "MediaGalleryVideo"
        verbose_name_plural = "MediaGalleryVideos"

    def __str__(self):
        return self.url
