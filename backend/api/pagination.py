from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10  # Количество объектов на одной странице по умолчанию
    page_size_query_param = 'limit'  # Название параметра для изменения размера страницы
    max_page_size = 100  # Максимальный размер страницы

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # Общее количество объектов
            'next': self.get_next_link(),  # Ссылка на следующую страницу
            'previous': self.get_previous_link(),  # Ссылка на предыдущую страницу
            'results': data  # Сами данные
        })
