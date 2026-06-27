import random
import logging
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
    Returns True if successful, False otherwise.
    """
    # ALWAYS log the OTP to the console for debugging/Render logs
    print(f"\n[OTP DEBUG] Email: {email} | Name: {name} | OTP: {otp}\n")

    subject = "Verify your TRANZO account - {{ otp }}"
    subject = subject.replace("{{ otp }}", otp)

    context = {
        'name': name,
        'otp': otp,
    }

    try:
        html_content = render_to_string('otp_email.html', context)
        text_content = strip_tags(html_content)
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        msg = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
        return True
    except Exception as e:
        logger.error(f"Failed to send HTML OTP email to {email}: {str(e)}")
        # We return False but the view will handle it gracefully now
        return False
