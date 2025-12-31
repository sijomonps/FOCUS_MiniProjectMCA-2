from django.contrib import admin
from .models import StudySession, Assignment, QuickNote, SubjectFolder

@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'duration', 'date', 'created_at')
    list_filter = ('date', 'subject')
    search_fields = ('user__username', 'subject')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'user', 'deadline', 'status', 'urgency', 'days_remaining')
    list_filter = ('status', 'urgency', 'deadline')
    search_fields = ('title', 'subject', 'user__username')
    
    def days_remaining(self, obj):
        return obj.days_remaining()
    days_remaining.short_description = 'Days Left'

@admin.register(SubjectFolder)
class SubjectFolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'note_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'user__username')
    
    def note_count(self, obj):
        return obj.note_count()
    note_count.short_description = 'Notes'

@admin.register(QuickNote)
class QuickNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'subject_folder', 'created_at', 'updated_at')
    list_filter = ('subject_folder', 'created_at')
    search_fields = ('user__username', 'title', 'content')

