from django.contrib import admin
from .models import (
    Post, Comment, Profile, SiteConfig, 
    Course, CourseItem, AcademyVideo, AcademyExercise, 
    UserProgress, UserCourseProgress, Badge, UserBadge
)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'media_type', 'is_published', 'created_at']
    list_filter = ['is_published', 'media_type', 'created_at']
    search_fields = ['title', 'content']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['content', 'author__username']
    date_hierarchy = 'created_at'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'birth_date']
    search_fields = ['user__username', 'bio']


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ['id', 'updated_at']
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteConfig.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False


# ===== ACADEMY COURSES =====

class CourseItemInline(admin.TabularInline):
    model = CourseItem
    extra = 1
    fields = ['order', 'content_type', 'video', 'exercise', 'is_required']
    ordering = ['order']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'order', 'is_active', 'is_featured', 'get_items_count', 'created_at']
    list_filter = ['level', 'is_active', 'is_featured', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order', '-created_at']
    list_editable = ['order', 'is_active', 'is_featured']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CourseItemInline]
    
    fieldsets = (
        ('Information Générale', {
            'fields': ('title', 'slug', 'description', 'level')
        }),
        ('Média', {
            'fields': ('thumbnail',)
        }),
        ('Paramètres', {
            'fields': ('order', 'is_active', 'is_featured', 'estimated_duration')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_items_count(self, obj):
        return f"📹 {obj.get_videos_count()} | 💻 {obj.get_exercises_count()}"
    get_items_count.short_description = 'Contenu'


@admin.register(CourseItem)
class CourseItemAdmin(admin.ModelAdmin):
    list_display = ['course', 'order', 'content_type', 'get_content_title', 'is_required']
    list_filter = ['course', 'content_type', 'is_required']
    search_fields = ['course__title', 'video__title', 'exercise__title']
    ordering = ['course', 'order']
    list_editable = ['order', 'is_required']
    
    def get_content_title(self, obj):
        content = obj.get_content()
        if content:
            return content.title
        return "—"
    get_content_title.short_description = 'Titre du Contenu'


@admin.register(AcademyVideo)
class AcademyVideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'duration', 'order', 'is_active', 'created_at']
    list_filter = ['level', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['order', '-created_at']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Information Générale', {
            'fields': ('title', 'description', 'level', 'duration')
        }),
        ('Média', {
            'fields': ('video_url', 'thumbnail')
        }),
        ('Paramètres', {
            'fields': ('order', 'is_active')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AcademyExercise)
class AcademyExerciseAdmin(admin.ModelAdmin):
    list_display = ['title', 'language', 'difficulty', 'order', 'is_active', 'created_at']
    list_filter = ['language', 'difficulty', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'instructions']
    ordering = ['order', '-created_at']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Information Générale', {
            'fields': ('title', 'description', 'language', 'difficulty')
        }),
        ('Contenu de l\'Exercice', {
            'fields': ('instructions', 'starter_code', 'solution_code', 'test_cases')
        }),
        ('Paramètres', {
            'fields': ('order', 'is_active')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'level', 'xp', 'total_points', 'streak_days', 'completed_videos_count', 'completed_exercises_count', 'last_activity']
    list_filter = ['level', 'last_activity', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['user', 'last_activity', 'created_at']
    filter_horizontal = ['completed_videos', 'completed_exercises']
    
    def completed_videos_count(self, obj):
        return obj.completed_videos.count()
    completed_videos_count.short_description = 'Vidéos Complétées'
    
    def completed_exercises_count(self, obj):
        return obj.completed_exercises.count()
    completed_exercises_count.short_description = 'Exercices Complétés'
    
    def has_add_permission(self, request):
        # Progress is created automatically
        return False


@admin.register(UserCourseProgress)
class UserCourseProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'completion_percentage', 'is_started', 'is_completed', 'last_accessed']
    list_filter = ['is_started', 'is_completed', 'course', 'last_accessed']
    search_fields = ['user__username', 'course__title']
    readonly_fields = ['started_at', 'completed_at', 'last_accessed', 'completion_percentage']
    filter_horizontal = ['completed_items']
    
    fieldsets = (
        ('Utilisateur & Cours', {
            'fields': ('user', 'course')
        }),
        ('Progression', {
            'fields': ('current_item', 'completion_percentage', 'is_started', 'is_completed')
        }),
        ('Items Complétés', {
            'fields': ('completed_items',)
        }),
        ('Dates', {
            'fields': ('started_at', 'completed_at', 'last_accessed'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Progress is created automatically
        return False


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['icon', 'name', 'condition_type', 'condition_value', 'color', 'order', 'is_active']
    list_filter = ['condition_type', 'is_active', 'color']
    search_fields = ['name', 'description']
    ordering = ['order', 'name']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('Badge Info', {
            'fields': ('name', 'description', 'icon', 'color')
        }),
        ('Unlock Conditions', {
            'fields': ('condition_type', 'condition_value')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'unlocked_at']
    list_filter = ['unlocked_at', 'badge']
    search_fields = ['user__username', 'badge__name']
    readonly_fields = ['unlocked_at']
    ordering = ['-unlocked_at']
    
    def has_add_permission(self, request):
        # Badges are unlocked automatically
        return True  # Allow manual unlock if needed

