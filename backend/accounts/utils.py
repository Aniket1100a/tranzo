import random
import logging
import os
import resend
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

logger = logging.getLogger(__name__)

def generate_otp():
    """Generates a random 6-digit OTP."""
    return str(random.randint(100000, 999999))

def send_otp_email(email, name, otp):
    """
    Sends a professional HTML 6-digit OTP to the provided email.
    Uses Resend API if RESEND_API_KEY is present (for Render), 
    otherwise falls back to SMTP (for Local).
    """
    # ALWAYS log the OTP to the console for Render logs fallback
    print(f"\n[OTP DEBUG] Email: {email} | Name: {name} | OTP: {otp}\n")

    subject = f"Verify your TRANZO account - {otp}"
    context = {
        'name': name,
        'otp': otp,
    }

    try:
        html_content = render_to_string('otp_email.html', context)
        text_content = strip_tags(html_content)
        
        # 1. Try Resend API (Works on Render)
        api_key = os.getenv("RESEND_API_KEY")
        if api_key:
            resend.api_key = api_key
            # Resend requires a verified domain or 'onboarding@resend.dev' for testing
            from_email = os.getenv("FROM_EMAIL", "onboarding@resend.dev")
            
            resend.Emails.send({
                "from": f"TRANZO <{from_email}>",
                "to": email,
                "subject": subject,
                "html": html_content,
            })
            return True

        # 2. Fallback to SMTP (Works locally)
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        msg = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
        return True

    except Exception as e:
        logger.error(f"Failed to send OTP email to {email}: {str(e)}")
        return False
