from django.contrib import admin

from dear_diary.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    idlelib = ("id",)
    list_display = (
        "id",
        "subject_note",
        "text_note",
        "views_counter",
        "owner",
        "public",
    )
    list_filter = ("owner",)
    search_fields = (
        "owner",
        "subject_note",
    )
