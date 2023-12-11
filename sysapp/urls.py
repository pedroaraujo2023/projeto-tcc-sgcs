from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('cadastrar/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('accounts/login/', views.fazer_login, name='fazer_login'),
    path('abrirchamado/', views.abrir_chamados, name='abrir_chamados'),
    path('logout/', auth_views.LogoutView.as_view(next_page='fazer_login'), name='logout'),
    path('dashboard/chamados/<str:estado>/', views.dashboard_chamados, name='dashboard_chamados'),

]
