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


def build_admin_html_email(name, email, subject, message):
    """Generate ultra-premium HTML email for Admin notification."""
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>New Portfolio Message</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0b0f19; color: #e2e8f0;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #0b0f19; padding: 40px 10px;">
    <tr>
      <td align="center">
        <table role="presentation" width="100%" max-width="600" cellspacing="0" cellpadding="0" style="max-width: 600px; background-color: #111827; border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 16px; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.5);">
          
          <!-- Header Banner -->
          <tr>
            <td style="background: linear-gradient(135deg, #4f46e5 0%, #7e22ce 50%, #db2777 100%); padding: 32px 24px; text-align: center;">
              <span style="background-color: rgba(255, 255, 255, 0.2); color: #ffffff; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;">🚀 New Contact Inquiry</span>
              <h1 style="color: #ffffff; margin: 16px 0 0 0; font-size: 24px; font-weight: 800; line-height: 1.3;">New Portfolio Message</h1>
              <p style="color: rgba(255, 255, 255, 0.85); margin: 6px 0 0 0; font-size: 14px;">Someone reached out through your portfolio website</p>
            </td>
          </tr>

          <!-- Content Body -->
          <tr>
            <td style="padding: 32px 28px; background-color: #111827;">
              
              <!-- Sender Details Card -->
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #1f2937; border-radius: 12px; padding: 20px; margin-bottom: 24px; border: 1px solid rgba(255, 255, 255, 0.08);">
                <tr>
                  <td style="padding-bottom: 12px;">
                    <span style="color: #94a3b8; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Sender Name</span>
                    <div style="color: #ffffff; font-size: 16px; font-weight: 700; margin-top: 4px;">{name}</div>
                  </td>
                </tr>
                <tr>
                  <td style="padding-bottom: 12px;">
                    <span style="color: #94a3b8; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Email Address</span>
                    <div style="margin-top: 4px;"><a href="mailto:{email}" style="color: #38bdf8; text-decoration: none; font-size: 15px; font-weight: 600;">{email}</a></div>
                  </td>
                </tr>
                <tr>
                  <td>
                    <span style="color: #94a3b8; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Subject</span>
                    <div style="color: #f8fafc; font-size: 15px; font-weight: 600; margin-top: 4px;">{subject}</div>
                  </td>
                </tr>
              </table>

              <!-- Message Content -->
              <div style="margin-bottom: 28px;">
                <span style="color: #94a3b8; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; display: block; margin-bottom: 8px;">Message Content</span>
                <div style="background-color: #0f172a; border-left: 4px solid #818cf8; border-radius: 0 12px 12px 0; padding: 20px; color: #e2e8f0; font-size: 15px; line-height: 1.6; white-space: pre-wrap;">{message}</div>
              </div>

              <!-- Reply Action Button -->
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
                <tr>
                  <td align="center">
                    <a href="mailto:{email}?subject=Re: {subject}" style="display: inline-block; background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); color: #ffffff; text-decoration: none; font-size: 15px; font-weight: 700; padding: 14px 32px; border-radius: 10px; box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3);">
                      ✉️ Reply to {name}
                    </a>
                  </td>
                </tr>
              </table>

            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background-color: #0f172a; padding: 20px 24px; text-align: center; border-top: 1px solid rgba(255, 255, 255, 0.08);">
              <p style="color: #64748b; font-size: 12px; margin: 0; line-height: 1.5;">
                Sent automatically via <b>Vyankateshwar Santosh Pund Portfolio System</b><br>
                Amravati, Maharashtra, India
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def build_user_html_email(name, subject):
    """Generate ultra-professional HTML auto-reply email for Sender."""
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Thank You for Reaching Out</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0b0f19; color: #e2e8f0;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #0b0f19; padding: 40px 10px;">
    <tr>
      <td align="center">
        <table role="presentation" width="100%" max-width="600" cellspacing="0" cellpadding="0" style="max-width: 600px; background-color: #111827; border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 16px; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.5);">
          
          <!-- Header Banner -->
          <tr>
            <td style="background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%); padding: 32px 24px; text-align: center;">
              <span style="background-color: rgba(255, 255, 255, 0.2); color: #ffffff; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;">✨ Message Received</span>
              <h1 style="color: #ffffff; margin: 16px 0 0 0; font-size: 24px; font-weight: 800; line-height: 1.3;">Thank You for Reaching Out!</h1>
              <p style="color: rgba(255, 255, 255, 0.9); margin: 6px 0 0 0; font-size: 14px;">I have received your inquiry and will get back to you shortly.</p>
            </td>
          </tr>

          <!-- Content Body -->
          <tr>
            <td style="padding: 32px 28px; background-color: #111827;">
              
              <p style="color: #f1f5f9; font-size: 16px; line-height: 1.6; margin-top: 0;">Hi <b>{name}</b>,</p>
              
              <p style="color: #cbd5e1; font-size: 15px; line-height: 1.6;">
                Thank you for contacting me through my portfolio website! I have received your message regarding:
              </p>

              <div style="background-color: #1f2937; border-left: 4px solid #38bdf8; border-radius: 0 10px 10px 0; padding: 16px; color: #f8fafc; font-size: 15px; font-weight: 600; margin: 20px 0;">
                "{subject}"
              </div>

              <p style="color: #cbd5e1; font-size: 15px; line-height: 1.6;">
                I review all incoming messages promptly and will respond to your email address as soon as possible.
              </p>

              <hr style="border: none; border-top: 1px solid rgba(255, 255, 255, 0.1); margin: 28px 0;">

              <!-- Profile / Signature Block -->
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
                <tr>
                  <td>
                    <div style="color: #ffffff; font-size: 16px; font-weight: 700;">Vyankateshwar Santosh Pund</div>
                    <div style="color: #38bdf8; font-size: 13px; font-weight: 600; margin-top: 2px;">Fresher Software Engineer | Python & Django Developer</div>
                    <div style="color: #94a3b8; font-size: 13px; margin-top: 6px;">📍 Amravati, Maharashtra, India</div>
                    <div style="color: #94a3b8; font-size: 13px; margin-top: 2px;">✉️ pundvyankateshwar@gmail.com | 📞 +91 8263986554</div>
                  </td>
                </tr>
              </table>

              <!-- Social Links Buttons -->
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="margin-top: 24px;">
                <tr>
                  <td>
                    <a href="https://linkedin.com/in/vyankateshwar-pund-7a654632b" target="_blank" style="display: inline-block; background-color: #1d4ed8; color: #ffffff; text-decoration: none; font-size: 13px; font-weight: 600; padding: 8px 18px; border-radius: 6px; margin-right: 8px;">LinkedIn Profile</a>
                    <a href="https://github.com/vyankateshwarpund" target="_blank" style="display: inline-block; background-color: #374151; color: #ffffff; text-decoration: none; font-size: 13px; font-weight: 600; padding: 8px 18px; border-radius: 6px;">GitHub Repositories</a>
                  </td>
                </tr>
              </table>

            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background-color: #0f172a; padding: 20px 24px; text-align: center; border-top: 1px solid rgba(255, 255, 255, 0.08);">
              <p style="color: #64748b; font-size: 12px; margin: 0;">
                © 2026 Vyankateshwar Santosh Pund. All rights reserved.
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def send_via_brevo_api(subject, recipient_email, text_body, html_body=None):
    """Sends HTML & Text email via Brevo REST API over HTTPS (Port 443)."""
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
        "textContent": text_body
    }

    if html_body:
        payload["htmlContent"] = html_body

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


