import logging
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from event_mail.models import Event, EmailTemplate, Employee

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Send automated event emails to employees'

    def handle(self, *args, **kwargs):
        current_date = timezone.now().date()
        events = Event.objects.filter(date=current_date)

        if not events:
            logger.info('No events scheduled for the current period.')
            return

        for event in events:
            try:
                email_template = EmailTemplate.objects.get(event_type=event.event_type)
                employee = Employee.objects.get(employee_id=event.employee_id)

                email_subject = email_template.subject
                email_body = email_template.body.replace('{{name}}', employee.name).replace('{{date}}', event.date)

                send_mail(
                    subject=email_subject,
                    message=email_body,
                    from_email='your_company@example.com',
                    recipient_list=[employee.email],
                    fail_silently=False,
                )

                logger.info(f'Successfully sent email to {employee.email}')
            except Exception as e:
                logger.error(f'Error sending email to {employee.email}: {e}')
