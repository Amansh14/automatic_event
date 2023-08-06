from django.shortcuts import render

# Create your views here.


from django.http import JsonResponse
from django.core.management import call_command

def send_event_emails_view(request):
    try:
        call_command('send_event_emails')
        response_data = {'status': 'success', 'message': 'Event emails sent successfully.'}
    except Exception as e:
        response_data = {'status': 'error', 'message': str(e)}

    return JsonResponse(response_data)

