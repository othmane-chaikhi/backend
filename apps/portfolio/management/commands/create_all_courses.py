"""
Management command to create comprehensive courses for multiple programming languages
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.portfolio.models import Course, CourseItem, AcademyVideo, AcademyExercise

User = get_user_model()


class Command(BaseCommand):
    help = 'Create comprehensive courses for multiple programming languages'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🚀 Creating comprehensive courses...'))
        
        # Get or create a default admin user
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'is_staff': True, 'is_superuser': True}
        )
        
        # Create courses
        self.create_python_course(admin_user)
        self.create_javascript_course(admin_user)
        self.create_java_course(admin_user)
        self.create_cpp_course(admin_user)
        self.create_html_css_course(admin_user)
        self.create_sql_course(admin_user)
        self.create_c_course(admin_user)
        self.create_typescript_course(admin_user)
        self.create_react_course(admin_user)
        
        self.stdout.write(self.style.SUCCESS('✅ All courses created successfully!'))
    
    def create_python_course(self, admin_user):
        """Create Python course"""
        self.stdout.write('📘 Creating Python course...')
        
        course, _ = Course.objects.get_or_create(
            slug='python-fundamentals',
            defaults={
                'title': 'Python Fundamentals',
                'description': 'Master Python from basics to advanced concepts',
                'level': 'beginner',
                'order': 1,
                'is_active': True,
                'is_featured': True,
                'estimated_duration': 180,
            }
        )
        
        # Video 1: Introduction
        video1, _ = AcademyVideo.objects.get_or_create(
            title='Introduction to Python',
            defaults={
                'description': 'Learn Python basics and setup',
                'video_url': 'https://www.youtube.com/watch?v=kqtD5dpn9C8',
                'duration': 15,
                'order': 1,
                'difficulty': 'easy',
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='video',
            video=video1,
            order=1
        )
        
        # Exercise 1: Hello World
        ex1, _ = AcademyExercise.objects.get_or_create(
            title='Python Hello World',
            defaults={
                'description': 'Write your first Python program',
                'instructions': 'Create a function called `hello()` that prints "Hello, World!"',
                'language': 'python',
                'difficulty': 'easy',
                'starter_code': '# Define your hello function here\n',
                'solution_code': '''def hello():
    print("Hello, World!")

hello()''',
                'order': 2,
                'points': 20,
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='exercise',
            exercise=ex1,
            order=2
        )
        
        # Exercise 2: Variables and Types
        ex2, _ = AcademyExercise.objects.get_or_create(
            title='Python Variables',
            defaults={
                'description': 'Work with different data types',
                'instructions': 'Create variables: name (string), age (int), height (float) and print them',
                'language': 'python',
                'difficulty': 'easy',
                'starter_code': '# Create your variables here\n',
                'solution_code': '''name = "Alice"
age = 25
height = 1.65

print(f"Name: {name}")
print(f"Age: {age}")
print(f"Height: {height}")''',
                'order': 3,
                'points': 20,
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='exercise',
            exercise=ex2,
            order=3
        )
        
        # Exercise 3: Loops
        ex3, _ = AcademyExercise.objects.get_or_create(
            title='Python For Loop',
            defaults={
                'description': 'Learn to use for loops',
                'instructions': 'Write a function that prints numbers from 1 to 10 using a for loop',
                'language': 'python',
                'difficulty': 'easy',
                'starter_code': 'def print_numbers():\n    # Your code here\n    pass\n',
                'solution_code': '''def print_numbers():
    for i in range(1, 11):
        print(i)

print_numbers()''',
                'order': 4,
                'points': 30,
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='exercise',
            exercise=ex3,
            order=4
        )
        
        self.stdout.write(self.style.SUCCESS('✅ Python course created!'))
    
    def create_javascript_course(self, admin_user):
        """Create JavaScript course"""
        self.stdout.write('📙 Creating JavaScript course...')
        
        course, _ = Course.objects.get_or_create(
            slug='javascript-essentials',
            defaults={
                'title': 'JavaScript Essentials',
                'description': 'Learn modern JavaScript from scratch',
                'level': 'beginner',
                'order': 2,
                'is_active': True,
                'is_featured': True,
                'estimated_duration': 200,
            }
        )
        
        # Video 1
        video1, _ = AcademyVideo.objects.get_or_create(
            title='JavaScript Basics',
            defaults={
                'description': 'Introduction to JavaScript',
                'video_url': 'https://www.youtube.com/watch?v=W6NZfCO5SIk',
                'duration': 20,
                'order': 1,
                'difficulty': 'easy',
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='video',
            video=video1,
            order=1
        )
        
        # Exercise 1: Hello World
        ex1, _ = AcademyExercise.objects.get_or_create(
            title='JavaScript Hello World',
            defaults={
                'description': 'Your first JavaScript function',
                'instructions': 'Create a function called `greet()` that logs "Hello, JavaScript!" to the console',
                'language': 'javascript',
                'difficulty': 'easy',
                'starter_code': '// Define your greet function here\n',
                'solution_code': '''function greet() {
    console.log("Hello, JavaScript!");
}

greet();''',
                'order': 2,
                'points': 20,
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='exercise',
            exercise=ex1,
            order=2
        )
        
        # Exercise 2: Arrow Functions
        ex2, _ = AcademyExercise.objects.get_or_create(
            title='JavaScript Arrow Functions',
            defaults={
                'description': 'Learn modern arrow function syntax',
                'instructions': 'Create an arrow function `double` that takes a number and returns its double',
                'language': 'javascript',
                'difficulty': 'easy',
                'starter_code': '// Create your arrow function here\n',
                'solution_code': '''const double = (num) => num * 2;

console.log(double(5));
console.log(double(10));''',
                'order': 3,
                'points': 30,
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='exercise',
            exercise=ex2,
            order=3
        )
        
        # Exercise 3: Array Methods
        ex3, _ = AcademyExercise.objects.get_or_create(
            title='JavaScript Array Map',
            defaults={
                'description': 'Master array methods',
                'instructions': 'Use .map() to double all numbers in an array [1, 2, 3, 4, 5]',
                'language': 'javascript',
                'difficulty': 'medium',
                'starter_code': 'const numbers = [1, 2, 3, 4, 5];\n// Use .map() here\n',
                'solution_code': '''const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(num => num * 2);

console.log(doubled);''',
                'order': 4,
                'points': 30,
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='exercise',
            exercise=ex3,
            order=4
        )
        
        self.stdout.write(self.style.SUCCESS('✅ JavaScript course created!'))
    
    def create_java_course(self, admin_user):
        """Create Java course"""
        self.stdout.write('☕ Creating Java course...')
        
        course, _ = Course.objects.get_or_create(
            slug='java-programming',
            defaults={
                'title': 'Java Programming',
                'description': 'Learn Java object-oriented programming',
                'level': 'intermediate',
                'order': 3,
                'is_active': True,
                'is_featured': True,
                'estimated_duration': 250,
            }
        )
        
        # Video 1
        video1, _ = AcademyVideo.objects.get_or_create(
            title='Java Introduction',
            defaults={
                'description': 'Getting started with Java',
                'video_url': 'https://www.youtube.com/watch?v=eIrMbAQSU34',
                'duration': 25,
                'order': 1,
                'difficulty': 'medium',
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='video',
            video=video1,
            order=1
        )
        
        # Exercise 1: Hello World
        ex1, _ = AcademyExercise.objects.get_or_create(
            title='Java Hello World',
            defaults={
                'description': 'Your first Java program',
                'instructions': 'Create a Main class with a main method that prints "Hello, Java!"',
                'language': 'java',
                'difficulty': 'easy',
                'starter_code': '// Write your Main class here\n',
                'solution_code': '''public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, Java!");
    }
}''',
                'order': 2,
                'points': 30,
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='exercise',
            exercise=ex1,
            order=2
        )
        
        # Exercise 2: Variables
        ex2, _ = AcademyExercise.objects.get_or_create(
            title='Java Variables',
            defaults={
                'description': 'Work with Java data types',
                'instructions': 'Create a class that declares int, double, and String variables and prints them',
                'language': 'java',
                'difficulty': 'easy',
                'starter_code': 'public class Variables {\n    // Your code here\n}\n',
                'solution_code': '''public class Variables {
    public static void main(String[] args) {
        int age = 25;
        double height = 1.75;
        String name = "Alice";
        
        System.out.println("Age: " + age);
        System.out.println("Height: " + height);
        System.out.println("Name: " + name);
    }
}''',
                'order': 3,
                'points': 30,
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='exercise',
            exercise=ex2,
            order=3
        )
        
        # Exercise 3: For Loop
        ex3, _ = AcademyExercise.objects.get_or_create(
            title='Java For Loop',
            defaults={
                'description': 'Master Java loops',
                'instructions': 'Create a program that prints numbers 1 to 10 using a for loop',
                'language': 'java',
                'difficulty': 'medium',
                'starter_code': 'public class Loop {\n    // Your code here\n}\n',
                'solution_code': '''public class Loop {
    public static void main(String[] args) {
        for (int i = 1; i <= 10; i++) {
            System.out.println(i);
        }
    }
}''',
                'order': 4,
                'points': 40,
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='exercise',
            exercise=ex3,
            order=4
        )
        
        self.stdout.write(self.style.SUCCESS('✅ Java course created!'))
    
    def create_cpp_course(self, admin_user):
        """Create C++ course"""
        self.stdout.write('⚡ Creating C++ course...')
        
        course, _ = Course.objects.get_or_create(
            slug='cpp-mastery',
            defaults={
                'title': 'C++ Mastery',
                'description': 'Master C++ programming from basics to advanced',
                'level': 'intermediate',
                'order': 4,
                'is_active': True,
                'is_featured': True,
                'estimated_duration': 280,
            }
        )
        
        # Video 1
        video1, _ = AcademyVideo.objects.get_or_create(
            title='C++ Basics',
            defaults={
                'description': 'Introduction to C++',
                'video_url': 'https://www.youtube.com/watch?v=vLnPwxZdW4Y',
                'duration': 30,
                'order': 1,
                'difficulty': 'medium',
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='video',
            video=video1,
            order=1
        )
        
        # Exercise 1: Hello World
        ex1, _ = AcademyExercise.objects.get_or_create(
            title='C++ Hello World',
            defaults={
                'description': 'Your first C++ program',
                'instructions': 'Create a program that outputs "Hello, C++!" using cout',
                'language': 'c++',
                'difficulty': 'easy',
                'starter_code': '#include <iostream>\nusing namespace std;\n\n// Write your main function here\n',
                'solution_code': '''#include <iostream>
using namespace std;

int main() {
    cout << "Hello, C++!" << endl;
    return 0;
}''',
                'order': 2,
                'points': 30,
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='exercise',
            exercise=ex1,
            order=2
        )
        
        # Exercise 2: Variables
        ex2, _ = AcademyExercise.objects.get_or_create(
            title='C++ Variables',
            defaults={
                'description': 'Work with C++ data types',
                'instructions': 'Declare int, double, and string variables and display them using cout',
                'language': 'c++',
                'difficulty': 'easy',
                'starter_code': '#include <iostream>\nusing namespace std;\n\nint main() {\n    // Your code here\n    return 0;\n}\n',
                'solution_code': '''#include <iostream>
using namespace std;

int main() {
    int age = 25;
    double height = 1.75;
    string name = "Alice";
    
    cout << "Age: " << age << endl;
    cout << "Height: " << height << endl;
    cout << "Name: " << name << endl;
    
    return 0;
}''',
                'order': 3,
                'points': 30,
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='exercise',
            exercise=ex2,
            order=3
        )
        
        # Exercise 3: For Loop
        ex3, _ = AcademyExercise.objects.get_or_create(
            title='C++ For Loop',
            defaults={
                'description': 'Master C++ loops',
                'instructions': 'Write a program that prints numbers 1 to 10 using a for loop',
                'language': 'c++',
                'difficulty': 'medium',
                'starter_code': '#include <iostream>\nusing namespace std;\n\nint main() {\n    // Your for loop here\n    return 0;\n}\n',
                'solution_code': '''#include <iostream>
using namespace std;

int main() {
    for (int i = 1; i <= 10; i++) {
        cout << i << endl;
    }
    return 0;
}''',
                'order': 4,
                'points': 40,
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='exercise',
            exercise=ex3,
            order=4
        )
        
        self.stdout.write(self.style.SUCCESS('✅ C++ course created!'))
    
    def create_html_css_course(self, admin_user):
        """Create HTML/CSS course"""
        self.stdout.write('🎨 Creating HTML/CSS course...')
        
        course, _ = Course.objects.get_or_create(
            slug='web-design-basics',
            defaults={
                'title': 'Web Design Basics',
                'description': 'Learn HTML and CSS to build beautiful websites',
                'level': 'beginner',
                'order': 5,
                'is_active': True,
                'is_featured': True,
                'estimated_duration': 150,
            }
        )
        
        # Video 1
        video1, _ = AcademyVideo.objects.get_or_create(
            title='HTML Fundamentals',
            defaults={
                'description': 'Learn HTML structure',
                'video_url': 'https://www.youtube.com/watch?v=UB1O30fR-EE',
                'duration': 20,
                'order': 1,
                'difficulty': 'easy',
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='video',
            video=video1,
            order=1
        )
        
        # Exercise 1: Basic HTML
        ex1, _ = AcademyExercise.objects.get_or_create(
            title='HTML Basic Page',
            defaults={
                'description': 'Create your first HTML page',
                'instructions': 'Create an HTML page with title, heading, and paragraph',
                'language': 'html',
                'difficulty': 'easy',
                'starter_code': '<!-- Write your HTML here -->\n',
                'solution_code': '''<!DOCTYPE html>
<html>
<head>
    <title>My First Page</title>
</head>
<body>
    <h1>Welcome to My Website</h1>
    <p>This is my first HTML page!</p>
</body>
</html>''',
                'order': 2,
                'points': 20,
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='exercise',
            exercise=ex1,
            order=2
        )
        
        # Exercise 2: HTML Lists
        ex2, _ = AcademyExercise.objects.get_or_create(
            title='HTML Lists',
            defaults={
                'description': 'Work with HTML lists',
                'instructions': 'Create an unordered list with 3 items: Apple, Banana, Orange',
                'language': 'html',
                'difficulty': 'easy',
                'starter_code': '<!DOCTYPE html>\n<html>\n<body>\n    <!-- Create your list here -->\n</body>\n</html>\n',
                'solution_code': '''<!DOCTYPE html>
<html>
<body>
    <h2>Fruits</h2>
    <ul>
        <li>Apple</li>
        <li>Banana</li>
        <li>Orange</li>
    </ul>
</body>
</html>''',
                'order': 3,
                'points': 20,
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='exercise',
            exercise=ex2,
            order=3
        )
        
        # Video 2: CSS
        video2, _ = AcademyVideo.objects.get_or_create(
            title='CSS Styling',
            defaults={
                'description': 'Learn to style with CSS',
                'video_url': 'https://www.youtube.com/watch?v=1PnVor36_40',
                'duration': 25,
                'order': 4,
                'difficulty': 'easy',
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='video',
            video=video2,
            order=4
        )
        
        # Exercise 3: CSS Styling
        ex3, _ = AcademyExercise.objects.get_or_create(
            title='CSS Basic Styling',
            defaults={
                'description': 'Style HTML with CSS',
                'instructions': 'Create a CSS style that makes h1 red and centers text',
                'language': 'css',
                'difficulty': 'easy',
                'starter_code': '/* Write your CSS here */\n',
                'solution_code': '''h1 {
    color: red;
    text-align: center;
}

p {
    font-size: 16px;
    line-height: 1.5;
}''',
                'order': 5,
                'points': 30,
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='exercise',
            exercise=ex3,
            order=5
        )
        
        self.stdout.write(self.style.SUCCESS('✅ HTML/CSS course created!'))
    
    def create_sql_course(self, admin_user):
        """Create SQL course"""
        self.stdout.write('🗄️ Creating SQL course...')
        
        course, _ = Course.objects.get_or_create(
            slug='sql-database-essentials',
            defaults={
                'title': 'SQL Database Essentials',
                'description': 'Master database queries with SQL',
                'level': 'intermediate',
                'order': 6,
                'is_active': True,
                'is_featured': True,
                'estimated_duration': 180,
            }
        )
        
        # Video 1
        video1, _ = AcademyVideo.objects.get_or_create(
            title='SQL Introduction',
            defaults={
                'description': 'Introduction to databases and SQL',
                'video_url': 'https://www.youtube.com/watch?v=HXV3zeQKqGY',
                'duration': 30,
                'order': 1,
                'difficulty': 'medium',
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='video',
            video=video1,
            order=1
        )
        
        # Exercise 1: SELECT
        ex1, _ = AcademyExercise.objects.get_or_create(
            title='SQL SELECT Query',
            defaults={
                'description': 'Learn to query data',
                'instructions': 'Write a SELECT query to get all columns from the users table',
                'language': 'sql',
                'difficulty': 'easy',
                'starter_code': '-- Write your SELECT query here\n',
                'solution_code': '''SELECT * FROM users;''',
                'order': 2,
                'points': 20,
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='exercise',
            exercise=ex1,
            order=2
        )
        
        # Exercise 2: WHERE
        ex2, _ = AcademyExercise.objects.get_or_create(
            title='SQL WHERE Clause',
            defaults={
                'description': 'Filter data with WHERE',
                'instructions': 'Select all users WHERE age is greater than 18',
                'language': 'sql',
                'difficulty': 'easy',
                'starter_code': '-- Write your query with WHERE clause\n',
                'solution_code': '''SELECT * FROM users WHERE age > 18;''',
                'order': 3,
                'points': 30,
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='exercise',
            exercise=ex2,
            order=3
        )
        
        # Exercise 3: JOIN
        ex3, _ = AcademyExercise.objects.get_or_create(
            title='SQL JOIN',
            defaults={
                'description': 'Combine tables with JOIN',
                'instructions': 'Write a query that joins users and orders tables',
                'language': 'sql',
                'difficulty': 'medium',
                'starter_code': '-- Write your JOIN query\n',
                'solution_code': '''SELECT users.name, orders.product
FROM users
JOIN orders ON users.id = orders.user_id;''',
                'order': 4,
                'points': 40,
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='exercise',
            exercise=ex3,
            order=4
        )
        
        self.stdout.write(self.style.SUCCESS('✅ SQL course created!'))
    
    def create_c_course(self, admin_user):
        """Create C course"""
        self.stdout.write('🔧 Creating C course...')
        
        course, _ = Course.objects.get_or_create(
            slug='c-programming-basics',
            defaults={
                'title': 'C Programming Basics',
                'description': 'Learn the fundamentals of C programming',
                'level': 'intermediate',
                'order': 7,
                'is_active': True,
                'is_featured': False,
                'estimated_duration': 220,
            }
        )
        
        # Video 1
        video1, _ = AcademyVideo.objects.get_or_create(
            title='C Language Introduction',
            defaults={
                'description': 'Getting started with C',
                'video_url': 'https://www.youtube.com/watch?v=KJgsSFOSQv0',
                'duration': 25,
                'order': 1,
                'difficulty': 'medium',
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='video',
            video=video1,
            order=1
        )
        
        # Exercise 1: Hello World
        ex1, _ = AcademyExercise.objects.get_or_create(
            title='C Hello World',
            defaults={
                'description': 'Your first C program',
                'instructions': 'Create a program that prints "Hello, C!" using printf',
                'language': 'c',
                'difficulty': 'easy',
                'starter_code': '#include <stdio.h>\n\n// Write your main function here\n',
                'solution_code': '''#include <stdio.h>

int main() {
    printf("Hello, C!\\n");
    return 0;
}''',
                'order': 2,
                'points': 30,
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='exercise',
            exercise=ex1,
            order=2
        )
        
        # Exercise 2: Variables
        ex2, _ = AcademyExercise.objects.get_or_create(
            title='C Variables',
            defaults={
                'description': 'Work with C variables',
                'instructions': 'Declare int, float variables and print them using printf',
                'language': 'c',
                'difficulty': 'easy',
                'starter_code': '#include <stdio.h>\n\nint main() {\n    // Your code here\n    return 0;\n}\n',
                'solution_code': '''#include <stdio.h>

int main() {
    int age = 25;
    float height = 1.75;
    
    printf("Age: %d\\n", age);
    printf("Height: %.2f\\n", height);
    
    return 0;
}''',
                'order': 3,
                'points': 30,
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='exercise',
            exercise=ex2,
            order=3
        )
        
        self.stdout.write(self.style.SUCCESS('✅ C course created!'))
    
    def create_typescript_course(self, admin_user):
        """Create TypeScript course"""
        self.stdout.write('💙 Creating TypeScript course...')
        
        course, _ = Course.objects.get_or_create(
            slug='typescript-fundamentals',
            defaults={
                'title': 'TypeScript Fundamentals',
                'description': 'Learn TypeScript for type-safe JavaScript',
                'level': 'intermediate',
                'order': 8,
                'is_active': True,
                'is_featured': False,
                'estimated_duration': 160,
            }
        )
        
        # Video 1
        video1, _ = AcademyVideo.objects.get_or_create(
            title='TypeScript Introduction',
            defaults={
                'description': 'Why use TypeScript',
                'video_url': 'https://www.youtube.com/watch?v=ahCwqrYpIuM',
                'duration': 20,
                'order': 1,
                'difficulty': 'medium',
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='video',
            video=video1,
            order=1
        )
        
        # Exercise 1: Basic Types
        ex1, _ = AcademyExercise.objects.get_or_create(
            title='TypeScript Types',
            defaults={
                'description': 'Learn TypeScript type annotations',
                'instructions': 'Create variables with type annotations: string, number, boolean',
                'language': 'typescript',
                'difficulty': 'easy',
                'starter_code': '// Define typed variables here\n',
                'solution_code': '''const name: string = "Alice";
const age: number = 25;
const isStudent: boolean = true;

console.log(`Name: ${name}`);
console.log(`Age: ${age}`);
console.log(`Student: ${isStudent}`);''',
                'order': 2,
                'points': 30,
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='exercise',
            exercise=ex1,
            order=2
        )
        
        # Exercise 2: Functions
        ex2, _ = AcademyExercise.objects.get_or_create(
            title='TypeScript Functions',
            defaults={
                'description': 'Typed function parameters',
                'instructions': 'Create a function that takes two numbers and returns their sum with proper types',
                'language': 'typescript',
                'difficulty': 'medium',
                'starter_code': '// Create your typed function here\n',
                'solution_code': '''function add(a: number, b: number): number {
    return a + b;
}

console.log(add(5, 3));
console.log(add(10, 20));''',
                'order': 3,
                'points': 40,
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='exercise',
            exercise=ex2,
            order=3
        )
        
        self.stdout.write(self.style.SUCCESS('✅ TypeScript course created!'))
    
    def create_react_course(self, admin_user):
        """Create React course"""
        self.stdout.write('⚛️ Creating React course...')
        
        course, _ = Course.objects.get_or_create(
            slug='react-fundamentals',
            defaults={
                'title': 'React Fundamentals',
                'description': 'Build modern web apps with React',
                'level': 'advanced',
                'order': 9,
                'is_active': True,
                'is_featured': False,
                'estimated_duration': 240,
            }
        )
        
        # Video 1
        video1, _ = AcademyVideo.objects.get_or_create(
            title='React Introduction',
            defaults={
                'description': 'What is React and why use it',
                'video_url': 'https://www.youtube.com/watch?v=Tn6-PIqc4UM',
                'duration': 30,
                'order': 1,
                'difficulty': 'hard',
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='video',
            video=video1,
            order=1
        )
        
        # Exercise 1: Component
        ex1, _ = AcademyExercise.objects.get_or_create(
            title='React Component',
            defaults={
                'description': 'Create your first React component',
                'instructions': 'Create a functional component that returns a Hello message',
                'language': 'javascript',
                'difficulty': 'medium',
                'starter_code': '// Create your component here\n',
                'solution_code': '''function Hello() {
    return <h1>Hello, React!</h1>;
}

export default Hello;''',
                'order': 2,
                'points': 40,
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='exercise',
            exercise=ex1,
            order=2
        )
        
        # Exercise 2: Props
        ex2, _ = AcademyExercise.objects.get_or_create(
            title='React Props',
            defaults={
                'description': 'Use props in components',
                'instructions': 'Create a Greeting component that accepts a name prop',
                'language': 'javascript',
                'difficulty': 'medium',
                'starter_code': '// Create your component with props\n',
                'solution_code': '''function Greeting({ name }) {
    return <h1>Hello, {name}!</h1>;
}

export default Greeting;''',
                'order': 3,
                'points': 50,
                'is_active': True,
            }
        )
        
        CourseItem.objects.get_or_create(
            course=course,
            content_type='exercise',
            exercise=ex2,
            order=3
        )
        
        self.stdout.write(self.style.SUCCESS('✅ React course created!'))

