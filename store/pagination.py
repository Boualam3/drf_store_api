from rest_framework.pagination import PageNumberPagination

# because we remove this line below from the Setting of REST_FRAMEWORK we got a warning
# ? 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
# So we need to remove PAGE_SIZE from SETTINGS from REST_FRAMEWORK dictionary and implement our default pagination class that extends PageNumberPagination


class DefaultPagination(PageNumberPagination):
    page_size = 10
