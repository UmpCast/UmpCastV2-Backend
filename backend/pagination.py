from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_page_size(self, request):
        if self.page_size_query_param:
            try:
                page_size =  pagination._positive_int(
                    request.query_params[self.page_size_query_param],
                    strict=True,
                    cutoff=self.max_page_size
                )
                self.page_size = page_size
                return self.page_size
            except (KeyError, ValueError):
                pass
        return self.page_size

    def get_paginated_response(self, data):
        return Response({
            'page_size': self.page_size,
            'max_page_size': self.max_page_size,
            'page_number': self.page.number,
            'count': self.page.paginator.count,
            'results': data
        })
