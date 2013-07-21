# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View
from apps.pinger.forms import UploadFileForm, HaystackCreateModelForm
from apps.pinger.models import Haystack
from django.core.urlresolvers import reverse_lazy
from apps.util.mixins import MessageMixin

class HaystackUploadView(TemplateResponseMixin, ContextMixin, View):
    form_class = UploadFileForm
    template_name = 'pinger/haystack_upload.html'
    success_url = reverse_lazy('hay_list')

    def get(self, request, *args, **kwargs):
        return self.render_to_response(
            self.get_context_data(form=self.form_class()))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            #if file is valid, transfer contents to db
            _file = form.cleaned_data["file"]
            for line in _file:
                self.line_to_haystack(line)
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def line_to_haystack(self, line):
        try:
            (url, phrase, name) = line.split('|')
        except ValueError:
            (url, phrase) = line.split('|')
            name = None
        straw = Haystack(
            url=url,
            search_phrase=phrase,
            name=name,
        )
        straw.save()

class HaystackListView(ListView):
    model = Haystack

class HaystackCreateView(MessageMixin, CreateView):
    model = Haystack
    form_class = HaystackCreateModelForm
    success_message='Added new item!'
    success_url = reverse_lazy('hay_list')

class HaystackUpdateView(MessageMixin, UpdateView):
    model = Haystack
    form_class = HaystackCreateModelForm
    success_message='Data was successfully edited'
    success_url = reverse_lazy('hay_list')

class HaystackDeleteView(MessageMixin, DeleteView):
    model = Haystack
    success_message='Link was removed from monitoring system.'
    success_url = reverse_lazy('hay_list')