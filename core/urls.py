from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Páginas principales
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    
    # Cursos
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:course_id>/edit/', views.course_edit, name='course_edit'),
    path('courses/<int:course_id>/delete/', views.course_delete, name='course_delete'),
    
    # Lecciones
    path('courses/<int:course_id>/lessons/create/', views.lesson_create, name='lesson_create'),
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('lessons/<int:lesson_id>/edit/', views.lesson_edit, name='lesson_edit'),
    path('lessons/<int:lesson_id>/delete/', views.lesson_delete, name='lesson_delete'),
    
    # Evaluaciones
    path('courses/<int:course_id>/evaluations/create/', views.evaluation_create, name='evaluation_create'),
    path('evaluations/<int:evaluation_id>/', views.evaluation_detail, name='evaluation_detail'),
    path('evaluations/<int:evaluation_id>/edit/', views.evaluation_edit, name='evaluation_edit'),
    path('evaluations/<int:evaluation_id>/delete/', views.evaluation_delete, name='evaluation_delete'),
    
    # Calificaciones
    path('evaluations/<int:evaluation_id>/score/<int:student_id>/', views.score_create, name='score_create'),
    path('scores/<int:score_id>/edit/', views.score_edit, name='score_edit'),
    
    # Inscripciones
    path('courses/<int:course_id>/enroll/', views.enroll, name='enroll'),
    path('enrollments/<int:enrollment_id>/cancel/', views.enrollment_cancel, name='enrollment_cancel'),
]
