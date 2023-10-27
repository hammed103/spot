from django.urls import path


from .server_views import start

urlpatterns = [
    path("api/start", start.as_view()),
]



"""urlpatterns = [
    path("api/start", start.as_view()),
     path("api/segment", segment.as_view()),
     path("api/demo", demo.as_view()),
     path("api/source", source.as_view()),
     path('callback/', callback, name='callback'),
]
"""