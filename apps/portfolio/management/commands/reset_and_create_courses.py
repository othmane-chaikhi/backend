"""
Command to reset Academy data and create fresh test courses
"""
from django.core.management.base import BaseCommand
from apps.portfolio.models import (
    Course, AcademyVideo, AcademyExercise, CourseItem,
    UserProgress, UserCourseProgress
)


class Command(BaseCommand):
    help = 'Delete all old courses and create fresh new ones for testing'

    def handle(self, *args, **options):
        self.stdout.write('🗑️  NETTOYAGE DE LA BASE DE DONNÉES...\n')
        
        # Delete all old data
        self.delete_old_data()
        
        self.stdout.write('\n✅ Nettoyage terminé !\n')
        self.stdout.write('📚 CRÉATION DE NOUVEAUX COURS...\n\n')
        
        # Create fresh new courses
        self.create_fresh_courses()
        
        self.stdout.write(self.style.SUCCESS('\n\n🎉 TOUT EST PRÊT !'))
        self.stdout.write(self.style.SUCCESS('\nAllez sur : http://localhost:3000/academy'))
    
    def delete_old_data(self):
        """Delete all existing Academy data"""
        # Delete in correct order to avoid foreign key issues
        
        self.stdout.write('  • Suppression des progressions utilisateurs...')
        UserCourseProgress.objects.all().delete()
        UserProgress.objects.all().delete()
        
        self.stdout.write('  • Suppression des items de cours...')
        CourseItem.objects.all().delete()
        
        self.stdout.write('  • Suppression des cours...')
        Course.objects.all().delete()
        
        self.stdout.write('  • Suppression des exercices...')
        AcademyExercise.objects.all().delete()
        
        self.stdout.write('  • Suppression des vidéos...')
        AcademyVideo.objects.all().delete()
    
    def create_fresh_courses(self):
        """Create brand new courses with videos and exercises"""
        
        # 1. Create videos
        videos = self._create_videos()
        self.stdout.write(f'✅ {len(videos)} vidéos créées')
        
        # 2. Create exercises
        exercises = self._create_exercises()
        self.stdout.write(f'✅ {len(exercises)} exercices créés')
        
        # 3. Create courses
        courses = self._create_courses(videos, exercises)
        self.stdout.write(f'✅ {len(courses)} cours créés')
    
    def _create_videos(self):
        """Create test videos"""
        videos_data = [
            # Python
            {
                'title': '🐍 Introduction à Python',
                'description': 'Apprenez les bases de Python : variables, boucles, fonctions',
                'video_url': 'https://www.youtube.com/watch?v=kqtD5dpn9C8',
            },
            {
                'title': '🐍 Python : Listes et Dictionnaires',
                'description': 'Maîtrisez les structures de données en Python',
                'video_url': 'https://www.youtube.com/watch?v=kqtD5dpn9C8',
            },
            # JavaScript
            {
                'title': '📜 JavaScript pour Débutants',
                'description': 'Les fondamentaux de JavaScript',
                'video_url': 'https://www.youtube.com/watch?v=W6NZfCO5SIk',
            },
            {
                'title': '📜 JavaScript : Fonctions',
                'description': 'Tout sur les fonctions en JavaScript',
                'video_url': 'https://www.youtube.com/watch?v=W6NZfCO5SIk',
            },
            # C++
            {
                'title': '⚡ C++ : Les Bases',
                'description': 'Introduction au langage C++',
                'video_url': 'https://www.youtube.com/watch?v=vLnPwxZdW4Y',
            },
            # Java
            {
                'title': '☕ Java : Premiers Pas',
                'description': 'Découvrez Java et la POO',
                'video_url': 'https://www.youtube.com/watch?v=aA448lskNMU',
            },
            # SQL
            {
                'title': '🗄️ SQL : Requêtes de Base',
                'description': 'SELECT, FROM, WHERE et plus',
                'video_url': 'https://www.youtube.com/watch?v=HXV3zeQKqGY',
            },
        ]
        
        videos = []
        for data in videos_data:
            video = AcademyVideo.objects.create(**data)
            videos.append(video)
        
        return videos
    
    def _create_exercises(self):
        """Create test exercises"""
        exercises_data = [
            # ========== PYTHON ==========
            {
                'title': '🐍 Python : Hello World',
                'description': 'Votre premier programme Python',
                'language': 'python',
                'difficulty': 'easy',
                'instructions': '''Écrivez un programme qui affiche "Hello, Python!"

Utilisez la fonction print() pour afficher le texte.''',
                'starter_code': '# Écrivez votre code ici\n',
                'solution_code': 'print("Hello, Python!")',
            },
            {
                'title': '🐍 Python : Somme de deux nombres',
                'description': 'Calculez la somme de deux nombres',
                'language': 'python',
                'difficulty': 'easy',
                'instructions': '''Créez deux variables a=5 et b=3, puis affichez leur somme.

Exemple de sortie : 8''',
                'starter_code': '# Définissez a et b\n# Affichez leur somme\n',
                'solution_code': '''a = 5
b = 3
print(a + b)''',
            },
            {
                'title': '🐍 Python : Boucle de 1 à 10',
                'description': 'Utilisez une boucle for',
                'language': 'python',
                'difficulty': 'easy',
                'instructions': '''Affichez les nombres de 1 à 10, un par ligne.

Utilisez une boucle for avec range().''',
                'starter_code': '# Utilisez une boucle for\n',
                'solution_code': '''for i in range(1, 11):
    print(i)''',
            },
            
            # ========== JAVASCRIPT ==========
            {
                'title': '📜 JavaScript : Hello World',
                'description': 'Votre premier programme JavaScript',
                'language': 'javascript',
                'difficulty': 'easy',
                'instructions': '''Affichez "Hello, JavaScript!" dans la console.

Utilisez console.log()''',
                'starter_code': '// Écrivez votre code ici\n',
                'solution_code': 'console.log("Hello, JavaScript!");',
            },
            {
                'title': '📜 JavaScript : Addition',
                'description': 'Créez une fonction d\'addition',
                'language': 'javascript',
                'difficulty': 'easy',
                'instructions': '''Créez une fonction add(a, b) qui retourne la somme de a et b.

Puis affichez add(3, 5) dans la console.''',
                'starter_code': '''// Créez la fonction add
function add(a, b) {
    // Votre code ici
}

console.log(add(3, 5));
''',
                'solution_code': '''function add(a, b) {
    return a + b;
}

console.log(add(3, 5));''',
            },
            {
                'title': '📜 JavaScript : Boucle',
                'description': 'Utilisez une boucle for',
                'language': 'javascript',
                'difficulty': 'easy',
                'instructions': '''Affichez les nombres de 1 à 5 dans la console.

Utilisez une boucle for.''',
                'starter_code': '// Utilisez une boucle for\n',
                'solution_code': '''for(let i = 1; i <= 5; i++) {
    console.log(i);
}''',
            },
            
            # ========== C++ ==========
            {
                'title': '⚡ C++ : Hello World',
                'description': 'Votre premier programme C++',
                'language': 'cpp',
                'difficulty': 'easy',
                'instructions': '''Écrivez un programme qui affiche "Hello, C++"

N\'oubliez pas :
- #include <iostream>
- using namespace std; ou std::cout
- La fonction main()''',
                'starter_code': '''#include <iostream>
using namespace std;

int main() {
    // Votre code ici
    return 0;
}''',
                'solution_code': '''#include <iostream>
using namespace std;

int main() {
    cout << "Hello, C++" << endl;
    return 0;
}''',
            },
            {
                'title': '⚡ C++ : Addition',
                'description': 'Calculez une somme',
                'language': 'cpp',
                'difficulty': 'easy',
                'instructions': '''Créez deux variables a=10 et b=20, puis affichez leur somme.''',
                'starter_code': '''#include <iostream>
using namespace std;

int main() {
    // Votre code ici
    return 0;
}''',
                'solution_code': '''#include <iostream>
using namespace std;

int main() {
    int a = 10;
    int b = 20;
    cout << a + b << endl;
    return 0;
}''',
            },
            
            # ========== JAVA ==========
            {
                'title': '☕ Java : Hello World',
                'description': 'Votre premier programme Java',
                'language': 'java',
                'difficulty': 'easy',
                'instructions': '''Créez une classe Main avec une méthode main qui affiche "Hello, Java!"

Utilisez System.out.println()''',
                'starter_code': '''public class Main {
    public static void main(String[] args) {
        // Votre code ici
    }
}''',
                'solution_code': '''public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, Java!");
    }
}''',
            },
            {
                'title': '☕ Java : Multiplication',
                'description': 'Calculez un produit',
                'language': 'java',
                'difficulty': 'easy',
                'instructions': '''Affichez le résultat de 6 * 7''',
                'starter_code': '''public class Main {
    public static void main(String[] args) {
        // Votre code ici
    }
}''',
                'solution_code': '''public class Main {
    public static void main(String[] args) {
        System.out.println(6 * 7);
    }
}''',
            },
            
            # ========== SQL ==========
            {
                'title': '🗄️ SQL : SELECT Simple',
                'description': 'Votre première requête SQL',
                'language': 'sql',
                'difficulty': 'easy',
                'instructions': '''Écrivez une requête qui sélectionne toutes les colonnes de la table "users"''',
                'starter_code': '-- Écrivez votre requête ici\n',
                'solution_code': 'SELECT * FROM users;',
            },
            {
                'title': '🗄️ SQL : SELECT avec WHERE',
                'description': 'Filtrez les résultats',
                'language': 'sql',
                'difficulty': 'medium',
                'instructions': '''Sélectionnez le nom et l\'email des utilisateurs qui ont plus de 18 ans.

Table : users (id, nom, email, age)''',
                'starter_code': '-- Écrivez votre requête ici\n',
                'solution_code': 'SELECT nom, email FROM users WHERE age > 18;',
            },
            
            # ========== C ==========
            {
                'title': '🔧 C : Hello World',
                'description': 'Programme classique en C',
                'language': 'c',
                'difficulty': 'easy',
                'instructions': '''Écrivez un programme qui affiche "Hello, C!"

Utilisez printf()''',
                'starter_code': '''#include <stdio.h>

int main() {
    // Votre code ici
    return 0;
}''',
                'solution_code': '''#include <stdio.h>

int main() {
    printf("Hello, C!\\n");
    return 0;
}''',
            },
        ]
        
        exercises = []
        for data in exercises_data:
            exercise = AcademyExercise.objects.create(**data)
            exercises.append(exercise)
        
        return exercises
    
    def _create_courses(self, videos, exercises):
        """Create courses with items"""
        
        # Create lookup dictionaries
        video_dict = {v.title: v for v in videos}
        exercise_dict = {e.title: e for e in exercises}
        
        courses_data = [
            {
                'title': '🐍 Python - Débutant Complet',
                'description': 'Apprenez Python de zéro avec des exercices pratiques',
                'level': 'beginner',
                'estimated_duration': 120,
                'is_active': True,
                'items': [
                    {'type': 'video', 'title': '🐍 Introduction à Python'},
                    {'type': 'exercise', 'title': '🐍 Python : Hello World'},
                    {'type': 'exercise', 'title': '🐍 Python : Somme de deux nombres'},
                    {'type': 'video', 'title': '🐍 Python : Listes et Dictionnaires'},
                    {'type': 'exercise', 'title': '🐍 Python : Boucle de 1 à 10'},
                ]
            },
            {
                'title': '📜 JavaScript - Les Bases',
                'description': 'Maîtrisez JavaScript avec des exemples concrets',
                'level': 'beginner',
                'estimated_duration': 100,
                'is_active': True,
                'items': [
                    {'type': 'video', 'title': '📜 JavaScript pour Débutants'},
                    {'type': 'exercise', 'title': '📜 JavaScript : Hello World'},
                    {'type': 'exercise', 'title': '📜 JavaScript : Addition'},
                    {'type': 'video', 'title': '📜 JavaScript : Fonctions'},
                    {'type': 'exercise', 'title': '📜 JavaScript : Boucle'},
                ]
            },
            {
                'title': '⚡ C++ - Introduction',
                'description': 'Découvrez le puissant langage C++',
                'level': 'intermediate',
                'estimated_duration': 150,
                'is_active': True,
                'items': [
                    {'type': 'video', 'title': '⚡ C++ : Les Bases'},
                    {'type': 'exercise', 'title': '⚡ C++ : Hello World'},
                    {'type': 'exercise', 'title': '⚡ C++ : Addition'},
                ]
            },
            {
                'title': '☕ Java - Programmation Orientée Objet',
                'description': 'Apprenez Java et la POO',
                'level': 'intermediate',
                'estimated_duration': 140,
                'is_active': True,
                'items': [
                    {'type': 'video', 'title': '☕ Java : Premiers Pas'},
                    {'type': 'exercise', 'title': '☕ Java : Hello World'},
                    {'type': 'exercise', 'title': '☕ Java : Multiplication'},
                ]
            },
            {
                'title': '🗄️ SQL - Bases de Données',
                'description': 'Interrogez des bases de données avec SQL',
                'level': 'beginner',
                'estimated_duration': 90,
                'is_active': True,
                'items': [
                    {'type': 'video', 'title': '🗄️ SQL : Requêtes de Base'},
                    {'type': 'exercise', 'title': '🗄️ SQL : SELECT Simple'},
                    {'type': 'exercise', 'title': '🗄️ SQL : SELECT avec WHERE'},
                ]
            },
            {
                'title': '🔧 C - Les Fondamentaux',
                'description': 'Le langage C pour les débutants',
                'level': 'beginner',
                'estimated_duration': 80,
                'is_active': True,
                'items': [
                    {'type': 'exercise', 'title': '🔧 C : Hello World'},
                ]
            },
        ]
        
        courses = []
        for course_data in courses_data:
            items_data = course_data.pop('items')
            
            # Create course
            course = Course.objects.create(**course_data)
            
            # Add items to course
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

