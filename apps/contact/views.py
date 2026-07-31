from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ContactMessage, NewsletterSubscriber
from .forms import ContactForm
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
def contact_view(request):
    """
    Production-ready contact view for Render deployment.
    Guarantees JSON response for AJAX requests and saves to database.
    """
    is_ajax = (
        request.headers.get('x-requested-with') == 'XMLHttpRequest' or
        request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' or
        'application/json' in request.headers.get('accept', '') or
        request.POST.get('is_ajax') == 'true' or
        request.GET.get('ajax') == '1'
    )

    if request.method == 'POST':
        try:
            form = ContactForm(request.POST)

            if form.is_valid():
                # Save to database first (guaranteed persistence)
                contact_msg = form.save()

                # Dispatch email notification in background thread (non-blocking)
                try:
                    from .email_utils import dispatch_contact_emails_async
                    dispatch_contact_emails_async(
                        contact_msg_id=contact_msg.id,
                        name=contact_msg.name,
                        email=contact_msg.email,
                        subject=contact_msg.subject,
                        message=contact_msg.message
                    )
                except Exception as email_err:
                    logger.error(f"Failed to dispatch async email task: {email_err}")

                # Return success response
                if is_ajax:
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Thank you! Your message has been sent successfully. I will reply soon!'
                    }, status=200)

                messages.success(request, "Thank you! Your message has been sent successfully.")
                return redirect('contact')

            else:
                # Form validation errors
                logger.warning(f"Contact form invalid: {form.errors}")
                if is_ajax:
                    errors = {field: [str(e) for e in err_list] for field, err_list in form.errors.items()}
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Please fill in all required fields correctly.',
                        'errors': errors
                    }, status=400)

                return render(request, 'contact.html', {'form': form})

        except Exception as e:
            logger.error(f"Contact view error: {e}", exc_info=True)
            if is_ajax:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Server error: {str(e)}'
                }, status=500)
            messages.error(request, f"Server error: {e}")
            return render(request, 'contact.html', {'form': ContactForm(request.POST)})

    # GET request — render form
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


@csrf_exempt
def subscribe_newsletter(request):
    is_ajax = (
        request.headers.get('x-requested-with') == 'XMLHttpRequest' or
        request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    )
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            try:
                sub, created = NewsletterSubscriber.objects.get_or_create(email=email)
                msg = 'Thank you for subscribing!' if created else 'You are already subscribed.'
                if is_ajax:
                    return JsonResponse({'status': 'success', 'message': msg})
                messages.success(request, msg)
            except Exception as e:
                logger.error(f"Newsletter subscribe error: {e}")
                if is_ajax:
                    return JsonResponse({'status': 'error', 'message': 'Subscription error.'}, status=500)
    return redirect('home')
