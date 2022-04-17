from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap


from .views import (
    index,login,logoutIndex,registerUser,changePassword,profileSettings,coursesGridList,favouritesCoursesGridList,
    AddFavouritesCoursesGridList,courseDetail,learningContentList,aboutUs,contact,aydinlatmaMetni,gizlilikPolitikası,
    kvkkMetni,blogDetail,allBlogs,paymentPage,successPayment,failPayment,callback,mesafeliSatis,footerMailSave,
    appointment,addWatchedList,times,activate
)



from .sitemaps import StaticViewSitemap,courseSiteMap,blogSiteMap,paymentPageSiteMap,successPaymentPageSiteMap,failPaymentPageSiteMap,addFavouriteSiteMap,appointmentSiteMap



sitemaps = {
    'static': StaticViewSitemap,
    "course": courseSiteMap,
    "blog": blogSiteMap,
    "payment": paymentPageSiteMap,
    "successPayment": successPaymentPageSiteMap,
    "failPayment": failPaymentPageSiteMap,
    "favourites":addFavouriteSiteMap,
    "appointmentSiteMap":appointmentSiteMap
}



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
    path('aydinlatma-metni',aydinlatmaMetni,name="aydinlatmaMetni"),
    path('gizlilik-politikasi',gizlilikPolitikası,name="gizlilikPolitikası"),
    path('kvkk-metni',kvkkMetni,name="kvkkMetni"),
    path('blog-detay/<slug:slug>',blogDetail,name="blogDetail"),
    path('tum-blog-yazilari',allBlogs,name="allBlogs"),
    path('odeme-sayfasi/<slug:slug>',paymentPage,name="paymentPage"),
    path('basarili-odeme/<slug:slug>',successPayment,name="successPayment"),
    path('hatali-odeme/<slug:slug>',failPayment,name="failPayment"),
    path('odeme-sonucu',callback,name="callback"),
    path('mesafeli-satis-sozlesmesi',mesafeliSatis,name="mesafeliSatis"),
    path('footer-mail-kaydet',footerMailSave,name="footerMailSave"),
    path('randevu-talebi/<int:randevuId>',appointment,name="appointment"),
    path('izlenenlere-ekle',addWatchedList,name="addWatchedList"),
    path('uygun-zamanlar',times,name="times"),
    path('activate/<uidb64>/<token>/',activate, name='activate'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')

]   