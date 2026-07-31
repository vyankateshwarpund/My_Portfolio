import os
import io
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.http import FileResponse, Http404
from django.conf import settings
from .models import Resume, Certificate

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_resume_buffer():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()

    name_style = ParagraphStyle('NameStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=20, leading=24, textColor=colors.HexColor('#0f172a'))
    title_style = ParagraphStyle('TitleStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=colors.HexColor('#4f46e5'))
    contact_style = ParagraphStyle('ContactStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor('#475569'))
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=colors.HexColor('#0f172a'))
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=13.5, textColor=colors.HexColor('#334155'))

    story.append(Paragraph('Vyankateshwar Santosh Pund', name_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph('Junior Software Engineer | Python & Django Developer | REST API Specialist', title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph('Amravati, Maharashtra, India | pundvyankateshwar@gmail.com | +91 8263986554', contact_style))
    story.append(Paragraph('LinkedIn: linkedin.com/in/vyankateshwar-pund-7a654632b | GitHub: github.com/vyankateshwarpund', contact_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width='100%', thickness=1.5, color=colors.HexColor('#cbd5e1'), spaceBefore=0, spaceAfter=8))

    story.append(Paragraph('SUMMARY', heading_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph('Junior Software Engineer with hands-on experience developing Python & Django web applications, REST APIs, MySQL databases, and clean architecture full-stack solutions.', body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph('WORK EXPERIENCE', heading_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph('<b>Junior Software Engineer</b> — CCIT Institute <i>(July 2026 – Present)</i>', body_style))
    story.append(Paragraph('• Engineered backend Django REST APIs for high-concurrency client modules.<br/>• Implemented secure JWT authentication and role-based access control (RBAC).', body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph('PROJECTS', heading_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph('<b>Student Management System REST API</b> <i>(Python, Django REST Framework, MySQL)</i>', body_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph('<b>E-Commerce Web Application</b> <i>(Python, Django, Bootstrap 5, MySQL)</i>', body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph('EDUCATION', heading_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph('<b>Bachelor of Engineering in Computer Science</b> — Dr. Rajendra Gode Institute of Technology <i>(CGPA: 8.06)</i>', body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

class ResumeView(TemplateView):
    template_name = 'resume.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume = Resume.objects.filter(is_active=True).first()

        # If resume exists but file field is empty, fallback to generated PDF
        if resume and not resume.file:
            relative_path = 'resume/Vyankateshwar_Pund_Resume.pdf'
            full_path = os.path.join(settings.MEDIA_ROOT, relative_path)
            if not os.path.exists(full_path):
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                buf = generate_pdf_resume_buffer()
                with open(full_path, 'wb') as f:
                    f.write(buf.read())
            resume.file.name = relative_path
            resume.save(update_fields=['file'])
                
        context['resume'] = resume
        context['certificates'] = Certificate.objects.all()[:6]
        return context

def download_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    resume.total_downloads += 1
    resume.save(update_fields=['total_downloads'])
    
    # Priority 1: Serve whatever file is currently attached to resume.file
    if resume.file:
        try:
            filename = os.path.basename(resume.file.name)
            return FileResponse(resume.file.open('rb'), as_attachment=True, filename=filename)
        except Exception:
            pass

    # Fallback if file is missing or invalid on disk
    relative_path = 'resume/Vyankateshwar_Pund_Resume.pdf'
    full_path = os.path.join(settings.MEDIA_ROOT, relative_path)
    
    if not os.path.exists(full_path):
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        buf = generate_pdf_resume_buffer()
        with open(full_path, 'wb') as f:
            f.write(buf.read())

    return FileResponse(open(full_path, 'rb'), as_attachment=True, filename="Vyankateshwar_Pund_Resume.pdf")
