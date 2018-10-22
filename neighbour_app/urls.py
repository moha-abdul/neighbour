from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns=[

    url(r'^$',views.home,name = 'home'),
    url(r'signup/', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^profile/',views.profile,name='profile'),
    url(r'^edit_profile/', views.edit_profile, name = 'edit_profile'),
    url(r'^new_post/', views.new_post, name = 'new_post'),
    url(r'single_post/(\d+)',views.single_post, name = 'single_post'),
    url(r'new_biz/',views.new_biz, name = 'new_biz'),
    url(r'^search_biz/', views.search_biz, name ='search_biz'),
    url(r'neighbour/(\d+)',views.neighbour, name = 'neighbour'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)