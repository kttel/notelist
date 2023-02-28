from django.urls import path

from knox import views as knox_views

from api import views


urlpatterns = [
    path('', views.get_routes, name='routes'),
    path('register/', views.CreateUserView.as_view(), name='register-user'),
    path('login/', views.LoginView.as_view(), name='login-user'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout-user'),
    path('me/', views.ProfileView.as_view(), name='profile'),
    path('notes/', views.NotesListView.as_view(), name='notes-list'),
    path('notes/categories/', views.CategoryListView.as_view(),
         name='categories-list'),
    path('notes/<int:pk>/', views.NoteDetailView.as_view(),
         name='note-detail'),
]
