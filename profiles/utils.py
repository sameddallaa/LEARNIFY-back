from django.conf import settings
import random
import string

from django.core.mail import send_mail

def send_password_after_signup(password: str, recipient):
    
    subject = 'Mot de passe Learnify'
    message = f"Bonjour, {recipient.first_name}.\n\n Soyez les bienvenus à notre service.\n\nVotre mot de passe Learnify est le suivant:\n\n {password}\n\nIl est recommendé que vous le changiez pour des raisons de sécurité. \n\nEquipe Learnify."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [recipient.email, ]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    
    

def generate_password(length=12):
    lower_case = string.ascii_lowercase
    upper_case = string.ascii_uppercase
    digits = string.digits
    special_chars = '!@#$%^&*()_+[]{}|;:,.<>?'

    all_chars = lower_case + upper_case + digits + special_chars

    if length < 8:
        raise ValueError("Password length must be at least 8 characters.")

    password = ''.join(random.sample(all_chars, length))

    return password
