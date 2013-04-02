import string
from random import choice

import redis

from django.http import HttpResponse, HttpResponseMethodNotAllowed, HttpResponseNotFound
from django.shortcuts import redirect

def get_redis():
    return redis.Redis()


def random_string(length, chars=string.letters+string.digits):
    return "".join(choice(chars) for i in xrange(length))

def short_link(request, short_path):
    full_path = get_redis().get(short_path)
    return redirect(full_path) if full_path else HttpResponseNotFound("Not found")

def shorten(request):

    if request.method == 'POST':
        full_path = request.POST['link']
        r = get_redis()
        short_path = random_string(5)

        while r.exists(short_path):
            short_path = random_string(5)

        r.set(short_path, full_path)
        return redirect(request.build_absolute_uri(short_path))

    return HttpResponseMethodNotAllowed(['POST'])

