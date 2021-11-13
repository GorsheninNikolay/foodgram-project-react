import django_filters

from .models import User


class SubscriptionsFilter(django_filters.FilterSet):
    limit = django_filters.NumberFilter(method='limit_filter')

    class Meta:
        model = User
        fields = ('limit', )

    def limit_filter(self, queryset, name, value):
        return queryset[:value]