def send_via_resend_api(subject, recipient_email, text_body, html_body=None):
    """Sends HTML & Text email via Resend REST API over HTTPS (Port 443)."""
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
        "text": text_body
    }

    if html_body:
        payload["html"] = html_body

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


def send_contact_emails_synchronously(contact_msg_id, name, email, subject, message):
    """
    Production-grade email dispatcher for Render.
    Sends rich HTML emails via Brevo / Resend / Django SMTP.
    """
    admin_subject = f"🚀 New Portfolio Message from {name}: {subject}"
    admin_text_body = (
        f"You received a new message on your portfolio website:\n\n"
        f"Sender Name: {name}\n"
        f"Sender Email: {email}\n"
        f"Subject: {subject}\n\n"
        f"Message Content:\n{message}\n\n"
        f"--------------------------------------------------\n"
        f"Sent via Vyankateshwar Pund Portfolio Website"
    )
    admin_html_body = build_admin_html_email(name, email, subject, message)

    user_subject = "Thank you for contacting Vyankateshwar Santosh Pund!"
    user_text_body = (
        f"Hi {name},\n\n"
        f"Thank you for reaching out through my portfolio website! I have received your message regarding '{subject}'.\n\n"
        f"I will review your inquiry and respond as soon as possible.\n\n"
        f"Best regards,\n"
        f"Vyankateshwar Santosh Pund\n"
        f"Python & Django Developer\n"
        f"Email: pundvyankateshwar@gmail.com | Phone: +91 8263986554\n"
    )
    user_html_body = build_user_html_email(name, subject)

    admin_recipient = getattr(settings, 'RECIPIENT_EMAIL', 'pundvyankateshwar@gmail.com')

    status_report = {
        'admin_sent': False,
        'user_sent': False,
        'backend_used': 'none',
        'errors': []
    }

    # 1. Try Brevo REST API
    brevo_key = get_brevo_api_key()
    if brevo_key:
        print(f"📧 Brevo API Key detected. Sending rich HTML emails via Brevo HTTPS API...")
        status_report['backend_used'] = 'brevo_api'
        status_report['admin_sent'] = send_via_brevo_api(admin_subject, admin_recipient, admin_text_body, admin_html_body)
        status_report['user_sent'] = send_via_brevo_api(user_subject, email, user_text_body, user_html_body)
        if status_report['admin_sent'] or status_report['user_sent']:
            return status_report

    # 2. Try Resend REST API
    if os.getenv('RESEND_API_KEY'):
        print("📧 Resend API Key detected. Sending rich HTML emails via Resend HTTPS API...")
        status_report['backend_used'] = 'resend_api'
        status_report['admin_sent'] = send_via_resend_api(admin_subject, admin_recipient, admin_text_body, admin_html_body)
        status_report['user_sent'] = send_via_resend_api(user_subject, email, user_text_body, user_html_body)
        if status_report['admin_sent'] or status_report['user_sent']:
            return status_report

    # 3. Fallback to standard Django SMTP
    status_report['backend_used'] = str(getattr(settings, 'EMAIL_BACKEND', 'smtp'))

    try:
        sent = send_mail(
            subject=admin_subject,
            message=admin_text_body,
            html_message=admin_html_body,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'pundvyankateshwar@gmail.com'),
            recipient_list=[admin_recipient],
            fail_silently=False,
        )
        if sent > 0:
            status_report['admin_sent'] = True
    except Exception as e:
        status_report['errors'].append(f"Admin SMTP failed: {e}")

    try:
        sent = send_mail(
            subject=user_subject,
            message=user_text_body,
            html_message=user_html_body,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'pundvyankateshwar@gmail.com'),
            recipient_list=[email],
            fail_silently=False,
        )
        if sent > 0:
            status_report['user_sent'] = True
    except Exception as e:
        status_report['errors'].append(f"User SMTP failed: {e}")

    return status_report
