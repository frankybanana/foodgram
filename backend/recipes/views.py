from django.http import HttpResponseNotFound, HttpResponseRedirect
from hashids import Hashids

from foodgram_backend.constants import MIN_LENGTH_FOR_SHORT_URL, SALT

hashids = Hashids(min_length=MIN_LENGTH_FOR_SHORT_URL, salt=SALT)


def get_hashed_short_url(value):
    return hashids.encode(value)


def get_decoded_short_url(value):
    return hashids.decode(value)


def handle_short_url(request, short_url):
    try:
        decoded_values = get_decoded_short_url(short_url)
        if decoded_values:
            recipe_id = decoded_values[0]
            return HttpResponseRedirect(request.build_absolute_uri
                                        (f'/recipes/{recipe_id}/'))
        return HttpResponseNotFound('Проверьте URL-адрес')
    except Exception as e:
        return HttpResponseNotFound(f'Произошла ошибка {e}')
