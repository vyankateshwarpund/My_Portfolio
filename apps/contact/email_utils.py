import os
import logging
import requests
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def get_brevo_api_key():
    """Detect Brevo API Key under any common environment variable name."""
    return (
        os.getenv('BREVO_API_KEY') or
        os.getenv('BREV_API_KEY') or
        os.getenv('BREVO_KEY') or
        os.getenv('BREVO_API') or
        os.getenv('SENDINBLUE_API_KEY') or
        ''
    ).strip()


def send_via_brevo_api(subject, recipient_email, message_body):
    """Sends email via Brevo REST API over HTTPS (Port 443 - works on Render Free Tier)."""
    api_key = get_brevo_api_key()
    if not api_key:
        print("⚠️ Brevo API Key not found in environment variables.")
        return False

    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }

    sender_email = (
        os.getenv('BREVO_SENDER_EMAIL') or
        os.getenv('EMAIL_HOST_USER') or
        getattr(settings, 'EMAIL_HOST_USER', 'pundvyankateshwar@gmail.com') or
        'pundvyankateshwar@gmail.com'
    ).strip()

    payload = {
        "sender": {"name": "Vyankateshwar Pund Portfolio", "email": sender_email},
        "to": [{"email": recipient_email}],
        "subject": subject,
        "textContent": message_body
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code in [200, 201, 202]:
            logger.info(f"✅ Brevo API success: delivered to {recipient_email}")
            print(f"✅ Brevo HTTPS API success: delivered to {recipient_email}")
            return True
        else:
            logger.error(f"❌ Brevo API error {response.status_code}: {response.text}")
            print(f"❌ Brevo API error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        logger.error(f"❌ Brevo API exception: {e}")
        print(f"❌ Brevo API exception: {e}")
        return False


def send_via_resend_api(subject, recipient_email, message_body):
    """Sends email via Resend REST API over HTTPS (Port 443)."""
    api_key = (os.getenv('RESEND_API_KEY') or '').strip()
    if not api_key:
        return False

    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    sender_email = os.getenv('RESEND_FROM_EMAIL', 'onboarding@resend.dev').strip()

    payload = {
        "from": f"Vyankateshwar Portfolio <{sender_email}>",
        "to": [recipient_email],
        "subject": subject,
        "text": message_body
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code in [200, 201, 202]:
            logger.info(f"✅ Resend API success: delivered to {recipient_email}")
            print(f"✅ Resend HTTPS API success: delivered to {recipient_email}")
            return True
        else:
            logger.error(f"❌ Resend API error {response.status_code}: {response.text}")
            print(f"❌ Resend API error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        logger.error(f"❌ Resend API exception: {e}")
        print(f"❌ Resend API exception: {e}")
        return False


def send_via_formspree(name, email, subject, message):
    """Sends notification via Formspree HTTP endpoint over Port 443."""
    endpoint = os.getenv('FORMSPREE_URL') or os.getenv('FORMSPREE_ENDPOINT')
    if not endpoint:
        formspree_id = os.getenv('FORMSPREE_ID')
        if formspree_id:
            endpoint = f"https://formspree.io/f/{formspree_id}"

    if not endpoint:
        return False

    payload = {
        "name": name,
        "email": email,
        "subject": subject,
        "message": message
    }

    try:
        response = requests.post(endpoint, json=payload, headers={"Accept": "application/json"}, timeout=10)
        if response.status_code in [200, 201, 202]:
            logger.info(f"✅ Formspree HTTP success for message from {email}")
            print(f"✅ Formspree HTTP success for message from {email}")
            return True
        else:
            logger.error(f"❌ Formspree error {response.status_code}: {response.text}")
            print(f"❌ Formspree error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        logger.error(f"❌ Formspree exception: {e}")
        print(f"❌ Formspree exception: {e}")
        return False


def send_contact_emails_synchronously(contact_msg_id, name, email, subject, message):
    """
    Production-grade email dispatcher for Render.
    Attempts HTTPS API providers (Brevo / Resend / Formspree) over Port 443 first,
    then falls back to Django SMTP.
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

    admin_recipient = getattr(settings, 'RECIPIENT_EMAIL', 'pundvyankateshwar@gmail.com')

    status_report = {
        'admin_sent': False,
        'user_sent': False,
        'backend_used': 'none',
        'errors': []
    }

    # 1. Try Brevo REST API (Checks BREVO_API_KEY, BREV_API_KEY, BREVO_KEY, SENDINBLUE_API_KEY)
    brevo_key = get_brevo_api_key()
    if brevo_key:
        print(f"📧 Brevo API Key detected (len={len(brevo_key)}). Sending via Brevo HTTPS API...")
        status_report['backend_used'] = 'brevo_api'
        status_report['admin_sent'] = send_via_brevo_api(admin_subject, admin_recipient, admin_body)
        status_report['user_sent'] = send_via_brevo_api(user_subject, email, user_body)
        if status_report['admin_sent'] or status_report['user_sent']:
            return status_report

    # 2. Try Resend REST API
    if os.getenv('RESEND_API_KEY'):
        print("📧 Resend API Key detected. Sending via Resend HTTPS API...")
        status_report['backend_used'] = 'resend_api'
        status_report['admin_sent'] = send_via_resend_api(admin_subject, admin_recipient, admin_body)
        status_report['user_sent'] = send_via_resend_api(user_subject, email, user_body)
        if status_report['admin_sent'] or status_report['user_sent']:
            return status_report

    # 3. Try Formspree HTTP Relay
    if os.getenv('FORMSPREE_URL') or os.getenv('FORMSPREE_ID'):
        print("📧 Formspree endpoint detected. Sending via Formspree HTTP...")
        status_report['backend_used'] = 'formspree'
        sent_fs = send_via_formspree(name, email, subject, message)
        status_report['admin_sent'] = sent_fs
        if sent_fs:
            return status_report

    # 4. Fallback to standard Django SMTP / Console backend
    status_report['backend_used'] = str(getattr(settings, 'EMAIL_BACKEND', 'smtp'))
    print(f"⚠️ No HTTP API keys found. Falling back to Django Backend ({status_report['backend_used']})...")

    # Send admin notification
    try:
        sent = send_mail(
            subject=admin_subject,
            message=admin_body,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'pundvyankateshwar@gmail.com'),
            recipient_list=[admin_recipient],
            fail_silently=False,
        )
        if sent > 0:
            status_report['admin_sent'] = True
            logger.info(f"✅ Admin SMTP email delivered (count={sent})")
        else:
            status_report['errors'].append("Admin send_mail returned 0 sent count")
    except Exception as e:
        err_msg = f"Admin SMTP send_mail failed: {e}"
        status_report['errors'].append(err_msg)
        logger.error(f"❌ {err_msg}")
        print(f"❌ {err_msg}")

    # Send user auto-reply
    try:
        sent = send_mail(
            subject=user_subject,
            message=user_body,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'pundvyankateshwar@gmail.com'),
            recipient_list=[email],
            fail_silently=False,
        )
        if sent > 0:
            status_report['user_sent'] = True
            logger.info(f"✅ User auto-reply SMTP delivered (count={sent})")
        else:
            status_report['errors'].append("User auto-reply returned 0 sent count")
    except Exception as e:
        err_msg = f"User auto-reply SMTP send_mail failed: {e}"
        status_report['errors'].append(err_msg)
        logger.error(f"❌ {err_msg}")
        print(f"❌ {err_msg}")

    return status_report
