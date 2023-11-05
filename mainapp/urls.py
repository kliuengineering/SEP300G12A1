from django.urls import path
from django.views.generic.base import RedirectView
from mainapp import views

urlpatterns = [
    path('', RedirectView.as_view(url='upload/')),  
    path('upload/', views.upload, name='upload')
]
