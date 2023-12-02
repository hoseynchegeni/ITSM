from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from ..models import TaskStatus, Task
from django.urls import reverse_lazy
from ..forms import CreateTaskStatusForm
from db_events.models import TaskLog
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django_filters.views import FilterView
from ..filters import StatusFilter



class StatusListView(LoginRequiredMixin, FilterView):
    model = TaskStatus
    context_object_name = "status"
    template_name = "tasks/status/list.html"
    filterset_class = StatusFilter
    
    def get_paginate_by(self, queryset):
        # Get the value for paginate_by dynamically (e.g., from a form input or session)
        # Example: Set paginate_by to a user-selected value stored in session
        user_selected_value = self.request.session.get(
            "items_per_page", 10
        )  # Default to 10

        return user_selected_value
    

class StatusDetailView(LoginRequiredMixin, DetailView):
    model = TaskStatus
    template_name = "tasks/status/detail.html"
    context_object_name = "status"


class StatusCreateView(LoginRequiredMixin, CreateView):
    template_name = "tasks/status/create.html"
    form_class = CreateTaskStatusForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("tasks:detail_status", kwargs={"pk": self.object.pk})


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = TaskStatus
    fields = ("name", "description", "is_active")
    template_name = "tasks/status/update.html"

    def get_success_url(self):
        return reverse_lazy("tasks:detail_status", kwargs={"pk": self.object.pk})


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskStatus
    template_name = "tasks/status/delete.html"
    success_url = reverse_lazy("tasks:list_status")

    def get(self, request, *args, **kwargs):
        # Get the object to be deleted
        self.object = self.get_object()

        # Perform the delete operation directly without displaying a confirmation template
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(
                self.request, f"Status  successfully Deleted!"
            )
        return HttpResponseRedirect(success_url)


class ChangeStatusView(LoginRequiredMixin, UpdateView):
    template_name = "tasks/status/change_status.html"
    model = Task
    fields = ("status",)

    def form_valid(self, form):
        task = form.save(commit=False)
        task.save()

        TaskLog.objects.create(
            task=task,
            user=self.request.user,
            event_type="Status Change",
            additional_info=f"{self.request.user} Set '{task.status}' Status for {task}",
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("tasks:detail", kwargs={"pk": self.object.pk})
