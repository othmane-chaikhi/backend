from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from .models import (
    Post, Comment, Profile, SiteConfig, 
    Course, CourseItem, AcademyVideo, AcademyExercise, 
    UserProgress, UserCourseProgress
)
from .serializers import (
    PostListSerializer, PostDetailSerializer, CommentSerializer,
    ProfileSerializer, SiteConfigSerializer,
    CourseListSerializer, CourseDetailSerializer, CourseItemDetailSerializer,
    CourseItemWriteSerializer, UserCourseProgressSerializer,
    AcademyVideoSerializer, AcademyExerciseSerializer, 
    UserProgressSerializer, ExerciseSubmissionSerializer
)
from .permissions import IsAuthorOrReadOnly, IsStaffOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing blog posts.
    List: GET /api/posts/
    Retrieve: GET /api/posts/{id}/
    Create: POST /api/posts/
    Update: PUT/PATCH /api/posts/{id}/
    Delete: DELETE /api/posts/{id}/
    """
    queryset = Post.objects.filter(is_published=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Post.objects.all()
        
        # Show unpublished posts only to staff
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_published=True)
        
        # Filter by search query
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )
        
        return queryset

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent published posts - optimized with select_related"""
        posts = (self.get_queryset()
                .filter(is_published=True)
                .select_related('author')  # Optimize author queries
                .prefetch_related('comments')  # Optimize comments count
                .only('id', 'title', 'content', 'media', 'video_url', 
                      'media_type', 'created_at', 'updated_at', 'is_published',
                      'author__username', 'author__first_name', 'author__last_name')
                .order_by('-created_at')[:3])
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def stats(self, request):
        """Get statistics for admin dashboard"""
        return Response({
            'total_posts': Post.objects.count(),
            'published_posts': Post.objects.filter(is_published=True).count(),
            'total_comments': Comment.objects.count(),
            'pending_comments': Comment.objects.filter(is_approved=False).count(),
        })


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing comments.
    """
    queryset = Comment.objects.filter(is_approved=True)
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    ordering = ['created_at']

    def get_queryset(self):
        queryset = Comment.objects.all()
        
        # Show unapproved comments only to staff
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_approved=True)
        
        # Filter by post
        post_id = self.request.query_params.get('post', None)
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        
        return queryset

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def toggle_approval(self, request, pk=None):
        """Toggle comment approval status"""
        comment = self.get_object()
        comment.is_approved = not comment.is_approved
        comment.save()
        serializer = self.get_serializer(comment)
        return Response(serializer.data)


class ProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user profiles.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """Get or update current user's profile"""
        profile, created = Profile.objects.get_or_create(user=request.user)
        
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class SiteConfigViewSet(viewsets.ModelViewSet):
    """
    ViewSet for site configuration (CV management).
    """
    queryset = SiteConfig.objects.all()
    serializer_class = SiteConfigSerializer
    permission_classes = [IsStaffOrReadOnly]

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current site configuration"""
        config = SiteConfig.get_solo()
        serializer = self.get_serializer(config)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'], permission_classes=[permissions.IsAdminUser])
    def update_cv(self, request):
        """Update CV file"""
        config = SiteConfig.get_solo()
        serializer = self.get_serializer(config, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AcademyVideoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Academy videos.
    """
    queryset = AcademyVideo.objects.filter(is_active=True)
    serializer_class = AcademyVideoSerializer
    permission_classes = [IsStaffOrReadOnly]
    ordering = ['order', '-created_at']
    
    def get_queryset(self):
        queryset = AcademyVideo.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset
    
    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        """Mark video as completed by user"""
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        video = self.get_object()
        progress, created = UserProgress.objects.get_or_create(user=request.user)
        
        if video not in progress.completed_videos.all():
            progress.completed_videos.add(video)
            progress.total_points += 10  # 10 points per video
            progress.save()
            return Response({'message': 'Video marked as completed', 'points': progress.total_points})
        
        return Response({'message': 'Video already completed'})


class AcademyExerciseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Academy exercises.
    """
    queryset = AcademyExercise.objects.filter(is_active=True)
    serializer_class = AcademyExerciseSerializer
    permission_classes = [IsStaffOrReadOnly]
    ordering = ['order', '-created_at']
    
    def get_queryset(self):
        queryset = AcademyExercise.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset
    
    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        """Execute code using Judge0 API - REAL execution for all languages!"""
        from .services.judge0_service import get_judge0_service
        
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        exercise = self.get_object()
        code = request.data.get('code', '')
        stdin = request.data.get('stdin', '')
        
        if not code or len(code.strip()) < 5:
            return Response({
                'success': False,
                'error': 'Code is too short',
                'message': '❌ Please write some code first'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get Judge0 service
        judge0 = get_judge0_service()
        
        # Execute code
        result = judge0.execute_code(
            source_code=code,
            language=exercise.language,
            stdin=stdin
        )
        
        return Response(result)
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit exercise solution for validation using Gemini AI + Judge0"""
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        exercise = self.get_object()
        code = request.data.get('code', '')
        
        # Get user progress
        progress, created = UserProgress.objects.get_or_create(user=request.user)
        
        # Check if exercise is already completed
        is_already_completed = exercise in progress.completed_exercises.all()
        
        # NEW: AI-powered validation with Gemini + Judge0
        validation_result = self._validate_with_ai_and_execution(exercise, code)
        
        # If exercise is already completed, preserve that status
        if is_already_completed:
            if validation_result['is_correct']:
                return Response({
                    'success': True,
                    'message': '✅ Exercice déjà complété - Votre nouvelle réponse est également correcte!',
                    'points': 0,
                    'total_points': progress.total_points,
                    'feedback': 'Vous avez déjà validé cet exercice. Continuez sur le suivant!',
                    'already_completed': True
                })
            else:
                # Return success but indicate the current answer is wrong
                return Response({
                    'success': True,
                    'message': '✅ Exercice déjà complété - Mais votre nouvelle réponse est incorrecte',
                    'points': 0,
                    'total_points': progress.total_points,
                    'feedback': 'Vous avez déjà validé cet exercice avec une bonne réponse. Votre tentative actuelle est incorrecte, mais l\'exercice reste complété.',
                    'hint': validation_result.get('hint', ''),
                    'already_completed': True,
                    'current_answer_incorrect': True
                })
        
        # First time submission
        if validation_result['is_correct']:
            progress.completed_exercises.add(exercise)
            
            # Award points based on difficulty
            points_map = {'easy': 20, 'medium': 30, 'hard': 50}
            points = points_map.get(exercise.difficulty, 20)
            progress.total_points += points
            progress.save()
            
            return Response({
                'success': True,
                'message': validation_result.get('message', 'Excellent! Solution correcte!'),
                'points': points,
                'total_points': progress.total_points,
                'feedback': validation_result.get('feedback', '')
            })
        else:
            return Response({
                'success': False,
                'message': validation_result.get('message', 'Solution incorrecte. Essayez encore!'),
                'hint': validation_result.get('hint', 'Vérifiez la logique de votre code'),
                'feedback': validation_result.get('feedback', '')
            })
    
    def _validate_with_ai_and_execution(self, exercise, submitted_code):
        """
        NEW: Validate solution using Gemini AI + Judge0 execution
        This provides intelligent, context-aware feedback
        """
        from .services.gemini_service import get_gemini_service
        from .services.judge0_service import get_judge0_service
        
        if not submitted_code or len(submitted_code.strip()) < 5:
            return {
                'is_correct': False,
                'message': '❌ Code trop court',
                'hint': 'Veuillez écrire une solution complète',
                'feedback': 'Votre code doit contenir au moins quelques lignes.'
            }
        
        # Step 1: Try to execute code with Judge0 (if supported)
        execution_output = None
        judge0 = get_judge0_service()
        
        has_compilation_error = False
        has_runtime_error = False
        error_message = ""
        
        try:
            result = judge0.execute_code(
                source_code=submitted_code,
                language=exercise.language,
                stdin=''
            )
            
            if result.get('success'):
                execution_output = result.get('stdout', '')
            elif result.get('compile_output'):
                # Compilation error - ALWAYS reject (syntax errors)
                has_compilation_error = True
                error_message = result.get('compile_output', '')
            elif result.get('stderr'):
                # Runtime error - Check if it's a browser API issue
                stderr = result.get('stderr', '')
                error_message = stderr
                
                # For JavaScript: Check if error is due to browser-specific APIs
                if exercise.language.lower() in ['javascript', 'js', 'typescript']:
                    browser_apis = ['alert', 'prompt', 'confirm', 'document', 'window', 'console', 'localStorage']
                    is_browser_api_error = any(api in stderr for api in browser_apis)
                    
                    if is_browser_api_error:
                        # Don't reject yet - let AI evaluate the logic
                        has_runtime_error = True
                        execution_output = f"⚠️ Code utilise des APIs navigateur: {stderr[:100]}"
                    else:
                        # Real runtime error - reject immediately
                        return {
                            'is_correct': False,
                            'message': '❌ Erreur d\'exécution',
                            'hint': 'Vérifiez la logique de votre code',
                            'feedback': f"Erreur: {stderr[:200]}"
                        }
                else:
                    # For other languages, reject on any runtime error
                    has_runtime_error = True
        except Exception as e:
            print(f"Judge0 execution error: {e}")
            # Continue with AI evaluation even if execution fails
        
        # If compilation error, reject immediately
        if has_compilation_error:
            return {
                'is_correct': False,
                'message': '❌ Erreur de compilation',
                'hint': 'Vérifiez la syntaxe de votre code',
                'feedback': f"Erreur: {error_message[:200]}"
            }
        
        # Step 2: Use Gemini AI for intelligent evaluation
        gemini = get_gemini_service()
        
        if gemini.is_available():
            try:
                ai_result = gemini.evaluate_code(
                    submitted_code=submitted_code,
                    solution_code=exercise.solution_code,
                    language=exercise.language,
                    instructions=exercise.instructions,
                    execution_output=execution_output
                )
                
                # Build response from AI evaluation
                return {
                    'is_correct': ai_result['is_correct'],
                    'message': '✅ ' + ai_result['feedback'] if ai_result['is_correct'] else '❌ ' + ai_result['feedback'],
                    'hint': ai_result.get('suggestions', ''),
                    'feedback': ai_result.get('reasoning', '')[:300],  # Limit feedback length
                    'ai_score': ai_result.get('score', 0)
                }
            except Exception as e:
                print(f"Gemini AI error: {e}")
                # Fallback to basic validation
        
        # Step 3: Fallback to basic validation if AI not available
        return self._validate_solution_intelligent(exercise, submitted_code)
    
    def _validate_solution_intelligent(self, exercise, submitted_code):
        """
        Intelligent validation that accepts multiple correct solutions
        """
        if not submitted_code or len(submitted_code.strip()) < 5:
            return {
                'is_correct': False,
                'message': '❌ Code trop court',
                'hint': 'Veuillez écrire une solution complète',
                'feedback': 'Votre code doit contenir au moins quelques lignes.'
            }
        
        language = exercise.language.lower()
        
        # For HTML/CSS: Check if essential elements are present
        if language in ['html', 'css', 'xml']:
            return self._validate_html_css(exercise, submitted_code)
        
        # For JavaScript: Check for key functions/logic
        elif language in ['javascript', 'js', 'typescript']:
            return self._validate_javascript(exercise, submitted_code)
        
        # For Python: Check for key elements
        elif language == 'python':
            return self._validate_python(exercise, submitted_code)
        
        # For C++: Check for C++ patterns
        elif language in ['c++', 'cpp']:
            return self._validate_cpp(exercise, submitted_code)
        
        # For Java: Check for Java patterns
        elif language == 'java':
            return self._validate_java(exercise, submitted_code)
        
        # For C: Check for C patterns
        elif language == 'c':
            return self._validate_c(exercise, submitted_code)
        
        # For SQL: Check for SQL keywords
        elif language == 'sql':
            return self._validate_sql(exercise, submitted_code)
        
        # Default: flexible comparison
        else:
            return self._validate_generic(exercise, submitted_code)
    
    def _validate_html_css(self, exercise, code):
        """Validate HTML/CSS by checking essential elements"""
        code_lower = code.lower()
        solution_lower = exercise.solution_code.lower()
        
        # Extract key tags from solution
        import re
        solution_tags = set(re.findall(r'<(\w+)', solution_lower))
        submitted_tags = set(re.findall(r'<(\w+)', code_lower))
        
        # Check if main tags are present
        missing_tags = solution_tags - submitted_tags
        
        if len(missing_tags) == 0:
            return {
                'is_correct': True,
                'message': '✅ Parfait! Tous les éléments requis sont présents!',
                'feedback': 'Votre structure HTML est correcte.'
            }
        elif len(missing_tags) <= 2:
            return {
                'is_correct': True,
                'message': '✅ Bien! Solution acceptée avec une approche différente.',
                'feedback': f'Note: Vous pourriez aussi utiliser: {", ".join(missing_tags)}'
            }
        else:
            return {
                'is_correct': False,
                'message': 'Il manque des éléments importants',
                'hint': f'Essayez d\'ajouter: {", ".join(list(missing_tags)[:3])}'
            }
    
    def _validate_python(self, exercise, code):
        """Validate Python code"""
        # Check for basic syntax patterns
        has_function = 'def ' in code
        has_logic = any(kw in code for kw in ['if', 'for', 'while', 'return', 'print'])
        has_import = 'import' in code
        
        solution_lower = exercise.solution_code.lower()
        code_lower = code.lower()
        
        solution_has_function = 'def ' in exercise.solution_code
        solution_has_print = 'print' in solution_lower
        solution_has_loop = any(kw in solution_lower for kw in ['for ', 'while '])
        solution_has_conditional = 'if ' in solution_lower
        
        # Clean code lines (remove comments and empty lines)
        code_lines = [line for line in code.strip().split('\n') if line.strip() and not line.strip().startswith('#')]
        
        # Code must have at least 2 meaningful lines
        if len(code_lines) < 2:
            return {
                'is_correct': False,
                'message': '❌ Votre code est trop court',
                'hint': 'Écrivez une solution plus complète (au moins 2 lignes)',
                'feedback': 'Votre code doit contenir au moins quelques lignes de logique.'
            }
        
        # If solution requires a function, code MUST have a function
        if solution_has_function and not has_function:
            return {
                'is_correct': False,
                'message': '❌ Votre code doit contenir une fonction',
                'hint': 'La solution attendue utilise une fonction. Utilisez def nom_fonction():',
                'feedback': 'Définissez une fonction avec def.'
            }
        
        # If solution requires a loop, code should have a loop
        if solution_has_loop:
            has_loop = any(kw in code_lower for kw in ['for ', 'while '])
            if not has_loop:
                return {
                    'is_correct': False,
                    'message': '❌ Votre code doit contenir une boucle',
                    'hint': 'Utilisez for ou while pour créer une boucle',
                    'feedback': 'La solution attendue utilise une boucle.'
                }
        
        # If solution requires conditional, code should have conditional
        if solution_has_conditional:
            if 'if ' not in code_lower:
                return {
                    'is_correct': False,
                    'message': '❌ Votre code doit contenir une condition',
                    'hint': 'Utilisez if pour ajouter une logique conditionnelle',
                    'feedback': 'La solution attendue utilise une condition if.'
                }
        
        # If solution has print, code should have print
        if solution_has_print:
            if 'print' not in code_lower:
                return {
                    'is_correct': False,
                    'message': '❌ Votre code doit afficher quelque chose',
                    'hint': 'Utilisez print() pour afficher le résultat',
                    'feedback': 'La solution attendue utilise print().'
                }
        
        # Accept if code has meaningful logic and required elements
        if has_logic and len(code_lines) >= 2:
            return {
                'is_correct': True,
                'message': '✅ Excellent! Votre solution Python est valide!',
                'feedback': 'Votre code semble correct et bien structuré.'
            }
        
        return {
            'is_correct': False,
            'message': '❌ La solution semble incomplète',
            'hint': 'Vérifiez que vous avez implémenté toute la logique nécessaire',
            'feedback': 'Essayez d\'ajouter plus de code ou de logique.'
        }
    
    def _validate_javascript(self, exercise, code):
        """Validate JavaScript code - accepts browser APIs"""
        import re
        
        # Extract key elements from solution
        solution_lower = exercise.solution_code.lower()
        code_lower = code.lower()
        
        # Check for common JS patterns (including browser APIs)
        has_function = any(kw in code for kw in ['function', '=>', 'const', 'let', 'var'])
        has_logic = any(kw in code for kw in ['if', 'for', 'while', 'return', 'console.log', 'alert', 'prompt'])
        has_array_methods = any(method in code for method in ['.map', '.filter', '.reduce', '.forEach'])
        
        solution_has_function = any(kw in exercise.solution_code for kw in ['function', '=>'])
        solution_has_loop = any(kw in solution_lower for kw in ['for', 'while', '.map', '.foreach'])
        solution_has_conditional = 'if' in solution_lower
        
        # Check if code uses browser APIs (which is valid)
        uses_browser_apis = any(api in code_lower for api in ['alert', 'prompt', 'confirm', 'document.', 'window.'])
        
        code_lines = [line for line in code.strip().split('\n') if line.strip() and not line.strip().startswith('//')]
        
        # If solution requires a function, code MUST have a function
        if solution_has_function and not has_function:
            return {
                'is_correct': False,
                'message': '❌ Votre code doit contenir une fonction',
                'hint': 'La solution attendue utilise une fonction. Définissez une fonction.',
                'feedback': 'Utilisez function ou => pour créer une fonction.'
            }
        
        # If solution requires a loop, code should have a loop or array method
        if solution_has_loop:
            has_loop = any(kw in code_lower for kw in ['for', 'while', '.map', '.foreach', '.filter', '.reduce'])
            if not has_loop:
                return {
                    'is_correct': False,
                    'message': '❌ Votre code doit contenir une boucle ou une méthode de tableau',
                    'hint': 'Utilisez for, while, ou une méthode comme .map(), .forEach()',
                    'feedback': 'La solution attendue utilise une itération.'
                }
        
        # If solution requires conditional, code should have conditional
        if solution_has_conditional:
            if 'if' not in code_lower:
                return {
                    'is_correct': False,
                    'message': '❌ Votre code doit contenir une condition',
                    'hint': 'Utilisez if pour ajouter une logique conditionnelle',
                    'feedback': 'La solution attendue utilise une condition if.'
                }
        
        # Code must have meaningful content
        if len(code_lines) < 2:
            return {
                'is_correct': False,
                'message': '❌ Votre code est trop court',
                'hint': 'Écrivez une solution plus complète',
                'feedback': 'Votre code doit contenir au moins quelques lignes de logique.'
            }
        
        # If all required elements are present
        if (has_function or has_logic or has_array_methods) and len(code_lines) >= 2:
            feedback_msg = 'Votre code JavaScript semble correct et bien structuré.'
            if uses_browser_apis:
                feedback_msg += ' ⚠️ Note: Utilise des APIs navigateur (alert, prompt, etc.) - normal pour du code client.'
            
            return {
                'is_correct': True,
                'message': '✅ Excellent! Votre solution JavaScript est valide!',
                'feedback': feedback_msg
            }
        
        return {
            'is_correct': False,
            'message': '❌ La solution JavaScript semble incomplète',
            'hint': 'Vérifiez que vous avez implémenté toute la logique nécessaire',
            'feedback': 'Essayez d\'ajouter plus de code ou de logique.'
        }
    
    def _validate_cpp(self, exercise, code):
        """Validate C++ code"""
        # Check for C++ patterns
        has_includes = '#include' in code
        has_main = 'int main' in code
        has_namespace = 'using namespace std' in code or 'std::' in code
        has_logic = any(kw in code for kw in ['if', 'for', 'while', 'return', 'cout', 'cin'])
        
        solution_lower = exercise.solution_code.lower()
        
        solution_has_main = 'int main' in solution_lower
        solution_has_cout = 'cout' in solution_lower
        solution_has_loop = any(kw in solution_lower for kw in ['for', 'while'])
        
        code_lines = [line for line in code.strip().split('\n') if line.strip() and not line.strip().startswith('//')]
        
        # Code must have at least 3 lines (include, main, logic)
        if len(code_lines) < 3:
            return {
                'is_correct': False,
                'message': '❌ Votre code est trop court',
                'hint': 'Un programme C++ nécessite au moins #include, main, et de la logique',
                'feedback': 'Écrivez un programme C++ complet.'
            }
        
        # Must have includes
        if not has_includes:
            return {
                'is_correct': False,
                'message': '❌ Votre code doit inclure des headers',
                'hint': 'Ajoutez #include <iostream> ou d\'autres headers nécessaires',
                'feedback': 'Les programmes C++ commencent par des #include.'
            }
        
        # If solution has main, code must have main
        if solution_has_main and not has_main:
            return {
                'is_correct': False,
                'message': '❌ Votre code doit contenir la fonction main',
                'hint': 'Ajoutez int main() { ... }',
                'feedback': 'La fonction main est le point d\'entrée du programme.'
            }
        
        # If solution has cout, code should have cout
        if solution_has_cout and 'cout' not in code.lower():
            return {
                'is_correct': False,
                'message': '❌ Votre code doit afficher quelque chose',
                'hint': 'Utilisez cout << pour afficher le résultat',
                'feedback': 'La solution attendue utilise cout.'
            }
        
        # If solution has loop, code should have loop
        if solution_has_loop:
            if not any(kw in code.lower() for kw in ['for', 'while']):
                return {
                    'is_correct': False,
                    'message': '❌ Votre code doit contenir une boucle',
                    'hint': 'Utilisez for ou while',
                    'feedback': 'La solution attendue utilise une boucle.'
                }
        
        # All required elements must be present
        # Only accept if code has includes, main, and all solution-required elements
        all_requirements_met = (
            has_includes and 
            (not solution_has_main or has_main) and
            (not solution_has_cout or 'cout' in code.lower()) and
            (not solution_has_loop or any(kw in code.lower() for kw in ['for', 'while'])) and
            len(code_lines) >= 3
        )
        
        if all_requirements_met:
            return {
                'is_correct': True,
                'message': '✅ Excellent! Votre solution C++ est valide!',
                'feedback': 'Votre code C++ semble correct et bien structuré.'
            }
        
        return {
            'is_correct': False,
            'message': '❌ La solution C++ semble incomplète',
            'hint': 'Vérifiez que vous avez inclus les headers nécessaires et implémenté la logique',
            'feedback': 'Essayez d\'ajouter les includes et la fonction main.'
        }
    
    def _validate_java(self, exercise, code):
        """Validate Java code"""
        # Check for Java patterns
        has_class = 'class' in code
        has_main = 'public static void main' in code
        has_method = 'public' in code or 'private' in code or 'protected' in code
        has_logic = any(kw in code for kw in ['if', 'for', 'while', 'return', 'System.out'])
        
        solution_lower = exercise.solution_code.lower()
        
        solution_has_main = 'public static void main' in solution_lower
        solution_has_sysout = 'system.out' in solution_lower
        solution_has_loop = any(kw in solution_lower for kw in ['for', 'while'])
        
        code_lines = [line for line in code.strip().split('\n') if line.strip() and not line.strip().startswith('//')]
        
        # Code must have at least 3 lines
        if len(code_lines) < 3:
            return {
                'is_correct': False,
                'message': '❌ Votre code est trop court',
                'hint': 'Un programme Java nécessite au moins une classe, une méthode, et de la logique',
                'feedback': 'Écrivez un programme Java complet.'
            }
        
        # Must have a class
        if not has_class:
            return {
                'is_correct': False,
                'message': '❌ Votre code doit contenir une classe',
                'hint': 'Ajoutez public class NomClasse { ... }',
                'feedback': 'Les programmes Java doivent être dans une classe.'
            }
        
        # If solution has main, code must have main
        if solution_has_main and not has_main:
            return {
                'is_correct': False,
                'message': '❌ Votre code doit contenir la méthode main',
                'hint': 'Ajoutez public static void main(String[] args) { ... }',
                'feedback': 'La méthode main est le point d\'entrée du programme.'
            }
        
        # If solution has System.out, code should have it
        if solution_has_sysout and 'system.out' not in code.lower():
            return {
                'is_correct': False,
                'message': '❌ Votre code doit afficher quelque chose',
                'hint': 'Utilisez System.out.println() pour afficher le résultat',
                'feedback': 'La solution attendue utilise System.out.'
            }
        
        # If solution has loop, code should have loop
        if solution_has_loop:
            if not any(kw in code.lower() for kw in ['for', 'while']):
                return {
                    'is_correct': False,
                    'message': '❌ Votre code doit contenir une boucle',
                    'hint': 'Utilisez for ou while',
                    'feedback': 'La solution attendue utilise une boucle.'
                }
        
        # All required elements must be present
        all_requirements_met = (
            has_class and
            (not solution_has_main or has_main) and
            (not solution_has_sysout or 'system.out' in code.lower()) and
            (not solution_has_loop or any(kw in code.lower() for kw in ['for', 'while'])) and
            len(code_lines) >= 3
        )
        
        if all_requirements_met:
            return {
                'is_correct': True,
                'message': '✅ Excellent! Votre solution Java est valide!',
                'feedback': 'Votre code Java semble correct et bien structuré.'
            }
        
        return {
            'is_correct': False,
            'message': '❌ La solution Java semble incomplète',
            'hint': 'Vérifiez que vous avez créé une classe et implémenté la logique',
            'feedback': 'Essayez d\'ajouter une classe et des méthodes.'
        }
    
    def _validate_c(self, exercise, code):
        """Validate C code"""
        # Check for C patterns
        has_includes = '#include' in code
        has_main = 'int main' in code
        has_logic = any(kw in code for kw in ['if', 'for', 'while', 'return', 'printf', 'scanf'])
        
        solution_lower = exercise.solution_code.lower()
        
        solution_has_main = 'int main' in solution_lower
        solution_has_printf = 'printf' in solution_lower
        solution_has_loop = any(kw in solution_lower for kw in ['for', 'while'])
        
        code_lines = [line for line in code.strip().split('\n') if line.strip() and not line.strip().startswith('//')]
        
        # Code must have at least 3 lines
        if len(code_lines) < 3:
            return {
                'is_correct': False,
                'message': '❌ Votre code est trop court',
                'hint': 'Un programme C nécessite au moins #include, main, et de la logique',
                'feedback': 'Écrivez un programme C complet.'
            }
        
        # Must have includes
        if not has_includes:
            return {
                'is_correct': False,
                'message': '❌ Votre code doit inclure des headers',
                'hint': 'Ajoutez #include <stdio.h> ou d\'autres headers nécessaires',
                'feedback': 'Les programmes C commencent par des #include.'
            }
        
        # If solution has main, code must have main
        if solution_has_main and not has_main:
            return {
                'is_correct': False,
                'message': '❌ Votre code doit contenir la fonction main',
                'hint': 'Ajoutez int main() { ... }',
                'feedback': 'La fonction main est le point d\'entrée du programme.'
            }
        
        # If solution has printf, code should have printf
        if solution_has_printf and 'printf' not in code.lower():
            return {
                'is_correct': False,
                'message': '❌ Votre code doit afficher quelque chose',
                'hint': 'Utilisez printf() pour afficher le résultat',
                'feedback': 'La solution attendue utilise printf().'
            }
        
        # If solution has loop, code should have loop
        if solution_has_loop:
            if not any(kw in code.lower() for kw in ['for', 'while']):
                return {
                    'is_correct': False,
                    'message': '❌ Votre code doit contenir une boucle',
                    'hint': 'Utilisez for ou while',
                    'feedback': 'La solution attendue utilise une boucle.'
                }
        
        # All required elements must be present
        all_requirements_met = (
            has_includes and
            (not solution_has_main or has_main) and
            (not solution_has_printf or 'printf' in code.lower()) and
            (not solution_has_loop or any(kw in code.lower() for kw in ['for', 'while'])) and
            len(code_lines) >= 3
        )
        
        if all_requirements_met:
            return {
                'is_correct': True,
                'message': '✅ Excellent! Votre solution C est valide!',
                'feedback': 'Votre code C semble correct et bien structuré.'
            }
        
        return {
            'is_correct': False,
            'message': '❌ La solution C semble incomplète',
            'hint': 'Vérifiez que vous avez inclus les headers nécessaires et implémenté la logique',
            'feedback': 'Essayez d\'ajouter les includes et la fonction main.'
        }
    
    def _validate_sql(self, exercise, code):
        """Validate SQL code"""
        # Check for SQL patterns
        code_upper = code.upper()
        solution_upper = exercise.solution_code.upper()
        
        has_select = 'SELECT' in code_upper
        has_from = 'FROM' in code_upper
        has_where = 'WHERE' in code_upper
        has_insert = 'INSERT' in code_upper
        has_update = 'UPDATE' in code_upper
        has_delete = 'DELETE' in code_upper
        has_create = 'CREATE' in code_upper
        has_join = 'JOIN' in code_upper
        
        solution_has_select = 'SELECT' in solution_upper
        solution_has_insert = 'INSERT' in solution_upper
        solution_has_update = 'UPDATE' in solution_upper
        solution_has_delete = 'DELETE' in solution_upper
        solution_has_create = 'CREATE' in solution_upper
        solution_has_where = 'WHERE' in solution_upper
        solution_has_join = 'JOIN' in solution_upper
        
        # Flexible validation for SQL
        has_sql_keyword = any([has_select, has_insert, has_update, has_delete, has_create])
        
        # Must have at least one SQL keyword
        if not has_sql_keyword:
            return {
                'is_correct': False,
                'message': '❌ Votre code doit contenir une requête SQL',
                'hint': 'Utilisez SELECT, INSERT, UPDATE, DELETE, ou CREATE',
                'feedback': 'Écrivez une requête SQL valide.'
            }
        
        # If solution uses SELECT, code must use SELECT
        if solution_has_select and not has_select:
            return {
                'is_correct': False,
                'message': '❌ Votre requête doit utiliser SELECT',
                'hint': 'La solution attendue utilise SELECT',
                'feedback': 'Utilisez SELECT pour interroger les données.'
            }
        
        # If solution has FROM and code has SELECT, code must have FROM
        if solution_has_select and has_select and 'FROM' in solution_upper and not has_from:
            return {
                'is_correct': False,
                'message': '❌ Votre requête SELECT doit inclure FROM',
                'hint': 'Spécifiez la table avec FROM nom_table',
                'feedback': 'SELECT nécessite FROM pour spécifier la source.'
            }
        
        # If solution has WHERE, code should have WHERE
        if solution_has_where and not has_where:
            return {
                'is_correct': False,
                'message': '❌ Votre requête doit inclure une clause WHERE',
                'hint': 'Ajoutez WHERE pour filtrer les résultats',
                'feedback': 'La solution attendue utilise WHERE.'
            }
        
        # If solution has JOIN, code should have JOIN
        if solution_has_join and not has_join:
            return {
                'is_correct': False,
                'message': '❌ Votre requête doit inclure un JOIN',
                'hint': 'Utilisez JOIN pour combiner des tables',
                'feedback': 'La solution attendue utilise JOIN.'
            }
        
        # All required elements must be present
        all_requirements_met = (
            has_sql_keyword and
            (not solution_has_select or has_select) and
            (not solution_has_where or has_where) and
            (not solution_has_join or has_join) and
            (not (solution_has_select and 'FROM' in solution_upper) or has_from) and
            len(code.strip()) > 10
        )
        
        if all_requirements_met:
            return {
                'is_correct': True,
                'message': '✅ Excellent! Votre requête SQL est valide!',
                'feedback': 'Votre requête SQL semble correcte.'
            }
        
        return {
            'is_correct': False,
            'message': '❌ La requête SQL semble incomplète',
            'hint': 'Vérifiez que vous avez utilisé les bons mots-clés SQL (SELECT, FROM, WHERE, etc.)',
            'feedback': 'Essayez d\'écrire une requête SQL complète.'
        }
    
    def _validate_generic(self, exercise, code):
        """Generic validation for other languages"""
        # More strict comparison
        submitted_clean = ''.join(code.split()).lower()
        solution_clean = ''.join(exercise.solution_code.split()).lower()
        
        # Code must have minimum length
        if len(submitted_clean) < 15:
            return {
                'is_correct': False,
                'message': '❌ Votre code est trop court',
                'hint': 'Écrivez une solution plus complète',
                'feedback': 'Votre code doit contenir au moins quelques lignes.'
            }
        
        # Calculate simple similarity
        common_chars = sum(1 for a, b in zip(submitted_clean, solution_clean) if a == b)
        similarity = common_chars / max(len(solution_clean), 1)
        
        # Much stricter: need at least 70% similarity
        if similarity > 0.7:
            return {
                'is_correct': True,
                'message': '✅ Solution acceptée!',
                'feedback': 'Votre approche semble valide.'
            }
        elif similarity > 0.5:
            return {
                'is_correct': False,
                'message': '❌ Votre solution est proche mais pas tout à fait correcte',
                'hint': 'Vérifiez bien la logique et comparez avec les instructions',
                'feedback': f'Similarité: {int(similarity*100)}%. Essayez encore!'
            }
        
        return {
            'is_correct': False,
            'message': '❌ Essayez encore',
            'hint': 'Relisez les instructions et comparez avec l\'exemple',
            'feedback': 'Votre solution semble très différente de ce qui est attendu.'
        }
    
    @action(detail=True, methods=['get'])
    def solution(self, request, pk=None):
        """Get exercise solution (authenticated users)"""
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        exercise = self.get_object()
        return Response({
            'solution': exercise.solution_code,
            'title': exercise.title,
            'language': exercise.language
        })


class UserProgressViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for user progress tracking.
    """
    serializer_class = UserProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserProgress.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's progress"""
        progress, created = UserProgress.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(progress)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get detailed statistics"""
        progress, created = UserProgress.objects.get_or_create(user=request.user)
        
        return Response({
            'total_points': progress.total_points,
            'streak_days': progress.streak_days,
            'completed_videos': progress.completed_videos.count(),
            'completed_exercises': progress.completed_exercises.count(),
            'total_videos': AcademyVideo.objects.filter(is_active=True).count(),
            'total_exercises': AcademyExercise.objects.filter(is_active=True).count(),
            'completion_percentage': self._calculate_completion(progress),
            'last_activity': progress.last_activity
        })
    
    def _calculate_completion(self, progress):
        """Calculate overall completion percentage"""
        total_content = AcademyVideo.objects.filter(is_active=True).count() + \
                       AcademyExercise.objects.filter(is_active=True).count()
        
        if total_content == 0:
            return 0
        
        completed = progress.completed_videos.count() + progress.completed_exercises.count()
        return round((completed / total_content) * 100, 1)


# ===== COURSE VIEWSETS =====

class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for courses (series).
    List: GET /api/academy/courses/
    Retrieve: GET /api/academy/courses/{id}/
    Create: POST /api/academy/courses/ (staff only)
    Update: PUT/PATCH /api/academy/courses/{id}/ (staff only)
    Delete: DELETE /api/academy/courses/{id}/ (staff only)
    """
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['order', 'created_at']
    ordering = ['order', '-created_at']
    
    def get_permissions(self):
        """Allow read for authenticated, write for staff"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseListSerializer
    
    def get_queryset(self):
        queryset = Course.objects.prefetch_related('items').all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Start a course (create progress tracking)"""
        course = self.get_object()
        
        # Get or create progress
        progress, created = UserCourseProgress.objects.get_or_create(
            user=request.user,
            course=course
        )
        
        if created or not progress.is_started:
            progress.is_started = True
            progress.started_at = timezone.now()
            
            # Set current item to first item
            first_item = course.items.order_by('order').first()
            if first_item:
                progress.current_item = first_item
            
            progress.save()
        
        serializer = UserCourseProgressSerializer(progress)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        """Get user's progress for this course"""
        course = self.get_object()
        
        try:
            progress = UserCourseProgress.objects.get(user=request.user, course=course)
            serializer = UserCourseProgressSerializer(progress)
            return Response(serializer.data)
        except UserCourseProgress.DoesNotExist:
            return Response({
                'message': 'Course not started',
                'is_started': False
            }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def complete_item(self, request, pk=None):
        """Mark a course item as completed and move to next"""
        course = self.get_object()
        item_id = request.data.get('item_id')
        
        if not item_id:
            return Response({'error': 'item_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            item = CourseItem.objects.get(id=item_id, course=course)
        except CourseItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get or create progress
        progress, created = UserCourseProgress.objects.get_or_create(
            user=request.user,
            course=course
        )
        
        if created:
            progress.is_started = True
            progress.started_at = timezone.now()
        
        # Mark item as completed
        if item not in progress.completed_items.all():
            progress.completed_items.add(item)
            
            # Award XP based on content type
            user_progress, _ = UserProgress.objects.get_or_create(user=request.user)
            if item.content_type == 'video':
                xp = 10
            else:  # exercise
                xp = 50
            user_progress.add_xp(xp)
            user_progress.check_streak()
        
        # Update progress percentage
        progress.calculate_progress()
        
        # Move to next item
        next_item = item.get_next_item()
        if next_item:
            progress.current_item = next_item
            progress.save()
            
            return Response({
                'message': 'Item completed!',
                'next_item': {
                    'id': next_item.id,
                    'order': next_item.order,
                    'content_type': next_item.content_type
                },
                'completion_percentage': progress.completion_percentage,
                'is_completed': progress.is_completed
            })
        else:
            # Course completed!
            return Response({
                'message': 'Félicitations! Cours complété!',
                'next_item': None,
                'completion_percentage': 100,
                'is_completed': True
            })


class CourseItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for course items (individual content in a course).
    GET /api/academy/course-items/{id}/
    Create: POST /api/academy/course-items/ (staff only)
    Update: PUT/PATCH /api/academy/course-items/{id}/ (staff only)
    Delete: DELETE /api/academy/course-items/{id}/ (staff only)
    """
    queryset = CourseItem.objects.select_related('course', 'video', 'exercise').all()
    
    def get_serializer_class(self):
        """Use write serializer for create/update, detail for read"""
        if self.action in ['create', 'update', 'partial_update']:
            return CourseItemWriteSerializer
        return CourseItemDetailSerializer
    
    def get_permissions(self):
        """Allow read for authenticated, write for staff"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
    
    @action(detail=True, methods=['get'])
    def navigation(self, request, pk=None):
        """Get navigation info (previous, current, next)"""
        item = self.get_object()
        
        return Response({
            'current': {
                'id': item.id,
                'order': item.order,
                'content_type': item.content_type,
                'title': item.get_content().title if item.get_content() else None
            },
            'previous': {
                'id': item.get_previous_item().id,
                'order': item.get_previous_item().order
            } if item.get_previous_item() else None,
            'next': {
                'id': item.get_next_item().id,
                'order': item.get_next_item().order
            } if item.get_next_item() else None,
            'course_progress': self._get_course_progress(item.course)
        })
    
    def _get_course_progress(self, course):
        """Helper to get course progress"""
        try:
            progress = UserCourseProgress.objects.get(user=self.request.user, course=course)
            return {
                'completion_percentage': progress.completion_percentage,
                'current_item_order': progress.current_item.order if progress.current_item else None
            }
        except UserCourseProgress.DoesNotExist:
            return None

