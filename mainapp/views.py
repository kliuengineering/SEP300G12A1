# render and redirection
from django.shortcuts import render, redirect

# handling file storage natively
from django.core.files.storage import FileSystemStorage

# Create your views here.

# upload view; referencing to the html and css for details
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
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)


