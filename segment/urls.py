from django.urls import path


from .new_views import start
urlpatterns = [
    path("api/start", start.as_view()),
]
