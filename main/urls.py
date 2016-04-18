__author__ = 'Kira'

from django.conf.urls import url

from .views import MainPage, HistoryView, DiagramView


urlpatterns = [
    url('^$', MainPage.as_view()),
    url('^history/', HistoryView.as_view()),
    url('^diagram', DiagramView.as_view())
]
