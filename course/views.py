import operator
from datetime import datetime
# import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.views.generic import ListView, DetailView
from functools import reduce

from .models import Subject, Note, Rating, OnlineLecture, Discussion

from django.db.models import Q

from django.http import JsonResponse

class NotelistView(DetailView):
    model = Subject
    template_name = 'note_list.html'
    extra_context = {'subject_name': 'Math'}
    pk_url_kwarg = 'pk'

    # def get_queryset(self):
    #     result = super().get_queryset().order_by('rating'
    #     return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['notes'] = self.get_object().note_set.all()
        print(context['notes'])
        return context

class SubjectListView(ListView):
    model = Subject
    template_name = 'subject_list.html'
    context_object_name = 'subjects'




class SubjectSearchListView(SubjectListView):
    """
    Display a Blog List page filtered by the search query.
    """
    # paginate_by = 10
    template_name = 'home.html'
    context_object_name = None

    def get_queryset(self):
        result = super().get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list))
            )
            self.context_object_name = 'subjects'

        return result

def home(request):
    return render(request, 'home.html', {})

def rating(request, pk=None):
    data = {}
    if request.user.is_authenticated:
        obj = Rating.objects.get(user=request.user, note__pk=pk)
        print(obj.count)
        if obj.count < 5:
            obj.count +=1
            obj.save()
        data['count'] = obj.count
    else:
        data['error-message'] = "Please Login To Rate"
    return JsonResponse(data)

def download(request, pk=None):
    data = {}
    if request.is_ajax():
        obj = Note.objects.get(pk=pk)
        obj.download += 1
        obj.save()
        data = {'download': obj.download }
    return JsonResponse(data)

def clap(request):
    return render(request, 'clap.html', {})

def string_capture(request,  name=None):
    return HttpResponse(name)


def online_class_list(request):
    upcoming_classes = OnlineLecture.objects.all().filter(start_at__gte=datetime.now())
    previous_classes = OnlineLecture.objects.all().filter(start_at__lte=datetime.now())
    template_name = 'online_class_list.html'
    context = {
    'upcoming_classes': upcoming_classes,
    'previous_classes': previous_classes,
    }

    return render(request, template_name, context)


def online_class_attend(request, pk=None):
    obj = OnlineLecture.objects.get(pk=pk)

    template_name = 'onlineclass.html'
    context = {
    'live_lecture': obj,
    }
    return render(request, template_name, context)
