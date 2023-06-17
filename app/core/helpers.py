from fastapi import Query

from app.core.middlewares import request_object


class PaginationParams:
    def __init__(self, page: int = Query(1, ge=1), per_page: int = Query(13, ge=0)):
        self.page = page
        self.per_page = per_page
        self.limit = per_page * page
        self.offset = (page - 1) * per_page


class Paginator:
    def __init__(self, page: int, per_page: int, count: int, items):
        self.page: int = page
        self.per_page: int = per_page
        self.count: int = count
        self.items = items
        self.next_page: str = ''
        self.previous_page: str = ''
        self.total_page_count: int = 0
        self.request = request_object.get()

    def _get_next_page(self):
        if self.page >= self.total_page_count:
            return None

        url = self.request.url.include_query_params(page=self.page + 1)

        return str(url)

    def _get_previous_page(self):
        if self.page == 1 or self.page > self.total_page_count + 1:
            return None

        url = self.request.url.include_query_params(page=self.page - 1)

        return str(url)

    def _get_number_of_pages(self, total_count: int):
        remainder = total_count % self.per_page
        number_of_pages = total_count // self.per_page

        return number_of_pages if not remainder else number_of_pages + 1

    def _get_total_count(self):
        self.total_page_count = self._get_number_of_pages(self.count)

        return self.count

    def get_response(self):
        return {
            'count': self._get_total_count(),
            'next_page': self._get_next_page(),
            'previous_page': self._get_previous_page(),
            'items': self.items
        }


def paginate(page: int, per_page: int, count: int, items):
    paginator = Paginator(page=page, per_page=per_page, count=count, items=items)

    return paginator.get_response()
