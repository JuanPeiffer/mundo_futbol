from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('login/', views.signin, name='login'),
    path('usuario/editar/', views.editar, name='editar'),
    path('usuario/<int:usuario_id>/', views.usuario, name='usuario'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)