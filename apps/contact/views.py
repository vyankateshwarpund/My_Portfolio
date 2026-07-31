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

    def form_invalid(self, form):
        """Return JSON error for AJAX requests instead of re-rendering HTML."""
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors = {field: list(errs) for field, errs in form.errors.items()}
            return JsonResponse({
                'status': 'error',
                'message': 'Please fill in all required fields correctly.',
                'errors': errors
            }, status=400)
        return super().form_invalid(form)

    def form_valid(self, form):
        # Save message to DB first — guaranteed even if email fails
        try:
            contact_msg = form.save()
        except Exception as e:
            logger.error(f"DB save error: {e}")
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'Server error. Please try again later.'
                }, status=500)
            messages.error(self.request, 'Server error. Please try again.')
            return self.form_invalid(form)

        # Build email bodies
        admin_subject = f"New Portfolio Message from {contact_msg.name}: {contact_msg.subject}"
        admin_body = (
            f"You received a new message on your portfolio website:\n\n"
            f"Sender Name: {contact_msg.name}\n"
            f"Sender Email: {contact_msg.email}\n"
            f"Subject: {contact_msg.subject}\n\n"
            f"Message:\n{contact_msg.message}\n\n"
            f"--\nSent via Vyankateshwar Pund Portfolio Website"
        )
        user_body = (
            f"Hi {contact_msg.name},\n\n"
            f"Thank you for reaching out! I received your message about '{contact_msg.subject}'.\n\n"
            f"I will respond as soon as possible.\n\n"
            f"Best regards,\nVyankateshwar Santosh Pund\n"
            f"Python & Django Developer\n"
            f"Email: pundvyankateshwar@gmail.com"
        )

        # Send emails — fail silently, message is already saved to DB
        try:
            send_mail(
                subject=admin_subject,
                message=admin_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.RECIPIENT_EMAIL],
                fail_silently=True,
            )
            send_mail(
                subject="Thank you for contacting Vyankateshwar Santosh Pund!",
                message=user_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[contact_msg.email],
                fail_silently=True,
            )
            logger.info(f"Contact emails sent for: {contact_msg.email}")
        except Exception as e:
            logger.error(f"SMTP Email Error (message already saved to DB): {e}")

        # Always return success — message is saved to DB regardless of email status
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': 'Thank you! Your message has been sent successfully. I will reply soon!'
            })

        messages.success(self.request, "Thank you! Your message has been sent successfully.")
        return super().form_valid(form)


def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            sub, created = NewsletterSubscriber.objects.get_or_create(email=email)
            msg = 'Thank you for subscribing!' if created else 'You are already subscribed.'
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': msg})
            messages.success(request, msg)
    return redirect('home')
