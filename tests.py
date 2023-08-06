from django.test import TestCase
from django.utils import timezone
from event_mail.models import Event, EventType, EmailTemplate, Employee
from django.core.management import call_command
from unittest.mock import patch
import logging

logger = logging.getLogger(__name__)

class SendEventEmailsTestCase(TestCase):
    def setUp(self):
        self.event_type = EventType.objects.create(name='Birthday')
        self.email_template = EmailTemplate.objects.create(
            event_type=self.event_type,
            subject='Happy Birthday!',
            body='Dear {{name}},\n\nHappy Birthday on {{date}}!\n\nBest regards,\nYour Company',
        )
        self.employee = Employee.objects.create(
            email='employee@example.com',
            name='John Doe',
            employee_id='EMP123',
        )
        self.today_event = Event.objects.create(
            employee_id=self.employee.employee_id,
            event_type=self.event_type,
            date=timezone.now().date(),
        )
        self.future_event = Event.objects.create(
            employee_id=self.employee.employee_id,
            event_type=self.event_type,
            date=timezone.now().date() + timezone.timedelta(days=30),
        )

    @patch('event_email.management.commands.send_event_emails.send_mail')
    def test_send_event_emails(self, mock_send_mail):
        call_command('send_event_emails')
        self.assertEqual(mock_send_mail.call_count, 1)

    @patch('event_email.management.commands.send_event_emails.send_mail')
    def test_no_events_scheduled(self, mock_send_mail):
        self.today_event.delete()
        self.future_event.delete()
        call_command('send_event_emails')
        self.assertEqual(mock_send_mail.call_count, 0)
        self.assertIn('No events scheduled for the current period.', logger.output[0])

    @patch('event_email.management.commands.send_event_emails.send_mail')
    def test_error_sending_email(self, mock_send_mail):
        mock_send_mail.side_effect = Exception('Email sending error')
        call_command('send_event_emails')
        self.assertEqual(mock_send_mail.call_count, 1)
        self.assertIn('Error sending email to employee@example.com', logger.output[1])
        self.assertIn('Email sending error', logger.output[2])
