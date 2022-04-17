from django.contrib import sitemaps
from django.urls import reverse

from Admin.models import CourseModel, appointmentModel, blogModel

class StaticViewSitemap(sitemaps.Sitemap):
    protocol = 'https'

    def items(self):
        return ['index', 'login', 'logoutIndex','registerUser','changePassword','password_reset','password_reset_done','password_reset_complete',
        'profileSettings','coursesGridList','favouritesCoursesGridList',
        'learningContentList','aboutUs','contact','aydinlatmaMetni','gizlilikPolitikası','kvkkMetni','allBlogs',
        'callback','mesafeliSatis','footerMailSave',"times"]

    def location(self, item):
        return reverse(item)
    
 






class courseSiteMap(sitemaps.Sitemap):
    protocol = 'https'

    def items(self):
        return CourseModel.objects.all()

        
    def location(self,obj):
        return '/kurs-detay/%s' % (obj.slug)






class blogSiteMap(sitemaps.Sitemap):
    protocol = 'https'

    def items(self):
        return blogModel.objects.all()

        
    def location(self,obj):
        return '/blog-detay/%s' % (obj.slug)




class paymentPageSiteMap(sitemaps.Sitemap):
    protocol = 'https'

    def items(self):
        return CourseModel.objects.all()

        
    def location(self,obj):
        return '/odeme-sayfasi/%s' % (obj.slug)




class successPaymentPageSiteMap(sitemaps.Sitemap):
    protocol = 'https'

    def items(self):
        return CourseModel.objects.all()

        
    def location(self,obj):
        return '/basarili-odeme/%s' % (obj.slug)




class failPaymentPageSiteMap(sitemaps.Sitemap):
    protocol = 'https'

    def items(self):
        return CourseModel.objects.all()

        
    def location(self,obj):
        return '/hatali-odeme/%s' % (obj.slug)







class addFavouriteSiteMap(sitemaps.Sitemap):
    protocol = 'https'

    def items(self):
        return CourseModel.objects.all()

        
    def location(self,obj):
        return '/favori-kurs-ekle/%s' % (obj.pk)







class appointmentSiteMap(sitemaps.Sitemap):
    protocol = 'https'

    def items(self):
        return appointmentModel.objects.all()

        
    def location(self,obj):
        return '/randevu-talebi/%s' % (obj.pk)