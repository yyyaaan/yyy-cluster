# Yan Pan
# python -m pytest -v
# relative path warning: only work using "python -m pytest" simply "pytest" may not work
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from settings.settings import Settings

from ..main import app

class TestRoadMap:
    """
    The tests can use the normal database. All creation will be destroyed.
    """

    router = "/roadmap"
    fake_id = "this_is_a_fake_id_for_test_only"

    @classmethod
    def setup_method(self):
        settings = Settings()
        app.mongodb_client = AsyncIOMotorClient(settings.MONGO_URL)
        app.mongodb = app.mongodb_client[settings.MONGO_DB_NAME]
        app.collection_roadmap = app.mongodb["roadmaps"]
        self.client = TestClient(app)

    def test_reachable(self):
        response = self.client.get(f"{self.router}/")
        assert response.status_code == 200

    def test_list_roadmaps(self):
        response = self.client.get(f"{self.router}/list")
        assert response.status_code == 200
        assert type(response.json()) == list

    def test_create_roadmap(self):
        response = self.client.post(f"{self.router}/create", json={
            "_id": self.fake_id, "title": "test", "description": "test", "items": []
        })
        assert response.status_code == 201

    def test_delete_roadmap(self):
        response = self.client.delete(f"{self.router}/delete/{self.fake_id}")
        assert response.status_code == 202