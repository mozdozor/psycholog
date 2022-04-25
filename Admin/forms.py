from dataclasses import fields
from django import forms
from django.forms.widgets import DateInput, DateTimeInput, EmailInput, FileInput, TextInput, Textarea,SelectMultiple
import datetime
from psikolog.models import CommentModel, CustomUserModel
from .models import CategoryModel, CourseModel, IletisimModel, LogoModel, PageModel, appointmentAdminModel, appointmentCategoryModel, appointmentModel, aydinlatmaMetniModel, blogCategoryModel, blogModel, courseSessionModel, courseSessionVideoModel, footerMailModel, gizlilikMetniModel, hakkimizdaModel, kvkkMetniModel, mesafeliSatisModel, socialModel, whatWillYouLearnModel

from string import Template
from django.utils.safestring import mark_safe
from django.forms import ImageField, TimeInput



class categoryModelForm(forms.ModelForm):
    class Meta:
        model = CategoryModel
        fields=("name","image")
        widgets = {
            "name" : TextInput(attrs={"class":"form-control","type":"text","name":"name","required":"required"}),
        }
        labels = {      
            'name': "Kategori İsmi",
            'image': "Fotoğraf (800x533)",
        }








class CourseModelForm(forms.ModelForm):
    class Meta:
        model = CourseModel
        exclude=("videoCount","created_date","updated_date","average_star","none_average_star","author")
        widgets = {
            "title" : TextInput(attrs={"class":"form-control","type":"text","name":"title","required":"required"}),
            "category" : forms.Select(attrs={"class":"form-control select","name":"categoryName","required":"required"}),
            "description" : Textarea(attrs={"class":"form-control","name":"description","required":"required"}),
            "bottomDescription" : Textarea(attrs={"class":"form-control","name":"bottomDescription","required":"required"}),
            "zoomDuration" : forms.NumberInput(attrs={"class":"form-control","name":"zoomDuration","required":"required"}),
            "price" : forms.NumberInput(attrs={"class":"form-control","name":"price","required":"required"}),
            "meta_title" : TextInput(attrs={"class":"form-control","type":"text","name":"meta_title","maxlength":"65"}),
            "meta_description" : TextInput(attrs={"class":"form-control","type":"text","name":"meta_description","maxlength":"170"}),
            "meta_keywords" : TextInput(attrs={"class":"form-control","type":"text","name":"meta_keywords","data-max-words":"5"}),
        }
        labels = {      
            'image':"Kurs Fotoğrafı (800x533)",
            'title': "Kurs Başlığı",
            'description': "Açıklama Yazısı",
            'bottomDescription': "Alt Açıklama",
            'zoomDuration': "Zoom Eğitim Süresi (Saat)",
            'price': "Fiyat",
            'category': "Kategori",
            'meta_title': "Meta Başlık",
            'meta_description': "Meta Açıklama",
            'meta_keywords': "Meta Anahtar Kelimeler",
        }
    
  
class whatWillYouLearnModelForm(forms.ModelForm):
    class Meta:
        model = whatWillYouLearnModel
        exclude=("course",)
        widgets = {
            "title" : TextInput(attrs={"class":"form-control","type":"text","name":"title","required":"required"}),
            "description" : Textarea(attrs={"class":"form-control","name":"description"}),
        }
        labels = {      
            'title': "Başlık",
            'description': "Açıklama",
        }



class courseSessionModelForm(forms.ModelForm):
    class Meta:
        model = courseSessionModel
        exclude=("course",)
        widgets = {
            "title" : TextInput(attrs={"class":"form-control","type":"text","name":"title","required":"required"}),
        }
        labels = {      
            'title': "Bölüm Adı",
        }




