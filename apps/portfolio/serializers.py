from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Post, Comment, Profile, SiteConfig, 
    Course, CourseItem, AcademyVideo, AcademyExercise, 
    UserProgress, UserCourseProgress
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'location', 'birth_date', 'avatar']
        read_only_fields = ['id']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_id', 'content', 'created_at', 'is_approved']
        read_only_fields = ['id', 'created_at', 'author']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'media', 'video_url', 'media_type',
            'author', 'created_at', 'updated_at', 'is_published', 'comments_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'author']

    def get_comments_count(self, obj):
        return obj.comments.filter(is_approved=True).count()

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'media', 'video_url', 'media_type',
            'author', 'created_at', 'updated_at', 'is_published',
            'comments', 'comments_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'author']

    def get_comments_count(self, obj):
        return obj.comments.filter(is_approved=True).count()

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class SiteConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteConfig
        fields = [
            'id', 'cv', 'github_url', 'linkedin_url', 'twitter_url', 'email',
            'home_title', 'home_subtitle', 'home_description', 'about_text', 'skills_json',
            'updated_at'
        ]
        read_only_fields = ['id', 'updated_at']


class AcademyVideoSerializer(serializers.ModelSerializer):
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    
    class Meta:
        model = AcademyVideo
        fields = [
            'id', 'title', 'description', 'video_url', 'thumbnail', 'duration',
            'level', 'level_display', 'order', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AcademyExerciseSerializer(serializers.ModelSerializer):
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    language_display = serializers.CharField(source='get_language_display', read_only=True)
    is_completed = serializers.SerializerMethodField()
    
    class Meta:
        model = AcademyExercise
        fields = [
            'id', 'title', 'description', 'language', 'language_display', 
            'difficulty', 'difficulty_display', 'instructions', 'starter_code',
            'order', 'is_active', 'is_completed', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_is_completed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.completed_by.filter(user=request.user).exists()
        return False


class ExerciseSubmissionSerializer(serializers.Serializer):
    exercise_id = serializers.IntegerField()
    code = serializers.CharField()
    
    
class UserProgressSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    completed_videos_count = serializers.SerializerMethodField()
    completed_exercises_count = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProgress
        fields = [
            'id', 'user', 'completed_videos_count', 'completed_exercises_count',
            'total_points', 'streak_days', 'last_activity', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'last_activity', 'created_at']
    
    def get_completed_videos_count(self, obj):
        return obj.completed_videos.count()
    
    def get_completed_exercises_count(self, obj):
        return obj.completed_exercises.count()


# ===== COURSE SERIALIZERS =====

class CourseItemWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating course items"""
    
    class Meta:
        model = CourseItem
        fields = ['id', 'course', 'content_type', 'video', 'exercise', 'order', 'is_required']
        extra_kwargs = {
            'video': {'required': False, 'allow_null': True},
            'exercise': {'required': False, 'allow_null': True},
        }
    
    def validate(self, data):
        """Ensure either video or exercise is provided based on content_type"""
        content_type = data.get('content_type')
        video = data.get('video')
        exercise = data.get('exercise')
        
        if content_type == 'video' and not video:
            raise serializers.ValidationError({'video': 'Video is required when content_type is video'})
        if content_type == 'exercise' and not exercise:
            raise serializers.ValidationError({'exercise': 'Exercise is required when content_type is exercise'})
        
        return data


class CourseItemDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for course items including actual content"""
    content_title = serializers.SerializerMethodField()
    content_description = serializers.SerializerMethodField()
    content_data = serializers.SerializerMethodField()
    
    class Meta:
        model = CourseItem
        fields = [
            'id', 'course', 'order', 'content_type', 'video', 'exercise', 'is_required',
            'content_title', 'content_description', 'content_data'
        ]
        read_only_fields = ['content_title', 'content_description', 'content_data']
    
    def get_content_title(self, obj):
        content = obj.get_content()
        return content.title if content else None
    
    def get_content_description(self, obj):
        content = obj.get_content()
        return content.description if content else None
    
    def get_content_data(self, obj):
        """Return the full serialized content (video or exercise)"""
        if obj.content_type == 'video' and obj.video:
            return AcademyVideoSerializer(obj.video).data
        elif obj.content_type == 'exercise' and obj.exercise:
            return AcademyExerciseSerializer(obj.exercise, context=self.context).data
        return None


class CourseListSerializer(serializers.ModelSerializer):
    """Serializer for listing courses"""
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    items_count = serializers.SerializerMethodField()
    videos_count = serializers.IntegerField(source='get_videos_count', read_only=True)
    exercises_count = serializers.IntegerField(source='get_exercises_count', read_only=True)
    user_progress = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'thumbnail', 'level', 'level_display',
            'order', 'is_active', 'is_featured', 'estimated_duration',
            'items_count', 'videos_count', 'exercises_count', 'user_progress',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_items_count(self, obj):
        return obj.get_total_items()
    
    def get_user_progress(self, obj):
        """Get user's progress for this course"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                progress = UserCourseProgress.objects.get(user=request.user, course=obj)
                return {
                    'is_started': progress.is_started,
                    'is_completed': progress.is_completed,
                    'completion_percentage': progress.completion_percentage,
                    'current_item_order': progress.current_item.order if progress.current_item else None
                }
            except UserCourseProgress.DoesNotExist:
                pass
        return None


class CourseDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for a single course including all items"""
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    items = CourseItemDetailSerializer(many=True, read_only=True)
    items_count = serializers.SerializerMethodField()
    videos_count = serializers.IntegerField(source='get_videos_count', read_only=True)
    exercises_count = serializers.IntegerField(source='get_exercises_count', read_only=True)
    user_progress = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'thumbnail', 'level', 'level_display',
            'order', 'is_active', 'is_featured', 'estimated_duration',
            'items', 'items_count', 'videos_count', 'exercises_count', 'user_progress',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_items_count(self, obj):
        return obj.get_total_items()
    
    def get_user_progress(self, obj):
        """Get user's progress for this course"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                progress = UserCourseProgress.objects.get(user=request.user, course=obj)
                return {
                    'is_started': progress.is_started,
                    'is_completed': progress.is_completed,
                    'completion_percentage': progress.completion_percentage,
                    'current_item_id': progress.current_item.id if progress.current_item else None,
                    'current_item_order': progress.current_item.order if progress.current_item else None,
                    'completed_items_ids': list(progress.completed_items.values_list('id', flat=True))
                }
            except UserCourseProgress.DoesNotExist:
                pass
        return None


class UserCourseProgressSerializer(serializers.ModelSerializer):
    """Serializer for user course progress"""
    course = CourseListSerializer(read_only=True)
    current_item_detail = CourseItemDetailSerializer(source='current_item', read_only=True)
    
    class Meta:
        model = UserCourseProgress
        fields = [
            'id', 'user', 'course', 'current_item', 'current_item_detail',
            'is_started', 'is_completed', 'completion_percentage',
            'started_at', 'completed_at', 'last_accessed'
        ]
        read_only_fields = ['id', 'user', 'started_at', 'completed_at', 'last_accessed', 'completion_percentage']

