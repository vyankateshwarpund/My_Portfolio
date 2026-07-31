from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .models import ContactMessage, NewsletterSubscriber
from .forms import ContactForm
import logging

logger = logging.getLogger(__name__)


def contact_view(request):
    """Function-based contact view — reliable for both AJAX and regular POST."""
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            # Save to DB first — guaranteed even if email fails
            try:
                contact_msg = form.save()
            except Exception as e:
                logger.error(f"Contact DB save error: {e}")
                if is_ajax:
                    return JsonResponse(
                        {'status': 'error', 'message': 'Server error saving your message. Please try again.'},
                        status=500
                    )
                messages.error(request, 'Server error. Please try again.')
                return render(request, 'contact.html', {'form': form})

            # Print debug info to Render logs
            print("--- SMTP DEBUG INFO ---")
            print("HOST:", getattr(settings, 'EMAIL_HOST', None))
            print("PORT:", getattr(settings, 'EMAIL_PORT', None))
            print("USER:", getattr(settings, 'EMAIL_HOST_USER', None))
            print("PASSWORD LENGTH:", len(getattr(settings, 'EMAIL_HOST_PASSWORD', '') or ''))
            print("-----------------------")

            # Send notification email to portfolio owner
            try:
                send_mail(
                    subject=f"New Portfolio Message from {contact_msg.name}: {contact_msg.subject}",
                    message=(
                        f"You received a new message:\n\n"
                        f"Name: {contact_msg.name}\n"
                        f"Email: {contact_msg.email}\n"
                        f"Subject: {contact_msg.subject}\n\n"
                        f"Message:\n{contact_msg.message}\n\n"
                        f"-- Vyankateshwar Pund Portfolio"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.RECIPIENT_EMAIL],
                    fail_silently=False,
                )
                send_mail(
                    subject="Thank you for contacting Vyankateshwar Santosh Pund!",
                    message=(
                        f"Hi {contact_msg.name},\n\n"
                        f"Thank you for reaching out! I received your message about '{contact_msg.subject}'.\n\n"
                        f"I will respond as soon as possible.\n\n"
                        f"Best regards,\nVyankateshwar Santosh Pund\n"
                        f"Python & Django Developer | pundvyankateshwar@gmail.com"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[contact_msg.email],
                    fail_silently=False,
                )
                logger.info(f"Contact emails sent for: {contact_msg.email}")
            except Exception as e:
                logger.error(f"SMTP error (message already saved): {e}")
                print(f"EXACT SMTP ERROR: {e}")

            # Return success — message is saved regardless of email
            if is_ajax:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Thank you! Your message has been sent successfully. I will reply soon!'
                })
            messages.success(request, "Thank you! Your message has been sent successfully.")
            return redirect('contact')

        else:
            # Form validation failed
            logger.warning(f"Contact form invalid: {form.errors}")
            if is_ajax:
                errors = {}
                for field, error_list in form.errors.items():
                    errors[field] = [str(e) for e in error_list]
                return JsonResponse({
                    'status': 'error',
                    'message': 'Please fill in all required fields correctly.',
                    'errors': errors
                }, status=400)
            return render(request, 'contact.html', {'form': form})

    # GET request — show empty form
    form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            try:
                sub, created = NewsletterSubscriber.objects.get_or_create(email=email)
                msg = 'Thank you for subscribing!' if created else 'You are already subscribed.'
            except Exception as e:
                logger.error(f"Newsletter subscribe error: {e}")
                msg = 'Something went wrong. Please try again.'
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': msg})
            messages.success(request, msg)
    return redirect('home')
