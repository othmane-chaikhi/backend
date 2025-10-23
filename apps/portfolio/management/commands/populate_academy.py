from django.core.management.base import BaseCommand
from apps.portfolio.models import AcademyVideo, AcademyExercise, Course, CourseItem


class Command(BaseCommand):
    help = 'Populate Academy with sample courses, videos, and exercises'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🚀 Création du contenu de test pour l\'Academy...'))
        
        # Clear existing data
        self.stdout.write('🗑️  Nettoyage des données existantes...')
        CourseItem.objects.all().delete()
        Course.objects.all().delete()
        AcademyVideo.objects.all().delete()
        AcademyExercise.objects.all().delete()
        
        # Create Videos
        self.stdout.write('🎥 Création des vidéos...')
        
        video1 = AcademyVideo.objects.create(
            title='Introduction à Python',
            description='Découvrez les bases de Python : variables, types de données et opérateurs.',
            video_url='https://www.youtube.com/embed/kqtD5dpn9C8',
            level='beginner',
            duration=15,
            order=1,
            is_active=True
        )
        
        video2 = AcademyVideo.objects.create(
            title='Les Fonctions en Python',
            description='Apprenez à créer et utiliser des fonctions en Python.',
            video_url='https://www.youtube.com/embed/9Os0o3wzS_I',
            level='beginner',
            duration=20,
            order=2,
            is_active=True
        )
        
        video3 = AcademyVideo.objects.create(
            title='Introduction à HTML',
            description='Découvrez les bases du HTML : balises, structure et sémantique.',
            video_url='https://www.youtube.com/embed/UB1O30fR-EE',
            level='beginner',
            duration=18,
            order=3,
            is_active=True
        )
        
        video4 = AcademyVideo.objects.create(
            title='CSS pour Débutants',
            description='Apprenez à styliser vos pages web avec CSS.',
            video_url='https://www.youtube.com/embed/1PnVor36_40',
            level='beginner',
            duration=22,
            order=4,
            is_active=True
        )
        
        video5 = AcademyVideo.objects.create(
            title='JavaScript - Les Bases',
            description='Introduction à JavaScript : variables, conditions et boucles.',
            video_url='https://www.youtube.com/embed/W6NZfCO5SIk',
            level='beginner',
            duration=25,
            order=5,
            is_active=True
        )
        
        self.stdout.write(self.style.SUCCESS(f'✅ {AcademyVideo.objects.count()} vidéos créées'))
        
        # Create Exercises
        self.stdout.write('📝 Création des exercices...')
        
        exercise1 = AcademyExercise.objects.create(
            title='Hello World en Python',
            description='Votre premier programme Python !',
            language='python',
            difficulty='easy',
            instructions='''Écrivez un programme qui affiche "Hello, World!" dans la console.

Conseils :
- Utilisez la fonction print()
- N'oubliez pas les guillemets autour du texte''',
            starter_code='# Écrivez votre code ici\n',
            solution_code='print("Hello, World!")',
            order=1,
            is_active=True
        )
        
        exercise2 = AcademyExercise.objects.create(
            title='Variables et Calculs',
            description='Manipulez des variables et effectuez des calculs simples.',
            language='python',
            difficulty='easy',
            instructions='''Créez deux variables 'a' et 'b' avec les valeurs 10 et 5.
Calculez et affichez :
- Leur somme
- Leur différence
- Leur produit

Exemple de sortie :
15
5
50''',
            starter_code='# Créez vos variables ici\na = 10\nb = 5\n\n# Affichez les résultats\n',
            solution_code='''a = 10
b = 5

print(a + b)
print(a - b)
print(a * b)''',
            order=2,
            is_active=True
        )
        
        exercise3 = AcademyExercise.objects.create(
            title='Fonction Addition',
            description='Créez votre première fonction Python.',
            language='python',
            difficulty='medium',
            instructions='''Créez une fonction 'addition' qui prend deux paramètres et retourne leur somme.
Testez la fonction avec les valeurs 15 et 27.

Exemple d'utilisation :
resultat = addition(15, 27)
print(resultat)  # Affiche 42''',
            starter_code='''# Créez votre fonction ici
def addition(a, b):
    # Votre code ici
    pass

# Testez votre fonction
''',
            solution_code='''def addition(a, b):
    return a + b

resultat = addition(15, 27)
print(resultat)''',
            order=3,
            is_active=True
        )
        
        exercise4 = AcademyExercise.objects.create(
            title='Page HTML Simple',
            description='Créez votre première page HTML.',
            language='html',
            difficulty='easy',
            instructions='''Créez une page HTML avec :
- Un titre h1 "Bienvenue sur ma page"
- Un paragraphe avec un texte de votre choix
- Une liste non ordonnée avec 3 éléments

Structure de base fournie.''',
            starter_code='''<!DOCTYPE html>
<html>
<head>
    <title>Ma Page</title>
</head>
<body>
    <!-- Ajoutez votre contenu ici -->
    
</body>
</html>''',
            solution_code='''<!DOCTYPE html>
<html>
<head>
    <title>Ma Page</title>
</head>
<body>
    <h1>Bienvenue sur ma page</h1>
    <p>Ceci est mon premier site web !</p>
    <ul>
        <li>Premier élément</li>
        <li>Deuxième élément</li>
        <li>Troisième élément</li>
    </ul>
</body>
</html>''',
            order=4,
            is_active=True
        )
        
        exercise5 = AcademyExercise.objects.create(
            title='Styliser avec CSS',
            description='Ajoutez du style à votre page.',
            language='html',
            difficulty='medium',
            instructions='''Créez une page HTML avec un style CSS intégré.
Ajoutez :
- Un titre h1 en bleu
- Un paragraphe avec une couleur de fond grise et du padding
- Une bordure autour du body''',
            starter_code='''<!DOCTYPE html>
<html>
<head>
    <title>Page Stylisée</title>
    <style>
        /* Ajoutez votre CSS ici */
        
    </style>
</head>
<body>
    <h1>Mon titre</h1>
    <p>Mon paragraphe</p>
</body>
</html>''',
            solution_code='''<!DOCTYPE html>
<html>
<head>
    <title>Page Stylisée</title>
    <style>
        body {
            border: 2px solid #333;
            padding: 20px;
        }
        h1 {
            color: blue;
        }
        p {
            background-color: #f0f0f0;
            padding: 15px;
        }
    </style>
</head>
<body>
    <h1>Mon titre</h1>
    <p>Mon paragraphe</p>
</body>
</html>''',
            order=5,
            is_active=True
        )
        
        exercise6 = AcademyExercise.objects.create(
            title='Alert JavaScript',
            description='Affichez une alerte avec JavaScript.',
            language='javascript',
            difficulty='easy',
            instructions='''Écrivez du code JavaScript qui :
1. Affiche une alerte avec le message "Bienvenue !"
2. Affiche dans la console "Script chargé"

Utilisez alert() et console.log()''',
            starter_code='''// Votre code JavaScript ici
''',
            solution_code='''alert("Bienvenue !");
console.log("Script chargé");''',
            order=6,
            is_active=True
        )
        
        self.stdout.write(self.style.SUCCESS(f'✅ {AcademyExercise.objects.count()} exercices créés'))
        
        # Create Courses
        self.stdout.write('📚 Création des cours...')
        
        # Course 1: Python for Beginners
        course1 = Course.objects.create(
            title='Python pour Débutants',
            slug='python-pour-debutants',
            description='Apprenez les bases de Python de zéro. Parfait pour les débutants qui veulent maîtriser la programmation.',
            level='beginner',
            order=1,
            is_active=True,
            is_featured=True,
            estimated_duration=120
        )
        
        CourseItem.objects.create(course=course1, content_type='video', video=video1, order=1, is_required=True)
        CourseItem.objects.create(course=course1, content_type='exercise', exercise=exercise1, order=2, is_required=True)
        CourseItem.objects.create(course=course1, content_type='exercise', exercise=exercise2, order=3, is_required=False)
        CourseItem.objects.create(course=course1, content_type='video', video=video2, order=4, is_required=True)
        CourseItem.objects.create(course=course1, content_type='exercise', exercise=exercise3, order=5, is_required=True)
        
        # Course 2: Web Development Basics
        course2 = Course.objects.create(
            title='Développement Web - Les Bases',
            slug='developpement-web-les-bases',
            description='Maîtrisez HTML et CSS pour créer vos premières pages web. Introduction complète au développement front-end.',
            level='beginner',
            order=2,
            is_active=True,
            is_featured=True,
            estimated_duration=150
        )
        
        CourseItem.objects.create(course=course2, content_type='video', video=video3, order=1, is_required=True)
        CourseItem.objects.create(course=course2, content_type='exercise', exercise=exercise4, order=2, is_required=True)
        CourseItem.objects.create(course=course2, content_type='video', video=video4, order=3, is_required=True)
        CourseItem.objects.create(course=course2, content_type='exercise', exercise=exercise5, order=4, is_required=True)
        
        # Course 3: JavaScript Introduction
        course3 = Course.objects.create(
            title='JavaScript - Introduction',
            slug='javascript-introduction',
            description='Découvrez JavaScript et rendez vos pages web interactives. Apprenez les fondamentaux du langage.',
            level='beginner',
            order=3,
            is_active=True,
            is_featured=False,
            estimated_duration=90
        )
        
        CourseItem.objects.create(course=course3, content_type='video', video=video5, order=1, is_required=True)
        CourseItem.objects.create(course=course3, content_type='exercise', exercise=exercise6, order=2, is_required=True)
        
        self.stdout.write(self.style.SUCCESS(f'✅ {Course.objects.count()} cours créés'))
        
        # Summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('🎉 CRÉATION TERMINÉE AVEC SUCCÈS !'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write('')
        self.stdout.write(f'📊 Résumé :')
        self.stdout.write(f'   • Vidéos      : {AcademyVideo.objects.count()}')
        self.stdout.write(f'   • Exercices   : {AcademyExercise.objects.count()}')
        self.stdout.write(f'   • Cours       : {Course.objects.count()}')
        self.stdout.write(f'   • Items Cours : {CourseItem.objects.count()}')
        self.stdout.write('')
        self.stdout.write('📚 Cours créés :')
        for course in Course.objects.all():
            items_count = course.items.count()
            self.stdout.write(f'   • {course.title} ({items_count} items)')
        self.stdout.write('')
        self.stdout.write('🚀 Testez maintenant :')
        self.stdout.write('   • http://localhost:3000/academy')
        self.stdout.write('   • http://localhost:3000/admin/academy')
        self.stdout.write('')

