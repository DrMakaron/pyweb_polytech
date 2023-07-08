from django.urls import path

from other.views import IndexView


urlpatterns = [
    path('', IndexView.as_view()),
]
