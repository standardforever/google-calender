from django.shortcuts import render

# Create your views here.

from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from google.oauth2 import credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build



class GoogleCalendarInitView(View):
    def get(self, request):
        flow = Flow.from_client_secrets_file(
            settings.GOOGLE_CLIENT_SECRET_FILE,
            scopes=['https://www.googleapis.com/auth/calendar.readonly'],
            redirect_uri=request.build_absolute_uri(reverse('google-calendar-redirect'))
        )

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )

        request.session['google_auth_state'] = state

        return HttpResponseRedirect(authorization_url)


class GoogleCalendarRedirectView(View):
    def get(self, request):
        state = request.session.pop('google_auth_state', None)
        if state is None:
            return HttpResponseRedirect(reverse('google-calendar-init'))

        flow = Flow.from_client_secrets_file(
            settings.GOOGLE_CLIENT_SECRET_FILE,
            scopes=['https://www.googleapis.com/auth/calendar.readonly'],
            redirect_uri=request.build_absolute_uri(reverse('google-calendar-redirect'))
        )

        flow.fetch_token(authorization_response=request.build_absolute_uri(),
                         state=state)

        credentials = flow.credentials

        # Use the credentials to access the Google Calendar API
        service = build('calendar', 'v3', credentials=credentials)
        events_result = service.events().list(calendarId='primary', maxResults=10).execute()
        events = events_result.get('items', [])
        # Process the events as per your requirement

        # Return events as JSON
        return JsonResponse({'events': events})