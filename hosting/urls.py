from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    # redirection to url.py in the mainapp if needed
    path('', RedirectView.as_view(url="mainapp/")),  

    # routes requests to the admin interface
    path('admin/', admin.site.urls),

    # includes the urls from mainapp
    path('mainapp/', include('mainapp.urls')),
]

# checks if we are in the development mode or not; T = debug, F = production
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
