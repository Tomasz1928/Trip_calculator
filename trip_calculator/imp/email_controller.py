from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

class EmailSender:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.subject = ''
        self.message = ''

    def send_email(self, message_type):
        self._generate_message(message_type)
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.email]
        send_mail(self.subject, self.message, from_email, recipient_list)

    def _generate_message(self, message_type):
        login_url = reverse('login_view')
        full_login_url = f'{settings.SITE_URL}{login_url}'

        message_generators = {
            'invitation': self._generate_invitation_message,
            'registration': self._generate_registration_message,
            'recovery': self._generate_recovery_message,
            'update_password': self._generate_update_password_message,
        }

        if message_type in message_generators:
            message_generators[message_type](full_login_url)
        else:
            raise ValueError(f'Unknown message type: {message_type}')

    def _generate_invitation_message(self, full_login_url):
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

    def _generate_registration_message(self, full_login_url):
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

    def _generate_recovery_message(self, full_login_url):
        self.subject = 'No Reply. Your new password for Trip Calculator System'
        self.message = (
            f'Recovery process finished successfully, below You will find a new generated password.\n\n'
            f'Here is Your password: {self.password}\n'
            f'Best regards,\n'
            f'Team Trip Cost Calculator'
        )

    def _generate_update_password_message(self, full_login_url):
        self.subject = 'No Reply. Your new password for Trip Calculator System'
        self.message = (
            f'Update password process finished successfully, below You will find Your new password.\n\n'
            f'Here is Your password: {self.password}\n'
            f'Best regards,\n'
            f'Team Trip Cost Calculator'
        )
