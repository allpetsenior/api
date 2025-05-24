from analytics.models import Analytic


class AnalyticsRepository:
    def create_analytics(self, data):
        return Analytic.objects.create(**data)
