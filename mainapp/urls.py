# handling paths
from django.urls import path

# need the following import to redirect urls
from django.views.generic.base import RedirectView

# include views 
from mainapp import views

# blocks users from viewing the root directory;
# users are redirected to the upload view
urlpatterns = [
    # redirects the user to the upload page
    path('', RedirectView.as_view(url='upload/')),  
    path('upload/', views.upload, name='upload')
]
