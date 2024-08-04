from django.urls import path

from . import views
from .views import upload_image
from .views import get_csrf_token

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #basic 
    path("",views.index,name="index"),

    #for files 
    path('upload/', upload_image, name='upload_image'),
    path('csrf/', get_csrf_token, name='get_csrf_token'),

    path("sampleData/",views.sampleData,name="sampleData"),

    #for history
    path("get_history/",views.get_history,name="get_history"),

    #for doc
    path("doc_info/",views.doc_info,name="doc_info"),
    path("get_verify_list/",views.get_verify_list,name="get_verify_list"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)