class courseSessionVideoModelForm(forms.ModelForm):
    CHOICES= (
        ('satinAlanlar','Sadece satın alanlar izlesin'),
        ('herkes','Herkes'),
        
    )
    video_type=forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control select","name":"video_type","required":"required"}), choices=CHOICES,label="Videoyu kim izlesin")
    class Meta:
        model = courseSessionVideoModel
        fields=("title","url","video_type","minute","seconds")
        widgets = {
            "title" : TextInput(attrs={"class":"form-control","type":"text","name":"title","required":"required"}),
            "url" : TextInput(attrs={"class":"form-control","type":"text","name":"url","required":"required"}),
            "minute" : forms.NumberInput(attrs={"class":"form-control","name":"minute","required":"required"}),
            "seconds" : forms.NumberInput(attrs={"class":"form-control","name":"seconds","required":"required"}),
            
        }
        labels = {      
            'title': "Video Başlığı",
            'url': "URL Adresi (Videoların otomatik oynamasını istiyorsanız url adresinin sonuna '&autoplay=1&muted=1' komutunu tırnak işaretleri olmadan yazınız.)",
            'video_type': "Video Tipi",
            'minute': "Dakika",
            'seconds': "Saniye",
        }



class adminSettingsProfileModelForm(forms.ModelForm):
    class Meta:
        model = CustomUserModel
        fields=("first_name","last_name","phone_number","email","username","address","about","image")
        widgets = {
            "first_name" : TextInput(attrs={"class":"form-control","type":"text","name":"first_name","required":"required"}),
            "last_name" : TextInput(attrs={"class":"form-control","type":"text","name":"last_name","required":"required"}),
            "phone_number" : TextInput(attrs={"class":"form-control","type":"text","name":"phone_number","required":"required"}),
            "email" : TextInput(attrs={"class":"form-control","type":"email","name":"email","required":"required"}),
            "username" : TextInput(attrs={"class":"form-control","type":"text","name":"username","required":"required"}),
            "address" : TextInput(attrs={"class":"form-control","type":"text","name":"address","required":"required"}),
            "about" : Textarea(attrs={"class":"form-control","name":"about","required":"required"}),
        }
        labels = {      
            'first_name': "İsim",
            'last_name': "Soyisim",
            'phone_number': "Telefon",
            'email': "Email",
            'username': "Kullanıcı Adı",
            'address': "Adres",
            'about': "Hakkımda",
            'image': "Profil Fotoğrafı",
        }





class PageModelForm(forms.ModelForm):
    class Meta:
        model = PageModel
        fields=("__all__")
        widgets = {
            "meta_title" : TextInput(attrs={"class":"form-control","type":"text","name":"meta_title"}),
            "meta_description" : Textarea(attrs={"class":"form-control","type":"text","name":"meta_description","rows":"5","cols":"5"}),
            "meta_keywords" : TextInput(attrs={"class":"form-control","type":"text","name":"meta_keywords"}),
            "view_name" : TextInput(attrs={"class":"form-control","type":"text","name":"view_name"}),           
        }



class CommentModelForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields=("comment",)
        widgets = {           
            "comment" : Textarea(attrs={"class":"form-control","cols":"40","rows":"3"}),          
        }




class logoModelForm(forms.ModelForm):
    class Meta:
        model = LogoModel
        fields=("__all__")
        widgets = {           
            "name" : TextInput(attrs={"class":"form-control","type":"text","name":"name"}), 
        }
        labels = {      
            'name': "Logo Adı",
            'image': "Logo Fotoğrafı",
        }







class aydinlatmaMetniModelForm(forms.ModelForm):
    class Meta:
        model = aydinlatmaMetniModel
        fields=("description",)
        widgets = {           
            "description" : Textarea(attrs={"class":"form-control","name":"description","required":"required"}),    
        }
        labels = {      
            'description': "Metin",
            
        }




class kvkkMetniModelForm(forms.ModelForm):
    class Meta:
        model = kvkkMetniModel
        fields=("description",)
        widgets = {           
            "description" : Textarea(attrs={"class":"form-control","name":"description","required":"required"}),    
        }
        labels = {      
            'description': "Metin",
            
        }



