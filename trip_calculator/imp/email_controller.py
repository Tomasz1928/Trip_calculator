from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


class EmailSender:
    def __init__(self) -> None:
        self.subject = ''
        self.message = ''
        self.email = ''
        self.password = ''

    def set_email(self, email: str) -> None:
        self.email = email

    def set_password(self, password: str) -> None:
        self.password = password

    def generate_invitation_message(self) -> None:
        login_url = reverse('login_view')
        full_login_url = f'{settings.SITE_URL}{login_url}'

        self.subject = 'No Reply. Invitation to Trip Calculator System'
        self.message = (
            f'You have been invited to the Trip Calculator system by Your friend.\n\n'
            f'Here is Your login: {self.email}\n'
            f'Here is Your password: {self.password}\n'
            f'Please use this credential to log in here: {full_login_url}\n\n'
            f'After Login please update Your First name and Last name.\n\n'
            f'Best regards,\n'
            f'Team Trip Cost Calculator'
        )

    def generate_registration_message(self) -> None:
        login_url = reverse('login_view')
        full_login_url = f'{settings.SITE_URL}{login_url}'

        self.subject = 'No Reply. Welcome to Trip Calculator System'
        self.message = (
            f'Thank You very much for registering in our system.\n\n'
            f'Below You will find Your login details.\n'
            f'Here is Your login: {self.email}\n'
            f'Here is Your password: {self.password}\n'
            f'Please use this credential to log in here: {full_login_url}\n\n'
            f'Best regards,\n'
            f'Team Trip Cost Calculator'
        )

    def generate_recovery_message(self) -> None:
        self.subject = 'No Reply. Your new password for Trip Calculator System'
        self.message = (
            f'Recovery process finished successfully, below You will found a new generated password.\n\n'
            f'Here is Your password: {self.password}\n'
            f'Best regards,\n'
            f'Team Trip Cost Calculator'
        )

    def generate_update_password_message(self) -> None:
        self.subject = 'No Reply. Your new password for Trip Calculator System'
        self.message = (
            f'Update password process finished successfully, below You will found Your new password.\n\n'
            f'Here is Your password: {self.password}\n'
            f'Best regards,\n'
            f'Team Trip Cost Calculator'
        )

    def send_email(self) -> None:
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.email]
        try:
            send_mail(self.subject, self.message, from_email, recipient_list)
        except Exception as e:
            print(e)