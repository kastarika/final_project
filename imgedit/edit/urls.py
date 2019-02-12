#from django.urls.static import static
#from django.conf import settings
from django.urls import path, include
from . import views

app_name = 'edit'

urlpatterns = [
    path('', views.first_page, name='first_page'),
    path('show_all/', views.show_all, name='show_all'),
    path('upload/', views.upload, name='upload'),
    path('edit/<int:shomare>/', views.edit, name='edit')
]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
