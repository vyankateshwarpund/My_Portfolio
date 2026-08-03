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

                # Dispatch email notification synchronously
                from .email_utils import send_contact_emails_synchronously
                email_status = send_contact_emails_synchronously(
                    contact_msg_id=contact_msg.id,
                    name=contact_msg.name,
                    email=contact_msg.email,
                    subject=contact_msg.subject,
                    message=contact_msg.message
                )
                logger.info(f"Email dispatch summary: {email_status}")

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


def test_email_view(request):
    """Diagnostic view to test email APIs live on Render."""
    import os, requests
    from django.http import HttpResponse
    from .email_utils import get_brevo_api_key, send_via_brevo_api

    brevo_key = get_brevo_api_key()
    resend_key = (os.getenv('RESEND_API_KEY') or '').strip()

    html = "<h1>📧 Email Diagnostic Test</h1>"

    if brevo_key:
        html += f"<p><b>Brevo API Key detected:</b> <code>{brevo_key[:10]}...</code> (length={len(brevo_key)})</p>"
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {"accept": "application/json", "api-key": brevo_key, "content-type": "application/json"}
        sender = (os.getenv('BREVO_SENDER_EMAIL') or os.getenv('EMAIL_HOST_USER') or 'pundvyankateshwar@gmail.com').strip()
        recipient = getattr(settings, 'RECIPIENT_EMAIL', 'pundvyankateshwar@gmail.com')

        payload = {
            "sender": {"name": "Portfolio Test", "email": sender},
            "to": [{"email": recipient}],
            "subject": "Diagnostic Test Email from Vyankateshwar Portfolio",
            "textContent": f"Test email to verify Brevo delivery to {recipient}."
        }

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=10)
            if resp.status_code in [200, 201, 202]:
                html += f"<p style='color:green; font-size:18px;'><b>✅ Brevo API Success (HTTP {resp.status_code}):</b> {resp.text}</p>"
                html += f"<p>Check inbox/spam at <b>{recipient}</b>!</p>"
            else:
                html += f"<p style='color:red; font-size:18px;'><b>❌ Brevo API Error (HTTP {resp.status_code}):</b> {resp.text}</p>"
                if "sender" in resp.text.lower() or "validated" in resp.text.lower():
                    html += (
                        "<div style='background:#fff3cd; padding:15px; border-radius:8px; margin-top:10px;'>"
                        "<b>💡 How to fix Brevo Sender Error:</b><br>"
                        "Brevo requires the sender email to be your Brevo account signup email.<br>"
                        "Add environment variable on Render: <code>BREVO_SENDER_EMAIL</code> set to your Brevo account email!"
                        "</div>"
                    )
        except Exception as ex:
            html += f"<p style='color:red;'><b>❌ Exception:</b> {ex}</p>"
    else:
        html += (
            "<p style='color:red; font-size:18px;'><b>⚠️ Brevo API Key NOT detected in environment variables.</b></p>"
            "<p>Make sure you added <code>BREVO_API_KEY</code> on Render under Environment Variables!</p>"
        )

    return HttpResponse(html)


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
