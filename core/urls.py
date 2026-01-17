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
    
    # Admin Pages (Superuser Only)
    path('admin-panel/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-panel/users/', views.admin_users_view, name='admin_users'),
    path('admin-panel/users/<int:user_id>/', views.admin_user_detail_view, name='admin_user_detail'),
    
    # Admin API Endpoints
    path('api/admin/user/toggle-status/', views.admin_toggle_user_status, name='admin_toggle_user_status'),
    path('api/admin/user/delete/', views.admin_delete_user, name='admin_delete_user'),
    
    # AJAX Endpoints
    path('api/study/save/', views.save_study_session, name='save_study_session'),
    path('api/assignment/add/', views.add_assignment, name='add_assignment'),
    path('api/assignment/<int:assignment_id>/complete/', views.complete_assignment, name='complete_assignment'),
    path('api/assignment/delete/<int:assignment_id>/', views.delete_assignment, name='delete_assignment'),
    path('api/assignments/completed/all/', views.get_all_completed_assignments, name='get_all_completed_assignments'),
    path('api/note/save/', views.save_quick_note, name='save_quick_note'),
    path('api/folder/create/', views.create_subject_folder, name='create_subject_folder'),
    path('api/folder/delete/', views.delete_subject_folder, name='delete_subject_folder'),
    path('api/note/create/', views.create_note, name='create_note'),
    path('api/note/update/', views.update_note, name='update_note'),
    path('api/note/delete/', views.delete_note, name='delete_note'),
    path('api/note/toggle-pin/', views.toggle_pin_note, name='toggle_pin_note'),
    path('api/folder/delete-by-id/', views.delete_folder, name='delete_folder'),
]
