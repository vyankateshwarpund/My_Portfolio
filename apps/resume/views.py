import os
import io
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.http import FileResponse, Http404
from django.conf import settings
from .models import Resume, Certificate

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_resume_buffer():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=26,
        bottomMargin=26
    )
    story = []
    styles = getSampleStyleSheet()

    name_style = ParagraphStyle('Name', fontName='Helvetica-Bold', fontSize=16, leading=19, alignment=1, textColor=colors.HexColor('#000000'))
    sub_title_style = ParagraphStyle('SubTitle', fontName='Helvetica-Bold', fontSize=9.5, leading=12, alignment=1, textColor=colors.HexColor('#1e293b'))
    contact_style = ParagraphStyle('Contact', fontName='Helvetica', fontSize=8, leading=11, alignment=1, textColor=colors.HexColor('#334155'))
    
    sec_heading_style = ParagraphStyle('SecHeading', fontName='Helvetica-Bold', fontSize=9, leading=11.5, textColor=colors.HexColor('#000000'))
    body_style = ParagraphStyle('Body', fontName='Helvetica', fontSize=8, leading=10.8, textColor=colors.HexColor('#1f2937'))
    bullet_style = ParagraphStyle('Bullet', fontName='Helvetica', fontSize=7.8, leading=10.4, textColor=colors.HexColor('#1f2937'), leftIndent=10)
    meta_style = ParagraphStyle('Meta', fontName='Helvetica-Oblique', fontSize=7.6, leading=9.8, textColor=colors.HexColor('#475569'))
    
    # 1. HEADER
    story.append(Paragraph('VYANKATESHWAR SANTOSH PUND', name_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph('Junior Software Engineer | Python / Django Developer', sub_title_style))
    story.append(Spacer(1, 2))
    contact_text = 'Amravati, Maharashtra | +91 8263986554 | pundvyankateshwar@gmail.com | linkedin.com/in/vyankateshwar-pund-7a654632b | github.com/vyankateshwarpund'
    story.append(Paragraph(contact_text, contact_style))
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#000000'), spaceBefore=1, spaceAfter=4))

    # 2. PROFESSIONAL SUMMARY
    story.append(Paragraph('PROFESSIONAL SUMMARY', sec_heading_style))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#64748b'), spaceBefore=1, spaceAfter=3))
    summary_text = (
        "Junior Python/Django Developer with hands-on experience developing full-stack web applications and "
        "RESTful APIs using Django, Django REST Framework (DRF), MySQL, JavaScript, and Django ORM. Built an "
        "e-commerce application featuring 40+ API endpoints and 20+ database tables, and developed a REST API "
        "supporting 500+ student records. Experienced in authentication, authorization, role-based access control, "
        "CRUD operations, database design, API integration, Git/GitHub, and deployment. Focused on writing clean, "
        "maintainable backend code and developing reliable, scalable web applications."
    )
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 4))

    # 3. TECHNICAL SKILLS
    story.append(Paragraph('TECHNICAL SKILLS', sec_heading_style))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#64748b'), spaceBefore=1, spaceAfter=3))
    
    skills = [
        "<b>Languages:</b> Python, JavaScript, SQL, HTML5, CSS3",
        "<b>Frameworks & Libraries:</b> Django, Django REST Framework (DRF), React, Bootstrap 5",
        "<b>Databases & ORM:</b> MySQL, Django ORM, SQL Query Optimization",
        "<b>APIs & Integrations:</b> REST APIs, Razorpay API, Postman",
        "<b>Developer Tools & Platforms:</b> Git, GitHub, Docker, VS Code, PythonAnywhere, Render",
        "<b>Backend & Engineering Concepts:</b> OOP, CRUD Operations, Authentication & Authorization, Role-Based Access Control (RBAC), Database Optimization, Caching, API Development",
        "<b>Development Practices:</b> Agile/Scrum, Code Review, Version Control"
    ]
    for sk in skills:
        story.append(Paragraph(sk, body_style))
        story.append(Spacer(1, 1))
    story.append(Spacer(1, 3))

    # 4. PROFESSIONAL EXPERIENCE
    story.append(Paragraph('PROFESSIONAL EXPERIENCE', sec_heading_style))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#64748b'), spaceBefore=1, spaceAfter=3))
    
    exp_table_data = [
        [
            Paragraph('<b>Junior Software Engineer — CCIT Institute</b>', body_style),
            Paragraph('<b>Jul 2026 – Present</b>', ParagraphStyle('DateR', parent=body_style, alignment=2))
        ],
        [
            Paragraph('<i>Amravati, India</i>', meta_style),
            Paragraph('', meta_style)
        ]
    ]
    t_exp = Table(exp_table_data, colWidths=[380, 160])
    t_exp.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(t_exp)
    story.append(Spacer(1, 1.5))
    
    exp_bullets = [
        "• Developed and maintained Python/Django web applications in collaboration with senior developers, implementing new features and resolving bugs in a live codebase.",
        "• Implemented and tested REST API endpoints using Django REST Framework (DRF), supporting applications designed for 50+ concurrent users.",
        "• Debugged application issues and contributed fixes to improve reliability and functionality across the Django codebase.",
        "• Participated in Git/GitHub version-control workflows and code reviews, identifying defects before merge and maintaining code quality."
    ]
    for b in exp_bullets:
        story.append(Paragraph(b, bullet_style))
        story.append(Spacer(1, 1))
    story.append(Spacer(1, 4))

    # 5. PROJECTS
    story.append(Paragraph('PROJECTS', sec_heading_style))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#64748b'), spaceBefore=1, spaceAfter=3))

    # Project 1: SPCart
    p1_data = [
        [Paragraph('<b>SPCart — Full-Stack E-Commerce Platform</b>', body_style), Paragraph('<b>Jul 2026 – Aug 2026</b>', ParagraphStyle('DR1', parent=body_style, alignment=2))],
        [Paragraph('<i>Personal Project | Amravati, India</i>', meta_style), Paragraph('', meta_style)]
    ]
    tp1 = Table(p1_data, colWidths=[380, 160])
    tp1.setStyle(TableStyle([('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 1)]))
    story.append(tp1)
    story.append(Paragraph('<b>Technologies:</b> Python, Django, MySQL, Django REST Framework, JavaScript, Bootstrap 5, Razorpay API', body_style))
    story.append(Spacer(1, 1))
    p1_bullets = [
        "• Engineered a modular Django e-commerce platform using an 11-app architecture with 20+ database tables and 40+ API endpoints for product catalog, cart, wishlist, and order management.",
        "• Integrated Razorpay payment processing with server-side HMAC signature verification to validate payment authenticity and secure order confirmation.",
        "• Implemented email OTP-based registration, custom administrative sales analytics, and automated order-status email notifications.",
        "• Optimized Django backend performance by eliminating N+1 queries with annotate(), implementing category caching, and configuring WhiteNoise for compressed static-file serving; deployed on PythonAnywhere."
    ]
    for b in p1_bullets:
        story.append(Paragraph(b, bullet_style))
        story.append(Spacer(1, 1))
    story.append(Spacer(1, 3))

    # Project 2: Student Management System
    p2_data = [
        [Paragraph('<b>Student Management System — REST API</b>', body_style), Paragraph('<b>Jan 2025 – Feb 2025</b>', ParagraphStyle('DR2', parent=body_style, alignment=2))],
        [Paragraph('<i>Personal Project | Amravati, India</i>', meta_style), Paragraph('', meta_style)]
    ]
    tp2 = Table(p2_data, colWidths=[380, 160])
    tp2.setStyle(TableStyle([('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 1)]))
    story.append(tp2)
    story.append(Paragraph('<b>Technologies:</b> Python, Django REST Framework, MySQL, Django ORM', body_style))
    story.append(Spacer(1, 1))
    p2_bullets = [
        "• Designed and developed a REST API for managing student records with full CRUD functionality across 500+ student entries.",
        "• Built Django ORM-based database operations to simplify data management and improve query handling.",
        "• Added authentication and role-based access control (RBAC) to restrict access to student data and application functionality."
    ]
    for b in p2_bullets:
        story.append(Paragraph(b, bullet_style))
        story.append(Spacer(1, 1))
    story.append(Spacer(1, 3))

    # Project 3: Portfolio & Analytics
    p3_data = [
        [Paragraph('<b>Portfolio & Analytics</b>', body_style), Paragraph('<b>Jun 2026 – Jul 2026</b>', ParagraphStyle('DR3', parent=body_style, alignment=2))],
        [Paragraph('<i>Personal Project | Amravati, India</i>', meta_style), Paragraph('', meta_style)]
    ]
    tp3 = Table(p3_data, colWidths=[380, 160])
    tp3.setStyle(TableStyle([('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 1)]))
    story.append(tp3)
    story.append(Paragraph('<b>Technologies:</b> Python, Django, Django REST Framework, MySQL, Bootstrap 5, Docker, Render', body_style))
    story.append(Spacer(1, 1))
    p3_bullets = [
        "• Engineered a Django and MySQL portfolio platform featuring 40+ DRF API endpoints, 36 database tables, and a recruiter analytics dashboard with live visitor IP tracking.",
        "• Implemented a responsive glassmorphism interface with persistent Dark/Light mode support and Progressive Web App (PWA) offline functionality.",
        "• Containerized the application and configured deployment using Docker and Render."
    ]
    for b in p3_bullets:
        story.append(Paragraph(b, bullet_style))
        story.append(Spacer(1, 1))
    story.append(Spacer(1, 4))

    # 6. EDUCATION
    story.append(Paragraph('EDUCATION', sec_heading_style))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#64748b'), spaceBefore=1, spaceAfter=3))
    
    edu_data = [
        [
            Paragraph('<b>B.E. — Computer Science and Engineering</b>', body_style),
            Paragraph('<b>2023 – 2027</b>', ParagraphStyle('DateR4', parent=body_style, alignment=2))
        ],
        [
            Paragraph('Dr. Rajendra Gode Institute of Technology & Research, Amravati — Sant Gadge Baba Amravati University (SGBAU)', meta_style),
            Paragraph('<b>CGPA: 8.06 / 10.00</b>', ParagraphStyle('CGPA', parent=body_style, alignment=2))
        ]
    ]
    t_edu = Table(edu_data, colWidths=[400, 140])
    t_edu.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(t_edu)

    doc.build(story)
    buffer.seek(0)
    return buffer

class ResumeView(TemplateView):
    template_name = 'resume.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume = Resume.objects.filter(is_active=True).first()

        # Ensure active resume file is present
        if not resume:
            resume = Resume.objects.create(
                title='Vyankateshwar Santosh Pund - Software Engineer Resume',
                file='resume/Vyankateshwar_Pund_Resume_ATS.pdf',
                is_active=True
            )
        elif not resume.file:
            resume.file.name = 'resume/Vyankateshwar_Pund_Resume_ATS.pdf'
            resume.save(update_fields=['file'])
                
        context['resume'] = resume
        context['certificates'] = Certificate.objects.all()[:6]
        return context

def download_resume(request, pk=None):
    if pk:
        try:
            resume = Resume.objects.get(pk=pk)
            resume.total_downloads += 1
            resume.save(update_fields=['total_downloads'])
        except Resume.DoesNotExist:
            resume = None
    else:
        resume = Resume.objects.filter(is_active=True).first()

    # Priority 1: Serve existing ATS file
    ats_relative = 'resume/Vyankateshwar_Pund_Resume_ATS.pdf'
    ats_full_path = os.path.join(settings.MEDIA_ROOT, ats_relative)
    
    if os.path.exists(ats_full_path):
        return FileResponse(open(ats_full_path, 'rb'), as_attachment=True, filename="Vyankateshwar_Santosh_Pund_Resume.pdf")

    # Priority 2: Static backup
    static_path = os.path.join(settings.BASE_DIR, 'static', 'resume', 'Vyankateshwar_Pund_Resume_ATS.pdf')
    if os.path.exists(static_path):
        return FileResponse(open(static_path, 'rb'), as_attachment=True, filename="Vyankateshwar_Santosh_Pund_Resume.pdf")

    # Priority 3: Dynamic Generation
    buf = generate_pdf_resume_buffer()
    return FileResponse(buf, as_attachment=True, filename="Vyankateshwar_Santosh_Pund_Resume.pdf")

