from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms
from django.forms.widgets import DateInput, DateTimeInput, EmailInput, FileInput, TextInput, Textarea,PasswordInput, Select
from psikolog.models import CommentModel, CustomUserModel, sliderModel






class sliderModelForm(forms.ModelForm):
    class Meta:
        model = sliderModel
        exclude=("created_date","updated_date")
        widgets = {
            "top_title" : TextInput(attrs={"class":"form-control","type":"text","name":"top_title","required":"required"}),
            "bottom_title" : TextInput(attrs={"class":"form-control","name":"bottom_title","required":"required"}),
            "sira" : forms.NumberInput(attrs={"class":"form-control","name":"sira","required":"required"}),
        }
        labels = {      
            "image":"Foto (1600x750)",
            'top_title': "Üst Başlık",
            'bottom_title': "Alt Başlık",
            'sira': "Sıra",
        }






class registerUserForm(UserCreationForm):
    class Meta:
        model = CustomUserModel
        fields=("first_name","last_name","email","phone_number","password1","password2")
        widgets = {
            "first_name" : TextInput(attrs={"class":"input_field","type":"text","name":"first_name","required":"required"}),
            "last_name" : TextInput(attrs={"class":"input_field","name":"last_name","required":"required"}),
            "email" : EmailInput(attrs={"class":"input_field","name":"email","required":"required"}),
            "phone_number" : TextInput(attrs={"class":"input_field","name":"phone_number","required":"required"}),
            "password1" : PasswordInput(attrs={"class":"input_field","type":"password","name":"password1","required":"required"}),
            "password2" : PasswordInput(attrs={"class":"input_field","type":"password","name":"password2","required":"required"})
            
        }
        labels = {      
            'first_name': "İsim",
            'last_name': "Soyisim",
            'email': "Email",
            'phone_number': "Telefon",
            'password1': "Şifre",
            'password2': "Şifre Tekrar"
        }







class userSettingsProfileModelForm(forms.ModelForm):
    class Meta:
        model = CustomUserModel
        fields=("first_name","last_name","phone_number","email","address","image")
        widgets = {
            "first_name" : TextInput(attrs={"class":"input_field","type":"text","name":"first_name","required":"required"}),
            "last_name" : TextInput(attrs={"class":"input_field","type":"text","name":"last_name","required":"required"}),
            "phone_number" : TextInput(attrs={"class":"input_field","type":"text","name":"phone_number","required":"required"}),
            "email" : TextInput(attrs={"class":"input_field","type":"email","name":"email","required":"required"}),
            "address" : TextInput(attrs={"class":"input_field","type":"text","name":"address","required":"required"}),
        }
        labels = {      
            'first_name': "İsim",
            'last_name': "Soyisim",
            'phone_number': "Telefon",
            'email': "Email",
            'address': "Adres",
            'image': "Profil Fotoğrafı",
        }








class CommentModelStarsForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields=("comment","star")
        widgets = {           
            "comment" : Textarea(attrs={"class":"form-control","cols":"40","rows":"3"}),          
        }



