
from django.urls import path
from . import views

from dear_diary.apps import DearDiaryConfig
from dear_diary.views import (
    NoteListView,
    NoteDetailView,
    NoteCreateView,
    NoteUpdateView,
    NoteDeleteView,
)

app_name = DearDiaryConfig.name

urlpatterns = [
    path("", NoteListView.as_view(), name="note_list"),
    path("notes/<int:pk>/", NoteDetailView.as_view(), name="note_detail"),
    path("notes/create/", NoteCreateView.as_view(), name="note_create"),
    path("notes/<int:pk>/update/", NoteUpdateView.as_view(), name="note_update"),
    path("notes/<int:pk>/delete/", NoteDeleteView.as_view(), name="note_delete"),
    path('search/', views.search_view, name='search'),
]
