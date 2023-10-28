from typing import Any
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Note
from django_filters.views import FilterView
from .filters import NoteFilter, PublicNoteFilter
from .forms import CreatePublicNoteForm, CreateNoteForm

# Create your views here.


class PublicNoteView(FilterView):
    template_name = "notes/public_notes.html"
    model = Note
    context_object_name = "notes"
    filterset_class = PublicNoteFilter

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(is_public=True, is_archive=False)


class MyNotesView(FilterView):
    template_name = "notes/my_notes.html"
    model = Note
    filterset_class = NoteFilter
    context_object_name = "notes"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(author_id=self.request.user.id, is_archive=False)


class MyArchiveNotesView(FilterView):
    template_name = "notes/my_archive_notes.html"
    model = Note
    context_object_name = "notes"
    filterset_class = NoteFilter

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(author_id=self.request.user.id, is_archive=True)


class CreateNote(CreateView):
    template_name = "notes/create_note.html"
    form_class = CreateNoteForm
    success_url = reverse_lazy("notes:my_notes")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CreatePublicNote(CreateView):
    template_name = "notes/create_public_note.html"
    form_class = CreatePublicNoteForm
    success_url = reverse_lazy("notes:public_notes")

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.is_public = True
        return super().form_valid(form)
