from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('login/', views.signin, name='login'),
    path('usuario/editar/', views.editar, name='editar'),
    path('usuario/<int:usuario_id>/', views.usuario, name='usuario'),
]