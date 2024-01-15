from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include

urlpatterns = [
    path('', include('base.urls')),
    path('animal/', include('animals.urls', namespace='animals')),
    path('samples/', include('samples.urls', namespace='samples')),
    path('owners/', include('owners.urls', namespace='owners')),
    path('reports/', include('reports.urls', namespace='reports')),
    path('admin/', admin.site.urls),
] 