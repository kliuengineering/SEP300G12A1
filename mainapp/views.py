# render and redirection
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreationForm, LoginForm
from django.contrib.auth.decorators import login_required

# handling uploaded file
from .models import UploadedFile

# handling file storage natively
from django.core.files.storage import FileSystemStorage

# Create your views here.

# upload view; referencing to the html and css for details
@login_required
def upload(request):
    # dictionary for data exchange between view and upload.html
    context = {}

    # if it is a HTTP POST or not
    if request.method == 'POST':

        # contains the user upload
        uploaded_file = request.FILES['document']

        # creates an object to manipulate uploaded data
        fs = FileSystemStorage()

        # saves data into the file system
        name = fs.save(uploaded_file.name, uploaded_file)

        # generates key-value pair: key being the url 
        # context['url'] = fs.url(name)
        file_url = fs.url(name)

        # associate the file URL with the current user
        UploadedFile.objects.create(user=request.user, file_url=file_url)

        context['url'] = file_url

    return render(request, 'upload.html', context)


# Signup page
def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('upload')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


# logout page
def user_logout(request):
    logout(request)
    return redirect('login')


