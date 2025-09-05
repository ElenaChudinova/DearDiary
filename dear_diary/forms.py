from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, BooleanField

from .models import Note


class ModerForm(forms.Form):
    stop_words = [
        "путин",
        "бомбить",
        "нахуй",
        "блять",
        "заебись",
        "пиздато",
        "пиздатое",
        "бабы",
        "полиция",
    ]


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs["class"] = "form-check-input"
            else:
                fild.widget.attrs["class"] = "form-control"


class NoteForm(ModerForm, StyleFormMixin, ModelForm):
    class Meta:
        model = Note
        exclude = ("views_counter", "owner", "avatar", "id")

    def clean_note(self):
        note = self.cleaned_data["subject_note"]
        for stop_word in self.stop_words:
            if stop_word in note.title():
                raise ValidationError("Вы использовали запрещенное слово")

        return note


class NoteModerForm(ModerForm, StyleFormMixin, ModelForm):
    class Meta:
        model = Note
        fields = ("subject_note", "text_note")


class SearchForm(forms.Form):
    query = forms.CharField(label="Поиск")
