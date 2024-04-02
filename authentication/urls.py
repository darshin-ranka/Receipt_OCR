from django.contrib import admin
from django.urls import path
from . import views
from authentication.views import document_extractor , home 
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    #path('',views.home,name='home'),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('signout',views.signout,name="signout"),
    path('',home,name='home'),
    path('upload/', document_extractor, name='document_extractor'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#used to serve media files during development, allowing you to access uploaded files 
#(such as images, documents, etc.) directly from your Django server.


