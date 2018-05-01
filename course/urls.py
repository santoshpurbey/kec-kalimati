from django.urls import path

from .views import SubjectListView, SubjectSearchListView, NotelistView, download
urlpatterns = [
    path('note/<int:pk>/list', NotelistView.as_view(), name="note-list"),
    path('download/<int:pk>/', download, name="download"),
    path('', SubjectSearchListView.as_view(), name="home"),

]
