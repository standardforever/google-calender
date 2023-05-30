from django.urls import path
from .views import GoogleCalendarInitView, GoogleCalendarRedirectView
from django.conf import settings


urlpatterns = [
    path('calendar/init/', GoogleCalendarInitView.as_view(), name='google-calendar-init'),
    path('calendar/redirect/', GoogleCalendarRedirectView.as_view(), name='google-calendar-redirect'),
]

if settings.DEBUG:
    urlpatterns += [
        path('rest/v1/calendar/redirect/', GoogleCalendarRedirectView.as_view(), name='google-calendar-redirect'),
    ]