from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


class EmailSender:
    def __init__(self):
        self.subject = ''
        self.message = ''

    def send_email(self, message_type, **kwargs):
        self._generate_message(message_type, **kwargs)
        from_email = settings.DEFAULT_FROM_EMAIL
        send_mail(self.subject, self.message, from_email, [kwargs.get('email')])

    def _generate_message(self, message_type, **kwargs):
        login_url = reverse('login_view')
        full_login_url = f'{settings.SITE_URL}{login_url}'

        message_generators = {
            'invitation': lambda: self._generate_invitation_message(full_login_url, **kwargs),
            'registration': lambda: self._generate_registration_message(full_login_url, **kwargs),
            'recovery': lambda: self._generate_recovery_message(**kwargs),
            'update_password': lambda: self._generate_update_password_message(**kwargs),
        }

        message_generators[message_type]()

    def _generate_invitation_message(self, full_login_url, **kwargs):
        self.subject = 'No Reply. Invitation to Trip Calculator System'
        self.message = (
            f'You have been invited to the Trip Calculator system by Your friend.\n\n'
            f'Here is Your login: {kwargs.get('email')}\n'
            f'Here is Your password: {kwargs.get('password')}\n'
            f'Please use this credential to log in here: {full_login_url}\n\n'
            f'After Login please update Your First name and Last name.\n\n'
            f'Best regards,\n'
            f'Team Trip Cost Calculator'
        )

    def _generate_registration_message(self,full_login_url, **kwargs):
        self.subject = 'No Reply. Welcome to Trip Calculator System'
        self.message = (
            f'Thank You very much for registering in our system.\n\n'
            f'Below You will find Your login details.\n'
            f'Here is Your login: {kwargs.get('email')}\n'
            f'Here is Your password: {kwargs.get('password')}\n'
            f'Please use this credential to log in here: {full_login_url}\n\n'
            f'Best regards,\n'
            f'Team Trip Cost Calculator'
        )

    def _generate_recovery_message(self, **kwargs):
        self.subject = 'No Reply. Your new password for Trip Calculator System'
        self.message = (
            f'Recovery process finished successfully, below You will find a new generated password.\n\n'
            f'Here is Your password: {kwargs.get('password')}\n'
            f'Best regards,\n'
            f'Team Trip Cost Calculator'
        )

    def _generate_update_password_message(self, **kwargs):
        self.subject = 'No Reply. Your new password for Trip Calculator System'
        self.message = (
            f'Update password process finished successfully, below You will find Your new password.\n\n'
            f'Here is Your password: {kwargs.get('password')}\n'
            f'Best regards,\n'
            f'Team Trip Cost Calculator'
        )
