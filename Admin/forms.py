from dataclasses import fields
from django import forms
from django.forms.widgets import DateInput, DateTimeInput, EmailInput, FileInput, TextInput, Textarea

from psikolog.models import CommentModel, CustomUserModel
from .models import CategoryModel, CourseModel, PageModel, courseSessionModel, courseSessionVideoModel, whatWillYouLearnModel







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
        exclude=("videoCount","created_date","updated_date","average_star","none_average_star")
        widgets = {
            "title" : TextInput(attrs={"class":"form-control","type":"text","name":"title","required":"required"}),
            "author" : forms.Select(attrs={"class":"form-control select","name":"author","required":"required"}),
            "category" : forms.Select(attrs={"class":"form-control select","name":"categoryName","required":"required"}),
            "description" : Textarea(attrs={"class":"form-control","name":"description","required":"required"}),
            "bottomDescription" : Textarea(attrs={"class":"form-control","name":"bottomDescription","required":"required"}),
            "price" : forms.NumberInput(attrs={"class":"form-control","name":"price","required":"required"}),
            "meta_title" : TextInput(attrs={"class":"form-control","type":"text","name":"meta_title"}),
            "meta_description" : TextInput(attrs={"class":"form-control","type":"text","name":"meta_description"}),
            "meta_keywords" : TextInput(attrs={"class":"form-control","type":"text","name":"meta_keywords"}),
        }
        labels = {      
            'author':"Yazar",
            'image':"Kurs Fotoğrafı",
            'title': "Kurs Başlığı",
            'description': "Açıklama Yazısı",
            'bottomDescription': "Alt Açıklama",
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
            "description" : Textarea(attrs={"class":"form-control","name":"description","required":"required"}),
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
    class Meta:
        model = courseSessionVideoModel
        fields=("title","url",)
        widgets = {
            "title" : TextInput(attrs={"class":"form-control","type":"text","name":"title","required":"required"}),
            "url" : TextInput(attrs={"class":"form-control","type":"text","name":"url","required":"required"}),
        }
        labels = {      
            'title': "Video Başlığı",
            'url': "URL Adresi",
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