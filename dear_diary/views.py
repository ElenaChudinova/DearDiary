from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.template.context_processors import request
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.core.exceptions import PermissionDenied
from rest_framework.reverse import reverse_lazy

from dear_diary.forms import StyleFormMixin, NoteForm, NoteModerForm, SearchForm
from dear_diary.models import Note


class NoteListView(ListView):
    model = Note

    def get_queryset(self):
        return Note.objects.filter(public=True)

    def post_list(request):
        object_list = Note.objects.filter(public=True)
        paginator = Paginator(object_list, 6)  # 6 записей на каждой странице
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # Если страница не является целым числом, поставим первую страницу
            posts = paginator.page(1)
        except EmptyPage:
            # Если страница больше максимальной, доставить последнюю страницу результатов
            posts = paginator.page(paginator.num_pages)
        return render(request,
                      'dear_diary/pagination.html',
                      {'page': page,
                       'posts': posts})


class NoteDetailView(DetailView, StyleFormMixin, LoginRequiredMixin):
    model = Note

    def get_object(self, queryset=None, user=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_authenticated and self.object.public == True:
            self.object.views_counter += 1
            self.object.save()
            return self.object
        raise PermissionDenied


class NoteCreateView(CreateView, StyleFormMixin, LoginRequiredMixin):
    model = Note
    form_class = NoteForm
    success_url = reverse_lazy("dear_diary:note_list")

    def form_valid(self, form):
        note = form.save()
        user = self.request.user
        note.owner = user
        note.save()
        return super().form_valid(form)


class NoteUpdateView(UpdateView, StyleFormMixin, LoginRequiredMixin):
    model = Note
    form_class = NoteForm
    success_url = reverse_lazy("dear_diary:note_list")

    def form_valid(self, form):
        note = form.save()
        user = self.request.user
        note.owner = user
        note.save()
        return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return NoteForm
        if user.has_perm("dear_diary.can_edit_subject_note") and user.has_perm(
            "dear_diary.can_edit_text_note"
        ):
            return NoteModerForm
        raise PermissionDenied


class NoteDeleteView(DeleteView, StyleFormMixin, LoginRequiredMixin):
    model = Note
    success_url = reverse_lazy("dear_diary:note_list")


def search_view(request):
    query = None
    records = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            records = Note.objects.filter(subject_note__icontains=query)
    else:
        form = SearchForm()  # Если нет запроса, отображаем пустую форму

    context = {
        'form': form,
        'records': records,
        'query': query
    }
    return render(request, 'dear_diary/search_results.html', context)