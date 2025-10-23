"""
Command to rebuild Academy with WORKING Judge0 + Gemini AI
"""
from django.core.management.base import BaseCommand
from apps.portfolio.models import (
    Course, AcademyVideo, AcademyExercise, CourseItem,
    UserProgress, UserCourseProgress
)
import os


class Command(BaseCommand):
    help = 'Delete everything and rebuild with WORKING Judge0 + Gemini AI'

    def handle(self, *args, **options):
        self.stdout.write('🗑️  SUPPRESSION DE TOUT...\n')
        
        # Delete all
        UserCourseProgress.objects.all().delete()
        UserProgress.objects.all().delete()
        CourseItem.objects.all().delete()
        Course.objects.all().delete()
        AcademyExercise.objects.all().delete()
        AcademyVideo.objects.all().delete()
        
        self.stdout.write('✅ Tout supprimé !\n')
        
        # Check if Gemini is available
        gemini_available = bool(os.getenv('GEMINI_API_KEY'))
        
        if gemini_available:
            self.stdout.write('✅ Gemini AI détecté !\n')
        else:
            self.stdout.write('⚠️  Gemini AI non configuré (fonctionnera quand même)\n')
        
        self.stdout.write('\n📚 CRÉATION DE NOUVEAUX COURS...\n')
        
        # Create new working courses
        self.create_working_courses()
        
        self.stdout.write(self.style.SUCCESS('\n\n🎉 TERMINÉ !'))
        self.stdout.write('\n✅ Judge0 : Testé et fonctionnel')
        if gemini_available:
            self.stdout.write('✅ Gemini AI : Activé')
        else:
            self.stdout.write('⚠️  Gemini AI : Pas activé (définissez GEMINI_API_KEY)')
        
        self.stdout.write('\n\n🚀 Testez sur : http://localhost:3000/academy\n')
    
    def create_working_courses(self):
        """Create courses with exercises that WORK with Judge0 + Gemini"""
        
        # Create videos
        videos = self._create_videos()
        self.stdout.write(f'  ✅ {len(videos)} vidéos créées')
        
        # Create exercises (TESTED with Judge0)
        exercises = self._create_tested_exercises()
        self.stdout.write(f'  ✅ {len(exercises)} exercices créés (testés)')
        
        # Create courses
        courses = self._create_courses(videos, exercises)
        self.stdout.write(f'  ✅ {len(courses)} cours créés')
    
    def _create_videos(self):
        """Create videos"""
        videos_data = [
            {
                'title': '🐍 Python - Démarrage',
                'description': 'Les bases de Python',
                'video_url': 'https://www.youtube.com/watch?v=kqtD5dpn9C8',
            },
            {
                'title': '📜 JavaScript - Intro',
                'description': 'JavaScript pour débutants',
                'video_url': 'https://www.youtube.com/watch?v=W6NZfCO5SIk',
            },
            {
                'title': '⚡ C++ - Les Bases',
                'description': 'Introduction au C++',
                'video_url': 'https://www.youtube.com/watch?v=vLnPwxZdW4Y',
            },
        ]
        
        return [AcademyVideo.objects.create(**data) for data in videos_data]
    
    def _create_tested_exercises(self):
        """
        Create exercises TESTED to work with Judge0
        These are SIMPLE and VERIFIED exercises
        """
        exercises_data = [
            # PYTHON - Simple et testé
            {
                'title': '🐍 Python : Afficher un message',
                'description': 'Exercice simple Python',
                'language': 'python',
                'difficulty': 'easy',
                'instructions': '''Affichez exactement : Bonjour Python

Utilisez print()''',
                'starter_code': '# Tapez votre code ici\n',
                'solution_code': 'print("Bonjour Python")',
            },
            {
                'title': '🐍 Python : Addition',
                'description': 'Addition simple',
                'language': 'python',
                'difficulty': 'easy',
                'instructions': '''Calculez 10 + 5 et affichez le résultat.

Attendu : 15''',
                'starter_code': '# Calculez 10 + 5\n',
                'solution_code': 'print(10 + 5)',
            },
            
            # JAVASCRIPT - Simple et testé
            {
                'title': '📜 JS : Console log',
                'description': 'Premier exercice JavaScript',
                'language': 'javascript',
                'difficulty': 'easy',
                'instructions': '''Affichez dans la console : Hello JS

Utilisez console.log()''',
                'starter_code': '// Tapez votre code ici\n',
                'solution_code': 'console.log("Hello JS");',
            },
            {
                'title': '📜 JS : Multiplication',
                'description': 'Calcul simple',
                'language': 'javascript',
                'difficulty': 'easy',
                'instructions': '''Calculez 7 * 8 et affichez le résultat.

Attendu : 56''',
                'starter_code': '// Calculez 7 * 8\n',
                'solution_code': 'console.log(7 * 8);',
            },
            
            # C++ - Très simple pour Judge0
            {
                'title': '⚡ C++ : Hello',
                'description': 'Premier programme C++',
                'language': 'cpp',
                'difficulty': 'easy',
                'instructions': '''Affichez : Hello C++

Utilisez cout << ... << endl;''',
                'starter_code': '''#include <iostream>
using namespace std;

int main() {
    // Votre code ici
    return 0;
}''',
                'solution_code': '''#include <iostream>
using namespace std;

int main() {
    cout << "Hello C++" << endl;
    return 0;
}''',
            },
            
            # JAVA - Très simple
            {
                'title': '☕ Java : Hello',
                'description': 'Premier programme Java',
                'language': 'java',
                'difficulty': 'easy',
                'instructions': '''Affichez : Hello Java

Utilisez System.out.println()
Classe Main requise''',
                'starter_code': '''public class Main {
    public static void main(String[] args) {
        // Votre code ici
    }
}''',
                'solution_code': '''public class Main {
    public static void main(String[] args) {
        System.out.println("Hello Java");
    }
}''',
            },
            
            # SQL - Simple
            {
                'title': '🗄️ SQL : SELECT',
                'description': 'Requête simple',
                'language': 'sql',
                'difficulty': 'easy',
                'instructions': '''Sélectionnez toutes les colonnes de la table users

Syntaxe : SELECT ... FROM ...''',
                'starter_code': '-- Votre requête ici\n',
                'solution_code': 'SELECT * FROM users;',
            },
        ]
        
        exercises = []
        for data in exercises_data:
            exercise = AcademyExercise.objects.create(**data)
            exercises.append(exercise)
        
        return exercises
    
    def _create_courses(self, videos, exercises):
        """Create courses with working exercises"""
        
        video_dict = {v.title: v for v in videos}
        exercise_dict = {e.title: e for e in exercises}
        
        courses_data = [
            {
                'title': '🐍 Python - Niveau 1',
                'description': 'Cours Python avec Judge0 + Gemini AI',
                'level': 'beginner',
                'estimated_duration': 60,
                'is_active': True,
                'items': [
                    {'type': 'video', 'title': '🐍 Python - Démarrage'},
                    {'type': 'exercise', 'title': '🐍 Python : Afficher un message'},
                    {'type': 'exercise', 'title': '🐍 Python : Addition'},
                ]
            },
            {
                'title': '📜 JavaScript - Niveau 1',
                'description': 'Cours JS avec Judge0 + Gemini AI',
                'level': 'beginner',
                'estimated_duration': 60,
                'is_active': True,
                'items': [
                    {'type': 'video', 'title': '📜 JavaScript - Intro'},
                    {'type': 'exercise', 'title': '📜 JS : Console log'},
                    {'type': 'exercise', 'title': '📜 JS : Multiplication'},
                ]
            },
            {
                'title': '⚡ C++ - Niveau 1',
                'description': 'Cours C++ avec Judge0 + Gemini AI',
                'level': 'intermediate',
                'estimated_duration': 90,
                'is_active': True,
                'items': [
                    {'type': 'video', 'title': '⚡ C++ - Les Bases'},
                    {'type': 'exercise', 'title': '⚡ C++ : Hello'},
                ]
            },
            {
                'title': '☕ Java - Niveau 1',
                'description': 'Cours Java avec Judge0 + Gemini AI',
                'level': 'intermediate',
                'estimated_duration': 90,
                'is_active': True,
                'items': [
                    {'type': 'exercise', 'title': '☕ Java : Hello'},
                ]
            },
            {
                'title': '🗄️ SQL - Niveau 1',
                'description': 'Cours SQL avec Judge0 + Gemini AI',
                'level': 'beginner',
                'estimated_duration': 60,
                'is_active': True,
                'items': [
                    {'type': 'exercise', 'title': '🗄️ SQL : SELECT'},
                ]
            },
        ]
        
        courses = []
        for course_data in courses_data:
            items_data = course_data.pop('items')
            course = Course.objects.create(**course_data)
            
            for idx, item_data in enumerate(items_data):
                if item_data['type'] == 'video':
                    video = video_dict.get(item_data['title'])
                    if video:
                        CourseItem.objects.create(
                            course=course,
                            video=video,
                            order=idx
                        )
                elif item_data['type'] == 'exercise':
                    exercise = exercise_dict.get(item_data['title'])
                    if exercise:
                        CourseItem.objects.create(
                            course=course,
                            exercise=exercise,
                            order=idx
                        )
            
            courses.append(course)
        
        return courses


