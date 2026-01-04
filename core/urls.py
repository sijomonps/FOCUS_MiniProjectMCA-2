from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    # Main Pages
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('study/', views.study_view, name='study'),
    path('assignments/', views.assignments_view, name='assignments'),
    path('notes/', views.notes_view, name='notes'),
    
    # AJAX Endpoints
    path('api/study/save/', views.save_study_session, name='save_study_session'),
    path('api/assignment/add/', views.add_assignment, name='add_assignment'),
    path('api/assignment/<int:assignment_id>/complete/', views.complete_assignment, name='complete_assignment'),
    path('api/assignment/delete/<int:assignment_id>/', views.delete_assignment, name='delete_assignment'),
    path('api/assignments/completed/all/', views.get_all_completed_assignments, name='get_all_completed_assignments'),
    path('api/note/save/', views.save_quick_note, name='save_quick_note'),
    path('api/folder/create/', views.create_subject_folder, name='create_subject_folder'),
    path('api/note/create/', views.create_note, name='create_note'),
    path('api/note/delete/', views.delete_note, name='delete_note'),
    path('api/folder/delete/', views.delete_folder, name='delete_folder'),
]
