# Yan Pan
# relative path warning: only work using "python -m pytest" simply "pytest" may not work
from tests.client_helper import get_test_client

from ..app import app, get_db, BaseDbModel

client = get_test_client(app, get_db, BaseDbModel)

class TestRoadMap:

    def test_reachable(self):
        response = client.get("/")
        assert response.status_code == 200

    def test_create_roadmap(self):
        response = client.post("/roadmap", json={"id": -1, "title": "test", "description": "test"})
        assert response.status_code == 201
        assert "id" in response.json()

    def test_delete_roadmap(self):
        response = client.delete("/roadmap/-1")
        assert response.status_code == 202

    def test_get_roadmaps(self):
        response = client.get("/roadmap")
        assert response.status_code == 200
        assert type(response.json()) == list
