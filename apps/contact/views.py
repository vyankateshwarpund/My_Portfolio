from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .models import ContactMessage, NewsletterSubscriber
from .forms import ContactForm
import logging

logger = logging.getLogger(__name__)

class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/contact/'

    def form_valid(self, form):
        contact_msg = form.save()
        
        # 1. Send Email Notification to Vyankateshwar (Recipient)
        admin_subject = f"🚀 New Portfolio Message from {contact_msg.name}: {contact_msg.subject}"
        admin_body = (
            f"You received a new message on your portfolio website:\n\n"
            f"Sender Name: {contact_msg.name}\n"
            f"Sender Email: {contact_msg.email}\n"
            f"Subject: {contact_msg.subject}\n\n"
            f"Message Content:\n{contact_msg.message}\n\n"
            f"--------------------------------------------------\n"
            f"Sent via Vyankateshwar Pund Portfolio Website"
        )
        
        try:
            send_mail(
                subject=admin_subject,
                message=admin_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.RECIPIENT_EMAIL],
                fail_silently=False,
            )
            
            # 2. Send Auto-reply Confirmation Email to Sender
            user_subject = "Thank you for contacting Vyankateshwar Santosh Pund!"
            user_body = (
                f"Hi {contact_msg.name},\n\n"
                f"Thank you for reaching out through my portfolio website! I have received your message regarding '{contact_msg.subject}'.\n\n"
                f"I will review your inquiry and respond as soon as possible.\n\n"
                f"Best regards,\n"
                f"Vyankateshwar Santosh Pund\n"
                f"Junior Software Engineer | Python & Django Developer\n"
                f"Email: pundvyankateshwar@gmail.com | Phone: +91 8263986554\n"
            )
            send_mail(
                subject=user_subject,
                message=user_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[contact_msg.email],
                fail_silently=True,
            )
        except Exception as e:
            logger.error(f"SMTP Email Error: {e}")

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Thank you! Your message has been sent successfully.'})

        messages.success(self.request, "Thank you! Your message has been sent successfully.")
        return super().form_valid(form)

def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            sub, created = NewsletterSubscriber.objects.get_or_create(email=email)
            if created:
                msg = 'Thank you for subscribing to my newsletter!'
            else:
                msg = 'You are already subscribed to the newsletter.'
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': msg})
            messages.success(request, msg)
    return redirect('home')
