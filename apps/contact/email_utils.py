import os
import logging
import requests
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_email_via_brevo_api(subject, recipient_email, message_body):
    """
    Sends email synchronously over HTTPS (Port 443) using Brevo REST API.
    Recommended for production deployments like Render where SMTP ports are blocked.
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
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        if response.status_code in [200, 201, 202]:
            logger.info(f"✅ Email successfully delivered via Brevo REST API to {recipient_email}")
            print(f"✅ Brevo HTTPS API success: delivered to {recipient_email}")
            return True
        else:
            logger.error(f"❌ Brevo API failed with status {response.status_code}: {response.text}")
            print(f"❌ Brevo API error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        logger.error(f"❌ Brevo API request exception: {e}")
        print(f"❌ Brevo API exception: {e}")
        return False


def send_contact_emails_synchronously(contact_msg_id, name, email, subject, message):
    """
    Synchronously dispatches contact notification and auto-reply emails.
    Uses fail_silently=False and checks send_mail() return value (> 0)
    to confirm actual acceptance by the mail backend.
    """
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

    email_status = {
        'admin_sent': False,
        'user_sent': False,
        'backend_used': 'none',
        'errors': []
    }

    # 1. Prefer Brevo REST API (HTTPS Port 443) if BREVO_API_KEY is configured
    if os.getenv('BREVO_API_KEY'):
        email_status['backend_used'] = 'brevo_api'
        admin_recipient = getattr(settings, 'RECIPIENT_EMAIL', 'pundvyankateshwar@gmail.com')
        email_status['admin_sent'] = send_email_via_brevo_api(admin_subject, admin_recipient, admin_body)
        email_status['user_sent'] = send_email_via_brevo_api(user_subject, email, user_body)
        return email_status

    # 2. Synchronous Django send_mail with fail_silently=False & return count check
    email_status['backend_used'] = getattr(settings, 'EMAIL_BACKEND', 'smtp')

    # Send admin notification email
    try:
        sent_count = send_mail(
            subject=admin_subject,
            message=admin_body,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'pundvyankateshwar@gmail.com'),
            recipient_list=[getattr(settings, 'RECIPIENT_EMAIL', 'pundvyankateshwar@gmail.com')],
            fail_silently=False,
        )
        if sent_count > 0:
            email_status['admin_sent'] = True
            logger.info(f"✅ Admin email accepted by backend for message ID {contact_msg_id}")
            print(f"✅ Admin email accepted (count: {sent_count})")
        else:
            email_status['errors'].append("Admin email returned sent_count = 0")
            logger.warning(f"⚠️ Admin email sent_count = 0 for message ID {contact_msg_id}")
    except Exception as e:
        error_msg = f"Admin send_mail failed: {str(e)}"
        email_status['errors'].append(error_msg)
        logger.error(f"❌ {error_msg}")
        print(f"❌ {error_msg}")

    # Send auto-reply email to sender
    try:
        sent_count = send_mail(
            subject=user_subject,
            message=user_body,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'pundvyankateshwar@gmail.com'),
            recipient_list=[email],
            fail_silently=False,
        )
        if sent_count > 0:
            email_status['user_sent'] = True
            logger.info(f"✅ User auto-reply email accepted by backend for {email}")
            print(f"✅ User auto-reply accepted (count: {sent_count})")
        else:
            email_status['errors'].append("User auto-reply returned sent_count = 0")
            logger.warning(f"⚠️ User auto-reply sent_count = 0 for {email}")
    except Exception as e:
        error_msg = f"User auto-reply send_mail failed: {str(e)}"
        email_status['errors'].append(error_msg)
        logger.error(f"❌ {error_msg}")
        print(f"❌ {error_msg}")

    return email_status
