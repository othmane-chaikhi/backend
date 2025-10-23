from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet, CommentViewSet, ProfileViewSet, SiteConfigViewSet,
    CourseViewSet, CourseItemViewSet,
    AcademyVideoViewSet, AcademyExerciseViewSet, UserProgressViewSet
)

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'site-config', SiteConfigViewSet, basename='site-config')

# Academy routes
router.register(r'academy/courses', CourseViewSet, basename='academy-course')
router.register(r'academy/course-items', CourseItemViewSet, basename='academy-course-item')
router.register(r'academy/videos', AcademyVideoViewSet, basename='academy-video')
router.register(r'academy/exercises', AcademyExerciseViewSet, basename='academy-exercise')
router.register(r'academy/progress', UserProgressViewSet, basename='user-progress')

urlpatterns = [
    path('', include(router.urls)),
]

