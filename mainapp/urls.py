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
    #path('', RedirectView.as_view(url='upload/')),
    path('', RedirectView.as_view(url='login')),
    path('upload/', views.upload, name='upload'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),

]
