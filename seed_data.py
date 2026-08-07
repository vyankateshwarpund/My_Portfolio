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
            'projects_completed_count': 8,
            'internships_count': 1,
            'github_contributions_count': 600,
            'technologies_count': 15,
            'hours_coding_count': 500,
            'years_experience': '3 Months (Internship)',
        }
    )
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

    print("Database successfully updated to Fresher persona with 3 Months Internship Experience!")

if __name__ == '__main__':
    run_seed()
