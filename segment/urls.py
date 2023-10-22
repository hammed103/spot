from django.urls import path


from .new_views import start,segment,demo,callback,source
urlpatterns = [
    path("api/start", start.as_view()),
     path("api/segment", segment.as_view()),
     path("api/demo", demo.as_view()),
     path("api/source", source.as_view()),
     path('callback/', callback, name='callback'),
]
