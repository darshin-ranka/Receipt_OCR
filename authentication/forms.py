from django import forms
from .models import UploadedImage
from multiupload.fields import MultiFileField
# class UploadImageForm(forms.ModelForm):
#     class Meta:
#         model = UploadedImage
#         fields = ['image']


#defines a Django form class named UploadMultipleImagesForm. It inherits from forms.Form, which means it's a standard form class 
#without any model association.

class UploadMultipleImagesForm(forms.Form):
    # a form field named images. It's an instance of MultiFileField, which is a field specifically designed for handling multiple file uploads.
    images = MultiFileField(min_num=1, max_num=100, max_file_size=1024*1024*5)