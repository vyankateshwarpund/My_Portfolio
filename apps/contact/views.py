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

            # Dispatch email sending asynchronously in background thread
            # Prevents Gunicorn 500 timeouts when Render free tier blocks or slows down Port 587
            from .email_utils import dispatch_contact_emails_async
            dispatch_contact_emails_async(
                contact_msg_id=contact_msg.id,
                name=contact_msg.name,
                email=contact_msg.email,
                subject=contact_msg.subject,
                message=contact_msg.message
            )

            # Return success immediately — message is saved to database
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


def test_smtp(request):
    import socket
    from django.http import HttpResponse
    try:
        s = socket.create_connection(("smtp.gmail.com", 587), timeout=10)
        s.close()
        return HttpResponse("✅ SMTP reachable: Connected successfully to smtp.gmail.com:587")
    except Exception as e:
        return HttpResponse(f"❌ Connection failed: {e}", status=500)


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
