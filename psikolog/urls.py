from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    index,login,logoutIndex,registerUser,changePassword,profileSettings,coursesGridList,favouritesCoursesGridList,
    AddFavouritesCoursesGridList,courseDetail,learningContentList,aboutUs,contact
)

urlpatterns = [
    path('',index,name="index"),
    path('giris',login,name="login"),
    path('cikis',logoutIndex,name="logoutIndex"),
    path('kullanici-kayit',registerUser,name="registerUser"),
    path('kullanici-sifre-degistir',changePassword,name="changePassword"),
    path('sifremi-unuttum/',auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"),name='password_reset'),
    path('sifremi-unuttum/bitti/',auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),name='password_reset_done'),
    path('sifremi-sifirla/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"),name='password_reset_confirm'),
    path('sifremi-sifirla/bitti/',auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),name='password_reset_complete'),
    path('kullanici-profil-guncelle',profileSettings,name="profileSettings"),
    path('tum-kurslar',coursesGridList,name="coursesGridList"),
    path('favori-kurslar',favouritesCoursesGridList,name="favouritesCoursesGridList"),
    path('favori-kurs-ekle/<int:pk>',AddFavouritesCoursesGridList,name="AddFavouritesCoursesGridList"),
    path('kurs-detay/<slug:slug>',courseDetail,name="courseDetail"),
    path('ogrenim-icerigim',learningContentList,name="learningContentList"),
    path('hakkimizda',aboutUs,name="aboutUs"),
    path('iletisim',contact,name="contact"),

]