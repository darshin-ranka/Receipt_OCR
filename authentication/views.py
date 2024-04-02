from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from .forms import UploadMultipleImagesForm
from .models import UploadedImage
from .utils import extract_text_from_image
from django.contrib.auth.models import User
from PIL import Image
import torch
from transformers import LayoutLMForSequenceClassification, LayoutLMTokenizer
import pytesseract
import cv2



# Create your views here.
def home(request):
    return render(request,"authentication/index.html")

#funct name signup take req object as parameter
def signup(request):
    if request.method=="POST":    #checj req method is post
        #this lines retrive data from the submitted from each field corresponds to the variable in the form
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # after the user get registered with all this input we will registerd it in our backend i.e in database
        # creating a object i.e my user, create_user is an in built funct which take 3 parameters username email and pass1
        #User here represents the model or class  that Django provides for managing user account
        #.objects.create_user() method is a convenience method provided by Django for creating a new user instance.
        # It automatically handles hashing the password and saving the user object to the database.
        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname

        # save the user object in database
        myuser.save()
        
        #when user registered successfully we will give a message through django messages library.
        messages.success(request, "Your account has been succesfully created.")
        
        # now redirecting to signin page

        return redirect('signin')
         #if the request method is not POST, it renders the signup.html 
    return render(request,"authentication/signup.html")


#functn name sigin which take req as parameter
def signin(request):

    if request.method == 'POST':    # check request method is POST
        #retrive the username and pass1 entered by user through from the post data sent by sign in form
        username = request.POST['username']
        pass1=request.POST['pass1']

        #inbuilt funct authenticate which checks the username and password is matching to user's database
        user=authenticate(username=username,password=pass1)

        #if user is succesfully authenticate this block execute
        if user is not None:
            login(request, user)  # this logs in the user by creating session for them so they don't have to login again for subsequent request
            fname=user.first_name   # retrive first name of authenticated user
            return render(request,"authentication/index.html",{'fname':fname})
        else:   #if authenticate fails this code execute 
            messages.error(request, "Bad Credentials")  # generate the error message
            return redirect('home') # redirect to home page
        
        
    return render(request,"authentication/signin.html") #if req method is not POST this line render the signin html page which contain signin form

# function signout which take req as parameter
def signout(request):
     logout(request) #logout is funct provided by djnago , it logout the currently authenticated user by deleting their session data
     messages.success(request,"Logged Out Succesfully!") #generate msg of succesfully logout
     return redirect('home')    # redirect to home page    redirect is a shortcut function to perform an HTTP redirect to a specified URL or view name.







def document_extractor(request):  # function which take req as parameter
    if request.method == 'POST':  # check req method is POST
        #this line initialize form obj (form) with data from POST req. It is a form for uploading multiple img hence request.files contains any uploaded files

        form = UploadMultipleImagesForm(request.POST, request.FILES)
        if form.is_valid():   #check submitted form data is valid
            uploaded_images = []   #initialize an empty list to store upload image object


            #loop through each uploaded image file 'request.FILES.getlist('images')' retrive a list of uploaded image
            for image_file in request.FILES.getlist('images'):
                #for each uploade image a new uploaded_image obj is created with the image file and save to database

                uploaded_image = UploadedImage(image=image_file)
                uploaded_image.save()

                # Load uploaded image
                img = cv2.imread(uploaded_image.image.path)
                # Convert image to grayscale
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # Apply threshold to convert to binary image  it improve text extraction process
                threshold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                #cv2.THRESH_BINARY means that pixels with intensities(brightness and darkness) greater than the threshold value will be set to the maximum value (255), and others will be set to 0. 
                #cv2.THRESH_OTSU is a method for automatically determining the optimal threshold value based on the image histogram. It's particularly useful when the threshold value is not known in advance.
                
                # Extract text from the image using pytesseract that perform OCR
                text = pytesseract.image_to_string(threshold_img)
                # # extracted text is save to text attribute of uploaded_image  object and save to database
                uploaded_image.text = text
                uploaded_image.save()
                uploaded_images.append(uploaded_image)  # uploaded_image object is added to list of uploaded_image
            #after processing all uploaded images the user is redirected to index.html, passing the form and the list of uploaded images as context data
            return render(request, 'authentication/index.html', {'form': form, 'uploaded_images': uploaded_images})
    else:
        #if req method is not pOST new insatnce of uploadMultipleImageForm is created.this is for rendering the form in case od GEt req or form is not valid
        form = UploadMultipleImagesForm()
    return render(request, 'authentication/index.html', {'form': form})#index.html template is rendered passing the form as context data.





# views.py





# def document_extractor(request):
#     if request.method == 'POST':
#         form = UploadImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             uploaded_image = form.save()
#             text = extract_text_from_image(uploaded_image.image)
#             uploaded_image.text = text
#             uploaded_image.save()
#             return render(request, 'authentication/index.html', {'uploaded_image': uploaded_image, 'form': UploadImageForm()})
#     else:
#         form = UploadImageForm()
#     return render(request, 'authentication/index.html', {'form': form})







# def document_extractor(request):
#     if request.method == 'POST':
#         form = UploadImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             uploaded_image = form.save()

#             # Load uploaded image
#             img = cv2.imread(uploaded_image.image.path)
            
#             # Convert image to grayscale
#             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#             # Apply threshold to convert to binary image
#             threshold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#             # Extract text from the image using pytesseract
#             text = pytesseract.image_to_string(threshold_img)
#             print(text)

#             # Save extracted text to the uploaded image object
#             uploaded_image.text = text
#             uploaded_image.save()

#             # Render the HTML template with the uploaded image and form
#             return render(request, 'authentication/index.html', {'uploaded_image': uploaded_image, 'form': UploadImageForm()})
#     else:
#         form = UploadImageForm()
    
#     # Render the HTML template with the form
#     return render(request, 'authentication/index.html', {'form': form})
















