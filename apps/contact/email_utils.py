import os
import logging
import requests
import threading
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_email_via_brevo_api(subject, recipient_email, message_body):
    """
    Sends email over HTTPS (Port 443) using Brevo (Sendinblue) REST API.
    Works 100% on Render Free Tier where SMTP Port 587 is blocked.
    """
    api_key = os.getenv('BREVO_API_KEY')
    if not api_key:
        return False

    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }

    sender_email = getattr(settings, 'EMAIL_HOST_USER', 'pundvyankateshwar@gmail.com') or 'pundvyankateshwar@gmail.com'

    payload = {
        "sender": {"name": "Vyankateshwar Pund Portfolio", "email": sender_email},
        "to": [{"email": recipient_email}],
        "subject": subject,
        "textContent": message_body
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code in [200, 201, 202]:
            logger.info(f"Email sent via Brevo HTTPS API to {recipient_email}")
            print(f"✅ Brevo HTTPS API success to {recipient_email}")
            return True
        else:
            logger.error(f"Brevo API error {response.status_code}: {response.text}")
            print(f"❌ Brevo API error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Brevo API request exception: {e}")
        print(f"❌ Brevo API exception: {e}")
        return False


def dispatch_contact_emails_async(contact_msg_id, name, email, subject, message):
    """
    Runs in a background thread so the HTTP response returns instantly (<50ms)
    without causing Gunicorn 500 worker timeouts on Render.
    """
    def _worker():
        print(f"📧 [Async Email Task] Starting for: {email}")

        admin_subject = f"🚀 New Portfolio Message from {name}: {subject}"
        admin_body = (
            f"You received a new message on your portfolio website:\n\n"
            f"Sender Name: {name}\n"
            f"Sender Email: {email}\n"
            f"Subject: {subject}\n\n"
            f"Message Content:\n{message}\n\n"
            f"--------------------------------------------------\n"
            f"Sent via Vyankateshwar Pund Portfolio Website"
        )

        user_subject = "Thank you for contacting Vyankateshwar Santosh Pund!"
        user_body = (
            f"Hi {name},\n\n"
            f"Thank you for reaching out through my portfolio website! I have received your message regarding '{subject}'.\n\n"
            f"I will review your inquiry and respond as soon as possible.\n\n"
            f"Best regards,\n"
            f"Vyankateshwar Santosh Pund\n"
            f"Python & Django Developer\n"
            f"Email: pundvyankateshwar@gmail.com | Phone: +91 8263986554\n"
        )

        # 1. Try Brevo HTTPS API first (Port 443 - works on Render Free Tier)
        if os.getenv('BREVO_API_KEY'):
            sent_admin = send_email_via_brevo_api(admin_subject, getattr(settings, 'RECIPIENT_EMAIL', 'pundvyankateshwar@gmail.com'), admin_body)
            sent_user = send_email_via_brevo_api(user_subject, email, user_body)
            if sent_admin or sent_user:
                return

        # 2. Fallback to standard Django SMTP / Console backend
        try:
            send_mail(
                subject=admin_subject,
                message=admin_body,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'pundvyankateshwar@gmail.com'),
                recipient_list=[getattr(settings, 'RECIPIENT_EMAIL', 'pundvyankateshwar@gmail.com')],
                fail_silently=True,
            )
            send_mail(
                subject=user_subject,
                message=user_body,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'pundvyankateshwar@gmail.com'),
                recipient_list=[email],
                fail_silently=True,
            )
            print(f"✅ Django mail backend finished for: {email}")
        except Exception as e:
            print(f"⚠️ Async email fallback exception: {e}")

    # Launch background thread
    thread = threading.Thread(target=_worker, daemon=True)
    thread.start()
