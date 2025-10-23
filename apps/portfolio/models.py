import os
from io import BytesIO
from PIL import Image

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.base import ContentFile


class Post(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    media = models.FileField(upload_to='posts_media/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.media:
            ext = os.path.splitext(self.media.name)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.gif']:
                self.media_type = 'image'
                if ext != '.gif':
                    self.media = self.compress_image(self.media)
        elif self.video_url:
            self.media_type = 'video'
        super().save(*args, **kwargs)

    def compress_image(self, uploaded_file):
        """Compress uploaded images"""
        try:
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            img = Image.open(uploaded_file)

            max_size = (1600, 1600)
            img.thumbnail(max_size, Image.LANCZOS)

            buffer = BytesIO()

            if ext in ['.jpg', '.jpeg']:
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                img.save(buffer, format='JPEG', quality=75, optimize=True)
                new_name = os.path.splitext(uploaded_file.name)[0] + '.jpg'
            elif ext == '.png':
                img.save(buffer, format='PNG', optimize=True)
                new_name = uploaded_file.name
            else:
                return uploaded_file

            buffer.seek(0)
            return ContentFile(buffer.getvalue(), name=new_name)
        except Exception:
            return uploaded_file


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f'Profile of {self.user.username}'


class SiteConfig(models.Model):
    cv = models.FileField(upload_to='cv/', blank=True, null=True)
    
    # Social Media Links
    github_url = models.URLField(blank=True, null=True, help_text="GitHub profile URL")
    linkedin_url = models.URLField(blank=True, null=True, help_text="LinkedIn profile URL")
    twitter_url = models.URLField(blank=True, null=True, help_text="Twitter profile URL")
    email = models.EmailField(blank=True, null=True, help_text="Contact email")
    
    # Home Page Content
    home_title = models.CharField(max_length=200, blank=True, null=True, help_text="Main title on home page", default="Othmane Chaikhi")
    home_subtitle = models.CharField(max_length=200, blank=True, null=True, help_text="Subtitle on home page", default="Ingénieur en Informatique et Réseaux")
    home_description = models.TextField(blank=True, null=True, help_text="Description text on home page")
    about_text = models.TextField(blank=True, null=True, help_text="About me section text")
    skills_json = models.JSONField(blank=True, null=True, help_text="Skills as JSON array")
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Configuration'
        verbose_name_plural = 'Site Configuration'

    def __str__(self):
        return "Site Configuration"

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Course(models.Model):
    """A course/series that contains multiple videos and exercises"""
    LEVEL_CHOICES = [
        ('beginner', 'Débutant'),
        ('intermediate', 'Intermédiaire'),
        ('advanced', 'Avancé'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='courses/', blank=True, null=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    
    # Metadata
    order = models.IntegerField(default=0, help_text="Display order on courses list")
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    estimated_duration = models.IntegerField(default=0, help_text="Total duration in minutes")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_total_items(self):
        """Get total number of videos + exercises in this course"""
        return self.items.count()
    
    def get_videos_count(self):
        """Get number of videos in this course"""
        return self.items.filter(content_type='video').count()
    
    def get_exercises_count(self):
        """Get number of exercises in this course"""
        return self.items.filter(content_type='exercise').count()


class AcademyVideo(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Débutant'),
        ('intermediate', 'Intermédiaire'),
        ('advanced', 'Avancé'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_url = models.URLField(help_text="YouTube or Vimeo URL")
    thumbnail = models.ImageField(upload_to='academy/thumbnails/', blank=True, null=True)
    duration = models.CharField(max_length=20, help_text="e.g., '45 min'")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Academy Video'
        verbose_name_plural = 'Academy Videos'
    
    def __str__(self):
        return f"{self.title} ({self.get_level_display()})"


class AcademyExercise(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Facile'),
        ('medium', 'Moyen'),
        ('hard', 'Difficile'),
    ]
    
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('java', 'Java'),
        ('cpp', 'C++'),
        ('sql', 'SQL'),
        ('html', 'HTML/CSS'),
        ('other', 'Autre'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='easy')
    
    # Exercise content
    instructions = models.TextField(help_text="Detailed instructions for the exercise")
    starter_code = models.TextField(blank=True, help_text="Initial code provided to students")
    solution_code = models.TextField(help_text="Expected solution (for validation)")
    test_cases = models.JSONField(blank=True, null=True, help_text="Test cases as JSON")
    
    # Metadata
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Academy Exercise'
        verbose_name_plural = 'Academy Exercises'
    
    def __str__(self):
        return f"{self.title} ({self.get_language_display()} - {self.get_difficulty_display()})"


class CourseItem(models.Model):
    """Links videos and exercises to courses in a specific order"""
    CONTENT_TYPE_CHOICES = [
        ('video', 'Video'),
        ('exercise', 'Exercise'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='items')
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES)
    
    # Foreign keys to actual content (only one should be set)
    video = models.ForeignKey('AcademyVideo', on_delete=models.CASCADE, null=True, blank=True, related_name='course_items')
    exercise = models.ForeignKey('AcademyExercise', on_delete=models.CASCADE, null=True, blank=True, related_name='course_items')
    
    # Order in the course sequence
    order = models.IntegerField(default=0, help_text="Order in course sequence (1, 2, 3...)")
    is_required = models.BooleanField(default=True, help_text="Must complete to proceed")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['course', 'order']
        unique_together = ['course', 'order']
        verbose_name = 'Course Item'
        verbose_name_plural = 'Course Items'
    
    def __str__(self):
        if self.content_type == 'video' and self.video:
            return f"{self.course.title} - {self.order}. {self.video.title}"
        elif self.content_type == 'exercise' and self.exercise:
            return f"{self.course.title} - {self.order}. {self.exercise.title}"
        return f"{self.course.title} - Item {self.order}"
    
    def get_content(self):
        """Returns the actual video or exercise object"""
        if self.content_type == 'video':
            return self.video
        return self.exercise
    
    def get_next_item(self):
        """Get the next item in the course"""
        return CourseItem.objects.filter(
            course=self.course,
            order__gt=self.order
        ).order_by('order').first()
    
    def get_previous_item(self):
        """Get the previous item in the course"""
        return CourseItem.objects.filter(
            course=self.course,
            order__lt=self.order
        ).order_by('-order').first()


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='academy_progress')
    
    # Video progress
    completed_videos = models.ManyToManyField(AcademyVideo, blank=True, related_name='completed_by')
    
    # Exercise progress
    completed_exercises = models.ManyToManyField(AcademyExercise, blank=True, related_name='completed_by')
    
    # XP & Level System
    xp = models.IntegerField(default=0, help_text="Experience points")
    level = models.IntegerField(default=1, help_text="Current level")
    
    # Statistics
    total_points = models.IntegerField(default=0)
    streak_days = models.IntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True, help_text="Last day user was active")
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'User Progress'
        verbose_name_plural = 'User Progress'
    
    def __str__(self):
        return f"{self.user.username}'s Progress (Level {self.level}, {self.xp} XP)"
    
    def add_xp(self, points):
        """Add XP and automatically level up if threshold reached"""
        self.xp += points
        self.total_points += points
        
        # Level thresholds: 0-100: lvl 1, 100-300: lvl 2, 300-700: lvl 3, etc.
        level_thresholds = [0, 100, 300, 700, 1500, 3000, 6000, 10000]
        for level, threshold in enumerate(level_thresholds, start=1):
            if self.xp >= threshold:
                self.level = level
        
        self.save()
        return self.level
    
    def check_streak(self):
        """Check and update streak days"""
        from datetime import date, timedelta
        today = date.today()
        
        if self.last_activity_date:
            delta = (today - self.last_activity_date).days
            if delta == 1:
                # Consecutive day
                self.streak_days += 1
            elif delta > 1:
                # Streak broken
                self.streak_days = 1
            # If delta == 0 (same day), don't change streak
        else:
            self.streak_days = 1
        
        self.last_activity_date = today
        self.save()


class Badge(models.Model):
    CONDITION_TYPES = [
        ('exercises_completed', 'Exercises Completed'),
        ('videos_completed', 'Videos Completed'),
        ('streak', 'Streak Days'),
        ('xp_total', 'Total XP'),
        ('level_reached', 'Level Reached'),
        ('first_try_success', 'First Try Success'),
        ('time_based', 'Time Based Activity'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='🏆', help_text="Emoji or icon")
    condition_type = models.CharField(max_length=30, choices=CONDITION_TYPES)
    condition_value = models.IntegerField(help_text="Threshold to unlock")
    color = models.CharField(max_length=20, default='primary', help_text="Badge color theme")
    
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Badge'
        verbose_name_plural = 'Badges'
    
    def __str__(self):
        return f"{self.icon} {self.name}"


class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'badge']
        ordering = ['-unlocked_at']
        verbose_name = 'User Badge'
        verbose_name_plural = 'User Badges'
    
    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"


class UserCourseProgress(models.Model):
    """Track user progress through a specific course"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='user_progress')
    
    # Current position in course
    current_item = models.ForeignKey(CourseItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_users')
    completed_items = models.ManyToManyField(CourseItem, blank=True, related_name='completed_by_users')
    
    # Status
    is_started = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    completion_percentage = models.IntegerField(default=0)
    
    # Timestamps
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'course']
        ordering = ['-last_accessed']
        verbose_name = 'User Course Progress'
        verbose_name_plural = 'User Course Progress'
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title} ({self.completion_percentage}%)"
    
    def calculate_progress(self):
        """Calculate and update completion percentage"""
        total_items = self.course.get_total_items()
        if total_items == 0:
            self.completion_percentage = 0
        else:
            completed_count = self.completed_items.count()
            self.completion_percentage = int((completed_count / total_items) * 100)
            
            # Auto-complete course if all items done
            if self.completion_percentage == 100 and not self.is_completed:
                self.is_completed = True
                from django.utils import timezone
                self.completed_at = timezone.now()
        
        self.save()
        return self.completion_percentage

