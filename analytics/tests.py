import json
from datetime import datetime
from django.test import TestCase
from django.utils.timezone import timedelta

from analytics.models import Analytic
from analytics.services.create_analytic_metadata_service import CreateAnalyticMetadata
from core.models import User

test_user = {
    "name": "John",
    "last_name": "Doe Doe",
    "username": "johndoe",
    "password": "123456",
    "birth_date": datetime.now(),
    "state": "RJ",
    "cellphone": "2131323",
    "email": "johndoe@allpetsenior.com"
}


class FakeAnalyticRepo:
    def create_analytics(self, data):
        return Analytic(**data)


class AnalyticTestCase(TestCase):
    def setUp(self):
        self.test_user = User(test_user)
        self.AnalyticRepo = FakeAnalyticRepo()

    def test_create_analytic(self):
        """Analytic with the correct metadata"""
        timestamp = datetime.now() - timedelta(days=30)
        metadata = json.dumps({"page": "HOME", "timestamp": timestamp})
        payload = dict()
        payload["metadata"] = json.dumps(metadata)
        payload["user"] = self.test_user

        CreateMetadata = CreateAnalyticMetadata(self.AnalyticRepo)

        CreateMetadata.execute(payload)
