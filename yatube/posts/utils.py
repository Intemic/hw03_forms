from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpRequest


def get_page_obj(request: HttpRequest, list_object: list) -> Paginator:
    paginator = Paginator(list_object, settings.NUMBER_OF_LINES_ON_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