class gizlilikMetniModelForm(forms.ModelForm):
    class Meta:
        model = gizlilikMetniModel
        fields=("description",)
        widgets = {           
            "description" : Textarea(attrs={"class":"form-control","name":"description","required":"required"}),    
        }
        labels = {      
            'description': "Metin",
            
        }







    



class blogModelForm(forms.ModelForm):
    class Meta:
        model = blogModel
        exclude=("created_date","updated_date","author","slug")
        widgets = {           
            "title" : TextInput(attrs={"class":"form-control","type":"text","name":"title"}), 
            "description" : Textarea(attrs={"class":"form-control","name":"description","required":"required"}),   
            "categories" : SelectMultiple(attrs={"class":"form-control"}), 
            "meta_title" : TextInput(attrs={"class":"form-control","type":"text","name":"meta_title","maxlength":"65"}), 
            "meta_description" : TextInput(attrs={"class":"form-control","type":"text","name":"meta_description","maxlength":"170"}), 
            "meta_keywords" : TextInput(attrs={"class":"form-control","type":"text","name":"meta_keywords","data-max-words":"5"}), 
        }
        labels = {      
            'title': "Başlık",
            'description': "Blog Metni",
            'image': "Fotoğraf (800x400)",
            'categories': "Kategoriler (Birden fazla kategori seçimi için CTRL tuşunu kullanabilirsiniz)",
            'meta_title': "Meta Başlık",
            'meta_description': "Meta Açıklama",
            'meta_keywords': "Meta Anahtar Kelimeler",
            
            
        }







class blogCategoryModelForm(forms.ModelForm):
    class Meta:
        model = blogCategoryModel
        fields=("name",)
        widgets = {
            "name" : TextInput(attrs={"class":"form-control","type":"text","name":"name","required":"required"}),
        }
        labels = {      
            'name': "Kategori İsmi",
        }







class socialModelForm(forms.ModelForm):
    class Meta:
        model = socialModel
        exclude=("created_date","updated_date")
        widgets = {
            "facebook" : TextInput(attrs={"class":"form-control","type":"text","name":"facebook"}),
            "twitter" : TextInput(attrs={"class":"form-control","type":"text","name":"twitter"}),
            "pinterest" : TextInput(attrs={"class":"form-control","type":"text","name":"pinterest"}),
            "instagram" : TextInput(attrs={"class":"form-control","type":"text","name":"instagram"}),
            "phone_number" : TextInput(attrs={"class":"form-control","type":"text","name":"phone_number","required":"required"}),
            "email" : EmailInput(attrs={"class":"form-control","name":"email","required":"required"}),
        }
        labels = {      
            'facebook': "Facebook Adresiniz",
            'twitter': "Twitter Adresiniz",
            'pinterest': "Pinterest Adresiniz",
            'instagram': "Instagram Adresiniz",
            'phone_number': "Tellefon",
            'email': "Email Adresiniz",
        }





class IletisimModelForm(forms.ModelForm):
    class Meta:
        model = IletisimModel
        fields=("name","lastName","email","phone_number","mesaj")
        widgets = {
            "name" : TextInput(attrs={"class":"input_field","type":"text","name":"name","required":"required"}),
            "lastName" : TextInput(attrs={"class":"input_field","type":"text","name":"lastName","required":"required"}),
            "phone_number" : TextInput(attrs={"class":"input_field","type":"text","name":"phone_number","required":"required"}),
            "email" : TextInput(attrs={"class":"input_field","type":"email","name":"email","required":"required"}),
            "mesaj" : Textarea(attrs={"class":"input_field","type":"text","name":"mesaj","required":"required"}),
            
        }
        labels = {      
            'name': "İsim",
            'lastName': "Soyisim",
            'phone_number': "Telefon",
            'email': "Email",
            'mesaj': "Mesaj",
            
        }






class mesafeliSatisModelForm(forms.ModelForm):
    class Meta:
        model = mesafeliSatisModel
        fields=("description",)
        widgets = {           
            "description" : Textarea(attrs={"class":"form-control","name":"description","required":"required"}),    
        }
        labels = {      
            'description': "Metin",
            
        }








