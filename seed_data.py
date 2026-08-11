import os
import sys
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'apps'))
django.setup()

from portfolio.models import ProfileInfo, Experience, Education, Service, Achievement, SocialLink, Testimonial, CareerStep
from skills.models import Skill
from projects.models import Project, ProjectCategory, Technology
from blogs.models import Blog, BlogCategory, Tag
from resume.models import Resume, Certificate
from django.contrib.auth.models import User

def run_seed():
    print("Updating database to reflect Fresher status with 3 Months Internship Experience...")

    # Create superuser if not exists
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser('admin', 'pundvyankateshwar@gmail.com', 'admin123')
        print("Created Superuser: admin / admin123")
    else:
        admin_user = User.objects.get(username='admin')

    # Profile Info - Fresher Persona
    profile, _ = ProfileInfo.objects.get_or_create(
        id=1,
        defaults={
            'name': 'Vyankateshwar Santosh Pund',
            'title_roles': 'Fresher Software Engineer | Python Developer | Django Backend Developer | Python Full Stack Developer',
            'location': 'Amravati, Maharashtra, India',
            'email': 'pundvyankateshwar@gmail.com',
            'phone': '+91 8263986554',
            'linkedin_url': 'https://linkedin.com/in/vyankateshwar-pund-7a654632b',
            'github_url': 'https://github.com/vyankateshwarpund',
            'about_summary': (
                "I am a motivated Fresher Software Engineer with 3 months of hands-on internship experience "
                "developing Python and Django applications. I have built REST APIs, authentication systems, CRUD applications, "
                "and relational MySQL databases. Enthusiastic about writing clean code, learning new backend technologies, "
                "and solving real-world software engineering challenges."
            ),
            'career_goals': (
                "Currently seeking entry-level opportunities as a Backend Developer or Full Stack Developer in high-growth "
                "engineering teams where I can leverage my Python/Django skills and contribute to scalable web applications."
            ),
            'profile_image': 'profile/vyankateshwar_profile.jpg',
            'projects_completed_count': 4,
            'internships_count': 1,
            'github_contributions_count': 520,
            'technologies_count': 20,
            'hours_coding_count': 500,
            'years_experience': '3 Months (Internship)',
        }
    )
    profile.projects_completed_count = 4
    profile.github_contributions_count = 520
    profile.technologies_count = 20
    profile.hours_coding_count = 500
    profile.title_roles = 'Fresher Software Engineer | Python Developer | Django Backend Developer | Python Full Stack Developer'
    profile.years_experience = '3 Months (Internship)'
    profile.about_summary = (
        "I am a motivated Fresher Software Engineer with 3 months of hands-on internship experience "
        "developing Python and Django applications. I have built REST APIs, authentication systems, CRUD applications, "
        "and relational MySQL databases. Enthusiastic about writing clean code, learning new backend technologies, "
        "and solving real-world software engineering challenges."
    )
    profile.profile_image = 'profile/vyankateshwar_profile.jpg'
    profile.save()

    # Experience - 3 Months Internship
    Experience.objects.all().delete()
    Experience.objects.create(
        company_name='CCIT Institute',
        role='Software Engineer Intern',
        location='Amravati, Maharashtra, India',
        start_date=date(2026, 7, 1),
        end_date=date(2026, 9, 30),
        is_current=False,
        responsibilities=(
            "• Completed 3-month Software Engineer Internship working on Python & Django web applications.\n"
            "• Developed REST APIs and implemented authentication, CRUD functionality, and MySQL database integrations.\n"
            "• Performed bug fixing, feature implementation, and API endpoint testing using Postman.\n"
            "• Maintained Git version control, branch workflows, and collaborated in team code reviews."
        ),
        tech_stack_used='Python, Django, Django REST Framework, MySQL, Git, Postman, Bootstrap 5'
    )
    print("3-Month Internship Experience updated.")

    # Skills - Fresher / Academic / Internship Metrics
    Skill.objects.all().delete()
    skills_data = [
        ("Python", "Backend", 90, "Advanced", "3 Months", "120+ Problems", "8 Projects", "bi bi-filetype-py", True, 1),
        ("Django", "Backend", 88, "Advanced", "3 Months", "80+ Problems", "6 Projects", "bi bi-box-seam", True, 2),
        ("Django REST Framework", "Backend", 85, "Intermediate", "3 Months", "40+ Endpoints", "5 Projects", "bi bi-cpu-fill", True, 3),
        ("MySQL & Django ORM", "Database", 88, "Advanced", "3 Months", "30+ Schemas", "6 Projects", "bi bi-database-gear", True, 4),
        ("SQL Query Optimization", "Database", 82, "Intermediate", "Academic", "25+ Queries", "4 Projects", "bi bi-speedometer2", True, 5),
        ("JavaScript & HTML5/CSS3", "Frontend", 85, "Advanced", "Academic", "60+ UI Features", "8 Projects", "bi bi-filetype-js", True, 6),
        ("Bootstrap 5 & Glassmorphism", "Frontend", 88, "Advanced", "Academic", "30+ Layouts", "6 Projects", "bi bi-bootstrap-fill", True, 7),
        ("Git, GitHub & Postman", "Tools", 90, "Advanced", "3 Months", "600+ Commits", "8 Projects", "bi bi-git", True, 8),
        ("OOP & Clean Architecture", "Concepts", 88, "Advanced", "Academic", "Core Principles", "6 Projects", "bi bi-bricks", True, 9),
        ("Docker (Basic)", "Tools", 75, "Basic", "Academic", "Containerization", "3 Projects", "bi bi-box", True, 10),
    ]
    for name, cat, prof, lvl, yrs, probs, projs, icon, feat, order in skills_data:
        Skill.objects.create(
            name=name, category=cat, proficiency_percent=prof, level_label=lvl,
            years_experience=yrs, problems_solved=probs, projects_count=projs,
            icon_class=icon, is_featured=feat, order=order
        )
    print("Fresher Skills metrics updated.")

    # Services
    Service.objects.all().delete()
    services_data = [
        ("Full Stack Web Development", "bi bi-layers", "End-to-end modern web applications with Bootstrap 5, JS & Django backend.", "Developing dynamic, responsive web applications seamlessly connected to Python/Django backends.", 1),
        ("Backend Development", "bi bi-server", "High-performance backend systems built with Python & Django.", "Designing robust, clean architecture backends with Django ORM, custom middleware, and optimized SQL performance.", 2),
        ("Frontend Development", "bi bi-layout-text-window-reverse", "Responsive, modern UI interfaces using Bootstrap 5, HTML5/CSS3 & JavaScript.", "Crafting clean, accessible, dark-mode enabled responsive web layouts with interactive user experience.", 3),
        ("REST API Development", "bi bi-code-slash", "Scalable, secure RESTful APIs built with Django REST Framework.", "Creating clear API endpoints with Swagger/OpenAPI documentation, token authentication, and JSON serialization.", 4),
        ("Database Design & Optimization", "bi bi-database-gear", "MySQL database schema modeling and SQL query tuning.", "Designing normalized database tables, indexing strategy, foreign key constraints, and efficient query execution.", 5),
        ("Python Developer", "bi bi-filetype-py", "Custom Python scripts, automation, data handling, and object-oriented backend logic.", "Writing clean, standard-compliant Python code for business logic, algorithms, and backend feature development.", 6),
    ]
    for title, icon, short_desc, full_desc, order in services_data:
        Service.objects.create(
            title=title, icon_class=icon, short_description=short_desc, full_description=full_desc, order=order
        )

    # Projects & Technologies
    cat_cms, _ = ProjectCategory.objects.get_or_create(name='Portfolio & CMS')
    cat_api, _ = ProjectCategory.objects.get_or_create(name='Backend & REST API')
    cat_web, _ = ProjectCategory.objects.get_or_create(name='Full Stack Web App')

    tech_dict = {
        'Python': 'bi bi-filetype-py',
        'Django': 'bi bi-box-seam',
        'Django REST Framework': 'bi bi-cpu',
        'MySQL': 'bi bi-database',
        'Bootstrap 5': 'bi bi-bootstrap',
        'JavaScript': 'bi bi-filetype-js',
        'Docker': 'bi bi-box',
    }
    tech_objs = {}
    for t_name, icon in tech_dict.items():
        tech_objs[t_name], _ = Technology.objects.get_or_create(name=t_name, defaults={'icon_class': icon})

    # Project 1: Enterprise Portfolio
    proj1, _ = Project.objects.update_or_create(
        id=3,
        defaults={
            'title': 'Enterprise Software Engineer Portfolio & Analytics',
            'slug': 'enterprise-software-engineer-portfolio-analytics',
            'short_description': 'Database-driven enterprise portfolio platform featuring Recruiter Analytics Dashboard, PWA, Docker, and DRF REST APIs.',
            'full_details': (
                'A state-of-the-art production personal portfolio built with Django, DRF, MySQL, Docker, and Bootstrap 5. '
                'Includes an interactive Recruiter Analytics Dashboard, PWA support, GitHub API stats integration, '
                'visitor IP tracking middleware, dynamic blog engine with Markdown support, and downloadable resume tracker.'
            ),
            'github_url': 'https://github.com/vyankateshwarpund/My_Portfolio',
            'live_demo_url': 'http://localhost:8000/',
            'case_study_url': '',
            'category': cat_cms,
            'status_badge': 'Production-Ready',
            'api_calls_count': '1000+ API Calls',
            'db_tables_count': '36 DB Tables',
            'apis_count': '40+ APIs',
            'features': (
                '• Recruiter & Admin Analytics Dashboard with Chart.js\n'
                '• Dark/Light Glassmorphic theme switcher with CSS variables\n'
                '• Django REST Framework APIs for all resources\n'
                '• Visitor tracking middleware & contact email auto-responder\n'
                '• Containerized deployment support with Docker & Docker Compose\n'
                '• Progressive Web App (PWA) with offline caching support'
            ),
            'views_count': 810,
            'likes_count': 89,
            'is_featured': True,
            'order': 1
        }
    )
    proj1.tech_stack.set([tech_objs['Python'], tech_objs['Django'], tech_objs['Django REST Framework'], tech_objs['MySQL'], tech_objs['Docker'], tech_objs['Bootstrap 5'], tech_objs['JavaScript']])

    # Project 2: Student Management System
    proj2, _ = Project.objects.update_or_create(
        id=1,
        defaults={
            'title': 'Student Management System REST API',
            'slug': 'student-management-system-rest-api',
            'short_description': 'Robust API managing 500+ student records with role-based access, JWT authentication, and MySQL backend.',
            'full_details': (
                'High-performance RESTful API service built with Django REST Framework for educational institution record management. '
                'Includes JWT authentication, role-based permission control (Admin, Teacher, Student), automated OpenAPI documentation, '
                'and complex SQL queries for academic reporting.'
            ),
            'github_url': 'https://github.com/vyankateshwarpund',
            'live_demo_url': 'http://localhost:8000/api/projects/',
            'case_study_url': '',
            'category': cat_api,
            'status_badge': 'Production-Ready',
            'api_calls_count': '5000+ API Calls',
            'db_tables_count': '25+ DB Tables',
            'apis_count': '40+ APIs',
            'features': (
                '• Role-based Access Control (RBAC) & JWT Authentication\n'
                '• Filter, Search, and Pagination endpoints for student records\n'
                '• Automated Swagger / OpenAPI documentation generation\n'
                '• Complex relational database joins and performance optimization'
            ),
            'views_count': 450,
            'likes_count': 42,
            'is_featured': True,
            'order': 2
        }
    )
    proj2.tech_stack.set([tech_objs['Python'], tech_objs['Django'], tech_objs['Django REST Framework'], tech_objs['MySQL']])

    # Project 3: E-Commerce Web Application
    proj3, _ = Project.objects.update_or_create(
        id=2,
        defaults={
            'title': 'E-Commerce Web Application',
            'slug': 'e-commerce-web-application',
            'short_description': 'Full-featured online shopping platform with cart management, product filter, secure checkout, and user auth.',
            'full_details': (
                'Comprehensive E-Commerce web application built with Python, Django, MySQL, and Bootstrap 5. '
                'Features user authentication, dynamic product catalog, multi-attribute filtering, shopping cart persistence, '
                'order history tracking, and interactive checkout interface.'
            ),
            'github_url': 'https://github.com/vyankateshwarpund',
            'live_demo_url': 'http://localhost:8000/projects/',
            'case_study_url': '',
            'category': cat_web,
            'status_badge': 'Production-Ready',
            'api_calls_count': '5000+ API Calls',
            'db_tables_count': '25+ DB Tables',
            'apis_count': '40+ APIs',
            'features': (
                '• Dynamic Product Catalog & Real-time Search Filtering\n'
                '• Session-persistent Shopping Cart & Order Tracking\n'
                '• Customer Account Dashboard & Purchase History\n'
                '• Fully Responsive Glassmorphic UI layout'
            ),
            'views_count': 620,
            'likes_count': 58,
            'is_featured': True,
            'order': 3
        }
    )
    proj3.tech_stack.set([tech_objs['Python'], tech_objs['Django'], tech_objs['MySQL'], tech_objs['Bootstrap 5'], tech_objs['JavaScript']])

    print("Database successfully seeded with all 3 projects, technologies, and metrics!")

if __name__ == '__main__':
    run_seed()

