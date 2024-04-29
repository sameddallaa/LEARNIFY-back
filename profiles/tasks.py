from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task

@shared_task(bind=True)
def send_password_after_signup(password: str, recipients):
    
    for recipient in recipients:
        subject = 'Mot de passe Learnify'
        message = f"Bonjour, {recipient['first_name']}.\n\n Soyez les bienvenus à notre service.\n\nVotre mot de passe Learnify est le suivant:\n\n{password}\n\nIl est recommendé que vous le changiez pour des raisons de sécurité. \n\nEquipe Learnify."
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [recipient['email'], ]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)