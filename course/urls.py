from django.urls import path

from .views import SubjectListView, SubjectSearchListView, NotelistView,\
                    download, rating, clap, string_capture, online_class_list, online_class_attend
urlpatterns = [
    path('note/<int:pk>/list', NotelistView.as_view(), name="note-list"),
    path('download/<int:pk>/', download, name="download"),
    path('rating/<int:pk>/', rating, name="rating"),
    path('rating/<str:name>/', string_capture, name="string-capture"),
    path('online-class-list/', online_class_list, name="online-class-list"),
    path('online-class/<int:pk>/', online_class_attend, name="online-class"),
    path('', SubjectSearchListView.as_view(), name="home"),

]
