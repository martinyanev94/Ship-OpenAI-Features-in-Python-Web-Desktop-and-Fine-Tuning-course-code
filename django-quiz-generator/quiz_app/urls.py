from django.urls import path
from . import views

urlpatterns = [
    path("", views.generate, name="generate"),
    path("history/", views.history, name="history"),
    path("download/<int:quiz_id>/", views.download, name="download"),
]
