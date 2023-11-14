# render and redirection
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreationForm, LoginForm, SharedFileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import hashlib

# handling uploaded file
from .models import UploadedFile

# handling file storage natively
from django.core.files.storage import FileSystemStorage

# Create your views here.

# upload view; referencing to the html and css for details
# When a file is uploaded, calculate its SHA-256 hash and store it in the database along with the file.
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
        file_url = fs.url(name)

        # calculate the SHA-256 hash
        sha256_hash = hashlib.sha256()
        for chunk in uploaded_file.chunks():
            sha256_hash.update(chunk)

        # get the hex digest of the hash
        file_hash = sha256_hash.hexdigest()

        # associate the file URL with the current user
        # UploadedFile.objects.create(user=request.user, file_url=file_url)

        # creates an uploadedfile obj with the hash
        uploaded_file_obj = UploadedFile.objects.create(
            user=request.user, file_url=file_url, file_hash=file_hash
        )

        context['url'] = file_url

    return render(request, 'upload.html', context)


@login_required
def share_file(request, file_id):
    file_to_share = UploadedFile.objects.get(pk=file_id)

    if request.method == 'POST':
        form = SharedFileForm(request.POST)

        if form.is_valid():
            # Get the username from the form
            share_with_username = form.cleaned_data['share_with']

            try:
                # Get the user object based on the entered username
                shared_user = User.objects.get(username=share_with_username)

                # Add the user to the shared_with field
                file_to_share.shared_with.add(shared_user)
                return redirect('upload')
            except User.DoesNotExist:
                # Handle the case where the entered username doesn't exist
                form.add_error('share_with', 'User does not exist')

    else:
        form = SharedFileForm()

    return render(request, 'share_file.html', {'form': form, 'file_to_share': file_to_share})


@login_required
def delete_file(request, file_id):
    # Get the file object
    file_to_delete = UploadedFile.objects.get(pk=file_id)

    # Check if the user is the owner of the file
    if request.user == file_to_delete.user:
        # Delete the file
        file_to_delete.delete()

    # Redirect back to the upload page
    return redirect('upload')


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


@login_required
# logout page
def user_logout(request):
    logout(request)
    return redirect('login')