class footerMailModelForm(forms.ModelForm):
    class Meta:
        model = footerMailModel
        fields=("email",)
        widgets = {
            "email" : TextInput(attrs={"class":"input_field","type":"email","name":"email","required":"required"}),
        }
        labels = {      
            'email': "Email",
        }







class appointmentModelForm(forms.ModelForm):
    class Meta:
        model = appointmentModel
        exclude=("created_date","status","starting_time","finishing_time","date","top","merchant_oid")
        widgets = {
            "category" : forms.Select(attrs={"class":"input_field","name":"category","required":"required"}),
            "fullname" : TextInput(attrs={"class":"input_field","type":"text","name":"fullname","required":"required"}),
            "phone_number" : TextInput(attrs={"class":"input_field","type":"text","name":"phone_number","required":"required"}),
            "email" : TextInput(attrs={"class":"input_field","type":"email","name":"email","required":"required"}),
            "address" : TextInput(attrs={"class":"input_field","type":"text","name":"address","required":"required"}),
            "date" : DateInput(attrs={"class":"input_field","name":"date","type":"date","required":"required"}),
            "starting_time" : TimeInput(attrs={"class":"input_field","type":"time","name":"starting_time","required":"required"}),
            "finishing_time" : TimeInput(attrs={"class":"input_field","type":"time","name":"finishing_time","required":"required"}),
            "message" : Textarea(attrs={"class":"input_field","type":"text","name":"message","rows":"5"}),
            
        }
        labels = {     
            'category': "Kategori Seçiniz * ", 
            'fullname': "İsim Soyisim * ",
            'phone_number': "Telefon * ",
            'email': "Email * ",
            'address': "Adres * ",
            'date': "Tarih * ",
            'starting_time': "Başlangıç Saati",
            'finishing_time': "Bitiş Saati",
            'message': "İletmek istediğiniz özel bir mesajınız varsa yazınız",
            
        }








class hakkimizdaModelForm(forms.ModelForm):
    class Meta:
        model = hakkimizdaModel
        fields=("image","description","description2",)
        widgets = {           
            "description" : Textarea(attrs={"class":"form-control","name":"description","required":"required"}),    
            "description2" : Textarea(attrs={"class":"form-control","name":"description2","required":"required"}),    
        }
        labels = {     
            'image': "Fotoğraf (800x533)", 
            'description': "Ana sayfa metni",
            'description2': "Hakkımızda sayfası metni",
            
        }








class appointmentAdminModelForm(forms.ModelForm):
    CHOICES= (
        ('09:00','09:00'),
        ('10:00','10:00'),
        ('11:00','11:00'),
        ('12:00','12:00'),
        ('13:00','13:00'),
        ('14:00','14:00'),
        ('15:00','15:00'),
        ('16:00','16:00'),
        ('17:00','17:00'),
        ('18:00','18:00'),
        
    )
    starting_time=forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control select","name":"starting_time","required":"required"}), choices=CHOICES,label="Başlangıç Saati")
    finishing_time=forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control select","name":"finishing_time","required":"required"}), choices=CHOICES,label="Bitiş Saati")
    class Meta:
        model = appointmentAdminModel
        exclude=("created_date",)
        widgets = {
            "date" : DateInput(attrs={"class":"form-control","name":"date","type":"date","required":"required"}),
            
        }
        labels = {      
            'date': "Tarih",
        }
    
   







class appointmentCategoryModelForm(forms.ModelForm):
    class Meta:
        model = appointmentCategoryModel
        fields=("name","price")
        widgets = {
            "name" : TextInput(attrs={"class":"form-control","type":"text","name":"name","required":"required"}),
            "price" : forms.NumberInput(attrs={"class":"form-control","name":"price","required":"required"}),
        }
        labels = {      
            'name': "Randevu Kategori İsmi",
            "price":"Seans Ücreti"
        }
