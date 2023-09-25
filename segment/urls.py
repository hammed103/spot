from django.urls import path


from .new_views import start,segment
urlpatterns = [
    path("api/start", start.as_view()),
     path("api/segment", segment.as_view()),
]
