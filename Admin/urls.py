from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    indexAdmin,loginAdmin,logoutAdmin,showAllMessages,listMenu,addMenu,deleteMenu,categoryListAdmin,addCategoryAdmin,
    deleteCategoryAdmin,courseListAdmin,courseAddAdmin,courseDetailAdmin,deleteCourseAdmin,wwylListAdmin,
    wwylAddAdmin,deleteWwylAdmin,sessionListAdmin,sessionAddAdmin,deleteSessionAdmin,sessionVideoListAdmin,
    sessionVideoAddAdmin,deleteSessionVideoAdmin,profileSettingsAdmin,changePasswordAdmin,commentsAdmin,
    commentsRequestAdmin,acceptCommentsRequestAdmin,deleteComingRequestAdmin,showPagesAdmin,createPageModelAdmin,
    deletePageModelAdmin,userListAdmin,addReplyCommentAdmin,listNotificationsAdmin,deleteNotificationsAdmin,
    listBillingsAdmin,listSlidersAdmin,createSliderModelAdmin,deleteSliderAdmin
    
)

urlpatterns = [
    path('',indexAdmin,name="indexAdmin"),
    path('admin-giris',loginAdmin,name="loginAdmin"),
    path('admin-cikis',logoutAdmin,name="logoutAdmin"),
    path('admin-tum-mesajlar',showAllMessages,name="showAllMessages"),
    path('admin-menu-listele',listMenu,name="listMenu"),
    path('admin-menu-ekle',addMenu,name="addMenu"),
    path('admin-menu-sil/<int:pk>/<str:str>',deleteMenu,name="deleteMenu"),
    path('admin-kategori-listele',categoryListAdmin,name="categoryListAdmin"),
    path('admin-kategori-ekle',addCategoryAdmin,name="addCategoryAdmin"),
    path('admin-kategori-sil/<int:pk>',deleteCategoryAdmin,name="deleteCategoryAdmin"),
    path('admin-kurs-listele',courseListAdmin,name="courseListAdmin"),
    path('admin-kurs-ekle',courseAddAdmin,name="courseAddAdmin"),
    path('admin-kurs-detay/<int:pk>',courseDetailAdmin,name="courseDetailAdmin"),
    path('admin-kurs-sil/<int:pk>',deleteCourseAdmin,name="deleteCourseAdmin"),
    path('admin-ogrenecekleriniz-listele',wwylListAdmin,name="wwylListAdmin"),
    path('admin-ogrenecekleriniz-ekle',wwylAddAdmin,name="wwylAddAdmin"),
    path('admin-ogrenecekleriniz-sil/<int:pk>',deleteWwylAdmin,name="deleteWwylAdmin"),
    path('admin-kurs-bolum-listele/<int:pk>',sessionListAdmin,name="sessionListAdmin"),
    path('admin-kurs-bolum-ekle/<int:pk>',sessionAddAdmin,name="sessionAddAdmin"),
    path('admin-kurs-bolum-sil/<int:pk>',deleteSessionAdmin,name="deleteSessionAdmin"),
    path('admin-kurs-bolum-video-listele/<int:pk>',sessionVideoListAdmin,name="sessionVideoListAdmin"),
    path('admin-kurs-bolum-video-ekle/<int:pk>',sessionVideoAddAdmin,name="sessionVideoAddAdmin"),
    path('admin-kurs-bolum-video-sil/<int:pk>',deleteSessionVideoAdmin,name="deleteSessionVideoAdmin"),
    path('admin-profil-ayarlari',profileSettingsAdmin,name="profileSettingsAdmin"),
    path('admin-sifre-degistir',changePasswordAdmin,name="changePasswordAdmin"),
    path('admin-yorumlari-listele',commentsAdmin,name="commentsAdmin"),
    path('admin-istek-yorumlar',commentsRequestAdmin,name="commentsRequestAdmin"),
    path('admin-yorum-kabul-et/<int:pk>',acceptCommentsRequestAdmin,name="acceptCommentsRequestAdmin"),
    path('admin-yorum-sil/<int:pk>',deleteComingRequestAdmin,name="deleteComingRequestAdmin"),
    path('admin-seo-ayarlar',showPagesAdmin,name="showPagesAdmin"),
    path('admin-seo-ekle',createPageModelAdmin,name="createPageModelAdmin"),
    path('admin-seo-sil/<int:pk>',deletePageModelAdmin,name="deletePageModelAdmin"),
    path('admin-tum-kullanicilar',userListAdmin,name="userListAdmin"),
    path('admin-yorum-yanit-ekle/<slug:slug>/<int:pk>',addReplyCommentAdmin,name="addReplyCommentAdmin"),
    path('admin-tum-bildirimler',listNotificationsAdmin,name="listNotificationsAdmin"),
    path('admin-bildirim-sil/<int:pk>',deleteNotificationsAdmin,name="deleteNotificationsAdmin"),
    path('admin-tum-satin-alimlar',listBillingsAdmin,name="listBillingsAdmin"),
    path('admin-tum-sliderlar',listSlidersAdmin,name="listSlidersAdmin"),
    path('admin-slider-ekle',createSliderModelAdmin,name="createSliderModelAdmin"),
    path('admin-slider-sil/<int:pk>',deleteSliderAdmin,name="deleteSliderAdmin"),
    

]