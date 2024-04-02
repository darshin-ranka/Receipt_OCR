from django.contrib import admin
from.models import UploadedImage

# Register your models here.
#UploadedImage model will be accessible and manageable through the Django admin interface.
@admin.register(UploadedImage)
#This class customizes how the UploadedImage model is displayed and managed in the Django admin interface.
class UploadImageAdmin(admin.ModelAdmin):
    list_display=['id','image','text']
    # line specifies which fields of the UploadedImage model should be displayed in the list view of the 
    #Django admin interface
    #the list will  display the id, image, and text fields of each UploadedImage object.
    





#  superuser name= darshin password =darshin