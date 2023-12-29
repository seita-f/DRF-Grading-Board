"""
Filters for post APIs
"""
import django_filters
from core.models import (
    Post,
)


class PostFilter(django_filters.FilterSet):
    """ Define fileds for filtering """
    # Note: filed_name = {ForeignKey}__{name of field}
    shcool = django_filters.CharFilter(field_name='shcool__name',lookup_expr='contains')
    faculty = django_filters.CharFilter(field_name='faculty__name', lookup_expr='contains')
    _class = django_filters.CharFilter(field_name='_class__name', lookup_expr='contains')
    professor = django_filters.CharFilter(field_name='professor__name', lookup_expr='contains')
    created_at = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Post
        fields = ['school', 'faculty', '_class', 'professor', 'created_at']
