# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import Comics
from .tasks import get_comics


def main(request):

    if 'comic' in request.GET:
        id = request.GET.get('comic')
        viewed_comic = Comics.objects.get(id=id)
        viewed_comic.viewed = True

        viewed_comic.save()
        comics = Comics.objects.filter(viewed=False)
        return render(request, 'main_template.html', {'comic_context': comics})

    get_comics()
    comics = Comics.objects.filter(viewed=False)
    return render(request, 'main_template.html', {'comic_context': comics})
