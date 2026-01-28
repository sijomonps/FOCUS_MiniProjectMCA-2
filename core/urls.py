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
    path('support/', views.support_view, name='support'),
    
    # Admin Pages (Superuser Only)
    path('admin-panel/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-panel/users/', views.admin_users_view, name='admin_users'),
    path('admin-panel/users/<int:user_id>/', views.admin_user_detail_view, name='admin_user_detail'),
    path('admin-panel/passwords/', views.admin_passwords_view, name='admin_passwords'),
    path('admin-panel/report/', views.admin_generate_report, name='admin_generate_report'),
    path('admin-panel/messages/', views.admin_messages_view, name='admin_messages'),
    path('admin-panel/study-sessions/', views.admin_study_sessions_view, name='admin_study_sessions'),
    
    # Admin API Endpoints
    path('api/admin/user/toggle-status/', views.admin_toggle_user_status, name='admin_toggle_user_status'),
    path('api/admin/user/delete/', views.admin_delete_user, name='admin_delete_user'),
    path('api/admin/user/change-password/', views.admin_change_password, name='admin_change_password'),
    path('api/admin/message/respond/', views.admin_respond_message, name='admin_respond_message'),
    path('api/admin/feedback/approve/', views.admin_approve_feedback, name='admin_approve_feedback'),
    path('api/admin/session/edit/', views.admin_edit_session, name='admin_edit_session'),
    path('api/admin/session/delete/', views.admin_delete_session, name='admin_delete_session'),
    
    # Support/Message API Endpoints
    path('api/support/send/', views.send_support_message, name='send_support_message'),
    path('api/support/messages/', views.get_user_messages, name='get_user_messages'),
    
    # AJAX Endpoints
    path('api/study/save/', views.save_study_session, name='save_study_session'),
    path('api/study/today/', views.get_today_study_time, name='get_today_study_time'),
    path('api/assignment/add/', views.add_assignment, name='add_assignment'),
    path('api/assignment/<int:assignment_id>/complete/', views.complete_assignment, name='complete_assignment'),
    path('api/assignment/<int:assignment_id>/status/', views.update_assignment_status, name='update_assignment_status'),
    path('api/assignment/<int:assignment_id>/update/', views.update_assignment, name='update_assignment'),
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
