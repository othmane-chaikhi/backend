"""
Command to create advanced courses for all programming languages.
"""
from django.core.management.base import BaseCommand
from apps.portfolio.models import Course, AcademyVideo, AcademyExercise, CourseItem


class Command(BaseCommand):
    help = 'Create advanced courses for Java, C++, C, SQL, TypeScript, React'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Création des cours avancés...\n')

        # Create videos
        videos = self._create_videos()
        self.stdout.write(f'✅ {len(videos)} vidéos créées')

        # Create exercises
        exercises = self._create_exercises()
        self.stdout.write(f'✅ {len(exercises)} exercices créés')

        # Create courses
        courses = self._create_courses(videos, exercises)
        self.stdout.write(f'✅ {len(courses)} cours créés')

        self.stdout.write(self.style.SUCCESS('\n🎉 Cours avancés créés avec succès !'))

    def _create_videos(self):
        videos_data = [
            # Java Videos
            {
                'title': 'Introduction à Java',
                'description': 'Découvrez les bases de Java et la programmation orientée objet',
                'video_url': 'https://www.youtube.com/watch?v=aA448lskNMU',
            },
            {
                'title': 'Classes et Objets en Java',
                'description': 'Apprenez à créer des classes et des objets',
                'video_url': 'https://www.youtube.com/watch?v=aA448lskNMU',
            },
            # C++ Videos
            {
                'title': 'C++ : Les Fondamentaux',
                'description': 'Introduction à C++ et ses spécificités',
                'video_url': 'https://www.youtube.com/watch?v=vLnPwxZdW4Y',
            },
            {
                'title': 'Pointeurs et Références en C++',
                'description': 'Maîtrisez les concepts avancés de C++',
                'video_url': 'https://www.youtube.com/watch?v=vLnPwxZdW4Y',
            },
            # C Videos
            {
                'title': 'Programmation en C',
                'description': 'Les bases du langage C',
                'video_url': 'https://www.youtube.com/watch?v=KJgsSFOSQv0',
            },
            # SQL Videos
            {
                'title': 'SQL : Requêtes de Base',
                'description': 'Apprenez à interroger des bases de données',
                'video_url': 'https://www.youtube.com/watch?v=HXV3zeQKqGY',
            },
            {
                'title': 'SQL Avancé : JOIN et Sous-requêtes',
                'description': 'Maîtrisez les requêtes SQL avancées',
                'video_url': 'https://www.youtube.com/watch?v=HXV3zeQKqGY',
            },
            # TypeScript Videos
            {
                'title': 'TypeScript pour les Développeurs JS',
                'description': 'Ajoutez du typage à votre JavaScript',
                'video_url': 'https://www.youtube.com/watch?v=BwuLxPH8IDs',
            },
            # React Videos
            {
                'title': 'React : Components et Props',
                'description': 'Créez des interfaces avec React',
                'video_url': 'https://www.youtube.com/watch?v=SqcY0GlETPk',
            },
        ]

        videos = []
        for data in videos_data:
            video, created = AcademyVideo.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            videos.append(video)

        return videos

    def _create_exercises(self):
        exercises_data = [
            # Java Exercises
            {
                'title': 'Hello World en Java',
                'description': 'Créez votre premier programme Java',
                'language': 'java',
                'level': 'beginner',
                'instructions': '''Créez une classe HelloWorld avec une méthode main qui affiche "Hello, Java!"

Conseils :
- Utilisez public class HelloWorld
- Ajoutez public static void main(String[] args)
- Utilisez System.out.println() pour afficher''',
                'starter_code': '''public class HelloWorld {
    public static void main(String[] args) {
        // Votre code ici
    }
}''',
                'solution_code': '''public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, Java!");
    }
}''',
            },
            {
                'title': 'Calculatrice en Java',
                'description': 'Créez une classe Calculatrice avec des méthodes',
                'language': 'java',
                'level': 'intermediate',
                'instructions': '''Créez une classe Calculatrice avec :
- Une méthode additionner(int a, int b)
- Une méthode multiplier(int a, int b)''',
                'starter_code': '''public class Calculatrice {
    // Vos méthodes ici
}''',
                'solution_code': '''public class Calculatrice {
    public int additionner(int a, int b) {
        return a + b;
    }
    
    public int multiplier(int a, int b) {
        return a * b;
    }
}''',
            },
            # C++ Exercises
            {
                'title': 'Hello World en C++',
                'description': 'Votre premier programme C++',
                'language': 'cpp',
                'level': 'beginner',
                'instructions': '''Écrivez un programme qui affiche "Hello, C++"

Conseils :
- Incluez iostream
- Utilisez std::cout
- N'oubliez pas la fonction main''',
                'starter_code': '''#include <iostream>

int main() {
    // Votre code ici
    return 0;
}''',
                'solution_code': '''#include <iostream>

int main() {
    std::cout << "Hello, C++" << std::endl;
    return 0;
}''',
            },
            {
                'title': 'Fonction en C++',
                'description': 'Créez une fonction qui calcule le carré',
                'language': 'cpp',
                'level': 'intermediate',
                'instructions': 'Créez une fonction carre() qui prend un int et retourne son carré',
                'starter_code': '''#include <iostream>

// Votre fonction ici

int main() {
    std::cout << carre(5) << std::endl;
    return 0;
}''',
                'solution_code': '''#include <iostream>

int carre(int n) {
    return n * n;
}

int main() {
    std::cout << carre(5) << std::endl;
    return 0;
}''',
            },
            # C Exercises
            {
                'title': 'Hello World en C',
                'description': 'Programme classique en C',
                'language': 'c',
                'level': 'beginner',
                'instructions': 'Écrivez un programme qui affiche "Hello, C!"',
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
            {
                'title': 'Fonction Somme en C',
                'description': 'Créez une fonction qui additionne deux nombres',
                'language': 'c',
                'level': 'beginner',
                'instructions': 'Créez une fonction somme() qui additionne deux entiers',
                'starter_code': '''#include <stdio.h>

// Votre fonction ici

int main() {
    printf("%d\\n", somme(3, 5));
    return 0;
}''',
                'solution_code': '''#include <stdio.h>

int somme(int a, int b) {
    return a + b;
}

int main() {
    printf("%d\\n", somme(3, 5));
    return 0;
}''',
            },
            # SQL Exercises
            {
                'title': 'SELECT de Base',
                'description': 'Votre première requête SQL',
                'language': 'sql',
                'level': 'beginner',
                'instructions': '''Écrivez une requête qui sélectionne toutes les colonnes de la table "users"

Table : users (id, nom, email, age)''',
                'starter_code': '-- Votre requête ici',
                'solution_code': 'SELECT * FROM users;',
            },
            {
                'title': 'SELECT avec WHERE',
                'description': 'Filtrez les résultats',
                'language': 'sql',
                'level': 'beginner',
                'instructions': '''Sélectionnez le nom et l'email des utilisateurs qui ont plus de 18 ans

Table : users (id, nom, email, age)''',
                'starter_code': '-- Votre requête ici',
                'solution_code': 'SELECT nom, email FROM users WHERE age > 18;',
            },
            {
                'title': 'JOIN en SQL',
                'description': 'Joignez deux tables',
                'language': 'sql',
                'level': 'intermediate',
                'instructions': '''Sélectionnez les utilisateurs avec leurs commandes

Tables :
- users (id, nom)
- orders (id, user_id, produit)''',
                'starter_code': '-- Votre requête ici',
                'solution_code': 'SELECT users.nom, orders.produit FROM users JOIN orders ON users.id = orders.user_id;',
            },
            # TypeScript Exercises
            {
                'title': 'Interface TypeScript',
                'description': 'Définissez une interface',
                'language': 'javascript',
                'level': 'beginner',
                'instructions': 'Créez une interface User avec les propriétés : nom (string) et age (number)',
                'starter_code': '''// Définissez votre interface ici

const user: User = {
    nom: "Alice",
    age: 25
};''',
                'solution_code': '''interface User {
    nom: string;
    age: number;
}

const user: User = {
    nom: "Alice",
    age: 25
};''',
            },
            {
                'title': 'Fonction Typée',
                'description': 'Créez une fonction avec des types',
                'language': 'javascript',
                'level': 'intermediate',
                'instructions': 'Créez une fonction additionner() qui prend deux nombres et retourne leur somme',
                'starter_code': '''// Votre fonction ici

console.log(additionner(3, 5));''',
                'solution_code': '''function additionner(a: number, b: number): number {
    return a + b;
}

console.log(additionner(3, 5));''',
            },
            # React Exercises
            {
                'title': 'Composant React Simple',
                'description': 'Créez votre premier composant',
                'language': 'javascript',
                'level': 'beginner',
                'instructions': 'Créez un composant Welcome qui affiche "Bienvenue !"',
                'starter_code': '''import React from 'react';

// Votre composant ici

export default Welcome;''',
                'solution_code': '''import React from 'react';

function Welcome() {
    return <h1>Bienvenue !</h1>;
}

export default Welcome;''',
            },
            {
                'title': 'Composant avec Props',
                'description': 'Utilisez les props',
                'language': 'javascript',
                'level': 'intermediate',
                'instructions': 'Créez un composant Greeting qui affiche "Bonjour, [nom]" en utilisant une prop',
                'starter_code': '''import React from 'react';

// Votre composant ici

export default Greeting;''',
                'solution_code': '''import React from 'react';

function Greeting({ nom }) {
    return <h1>Bonjour, {nom}</h1>;
}

export default Greeting;''',
            },
        ]

        exercises = []
        for data in exercises_data:
            exercise, created = AcademyExercise.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            exercises.append(exercise)

        return exercises

    def _create_courses(self, videos, exercises):
        courses_data = [
            {
                'title': 'Java - Programmation Orientée Objet',
                'description': 'Maîtrisez Java et la POO',
                'level': 'intermediate',
                'estimated_duration': 120,
                'is_active': True,
                'items': [
                    {'type': 'video', 'ref': 'Introduction à Java'},
                    {'type': 'exercise', 'ref': 'Hello World en Java'},
                    {'type': 'video', 'ref': 'Classes et Objets en Java'},
                    {'type': 'exercise', 'ref': 'Calculatrice en Java'},
                ]
            },
            {
                'title': 'C++ - Programmation Système',
                'description': 'Apprenez C++ de A à Z',
                'level': 'advanced',
                'estimated_duration': 150,
                'is_active': True,
                'items': [
                    {'type': 'video', 'ref': 'C++ : Les Fondamentaux'},
                    {'type': 'exercise', 'ref': 'Hello World en C++'},
                    {'type': 'exercise', 'ref': 'Fonction en C++'},
                    {'type': 'video', 'ref': 'Pointeurs et Références en C++'},
                ]
            },
            {
                'title': 'C - Les Fondamentaux',
                'description': 'Le langage C pour les débutants',
                'level': 'beginner',
                'estimated_duration': 90,
                'is_active': True,
                'items': [
                    {'type': 'video', 'ref': 'Programmation en C'},
                    {'type': 'exercise', 'ref': 'Hello World en C'},
                    {'type': 'exercise', 'ref': 'Fonction Somme en C'},
                ]
            },
            {
                'title': 'SQL - Bases de Données',
                'description': 'Maîtrisez SQL et les bases de données',
                'level': 'beginner',
                'estimated_duration': 100,
                'is_active': True,
                'items': [
                    {'type': 'video', 'ref': 'SQL : Requêtes de Base'},
                    {'type': 'exercise', 'ref': 'SELECT de Base'},
                    {'type': 'exercise', 'ref': 'SELECT avec WHERE'},
                    {'type': 'video', 'ref': 'SQL Avancé : JOIN et Sous-requêtes'},
                    {'type': 'exercise', 'ref': 'JOIN en SQL'},
                ]
            },
            {
                'title': 'TypeScript - JavaScript Typé',
                'description': 'Ajoutez de la robustesse à votre JavaScript',
                'level': 'intermediate',
                'estimated_duration': 110,
                'is_active': True,
                'items': [
                    {'type': 'video', 'ref': 'TypeScript pour les Développeurs JS'},
                    {'type': 'exercise', 'ref': 'Interface TypeScript'},
                    {'type': 'exercise', 'ref': 'Fonction Typée'},
                ]
            },
            {
                'title': 'React - Interfaces Modernes',
                'description': 'Créez des applications avec React',
                'level': 'intermediate',
                'estimated_duration': 130,
                'is_active': True,
                'items': [
                    {'type': 'video', 'ref': 'React : Components et Props'},
                    {'type': 'exercise', 'ref': 'Composant React Simple'},
                    {'type': 'exercise', 'ref': 'Composant avec Props'},
                ]
            },
        ]

        # Create video/exercise lookup
        video_lookup = {v.title: v for v in videos}
        exercise_lookup = {e.title: e for e in exercises}

        courses = []
        for course_data in courses_data:
            items_data = course_data.pop('items')
            
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                defaults=course_data
            )
            
            if created:
                # Add items
                for idx, item_data in enumerate(items_data):
                    if item_data['type'] == 'video':
                        video = video_lookup.get(item_data['ref'])
                        if video:
                            CourseItem.objects.create(
                                course=course,
                                video=video,
                                order=idx
                            )
                    elif item_data['type'] == 'exercise':
                        exercise = exercise_lookup.get(item_data['ref'])
                        if exercise:
                            CourseItem.objects.create(
                                course=course,
                                exercise=exercise,
                                order=idx
                            )
            
            courses.append(course)

        return courses

