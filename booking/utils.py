from django.core.mail import send_mail
from django.conf import settings

def send_appointment_email(to_email, subject, message):
    from_email = settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'webmaster@localhost'
    send_mail(subject, message, from_email, [to_email])