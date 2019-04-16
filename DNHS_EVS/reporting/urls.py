from django.conf.urls import url
from django.urls import path
from reporting.ViewsF import reporting

app_name = 'reporting'

urlpatterns = [
    path('reports/',
        reporting.Reporting.as_view(),
        name='reports'
    ),
    path('ajax/get_votes_distribution/',
        reporting.get_votes_distribution_ajax,
        name='get_votes_distribution_ajax'
    ),
]
