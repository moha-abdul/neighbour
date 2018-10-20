from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views 

urlpatterns = [
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'', include('neighbour_app.urls')),
    url(r'^logout/$', views.logout, {"next_page": '/'}),
]
