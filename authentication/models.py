from django.db import models

# Create your models here.
from django.contrib.auth.models import User

#model named UploadedImage  represents a database table, and each field in the model corresponds to a column in the table.
class UploadedImage(models.Model):
    #defines a field named image in the UploadedImage model. It's an ImageField, which means it can store image files. 
    #upload_to parameter specifies the directory where uploaded images will be stored relative to the MEDIA_ROOT directory 
    #In this case, images will be stored in the uploaded_images/ directory
    image = models.ImageField(upload_to='uploaded_images/')
    #defines a field named text in the UploadedImage model. It's a TextField, which means it can store text data 
    #blank=True, null=True parameters indicate that this field is optional and can be left blank or set to null in the database.
    text = models.TextField(blank=True, null=True)



#defines a special method called __str__. This method is called when you want to represent an instance of the UploadedImage model as a string, 
#such as when it's displayed in the Django admin interface or in template rendering.
def __str__(self):
    # line specifies what should be returned when the __str__ method is called on an instance of the UploadedImage model.
     #It returns a formatted string that includes the image filename (self.image) and the text associated with the image (self.text)
    return f"Image: {self.image}, Text: {self.text}"



