# Yan Pan
# python -m pytest -v -s
# relative path warning: only work using "python -m pytest" simply "pytest" may not work
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient

from ..main import app
from settings.settings import Settings

settings = Settings()


class TestAuth:
    """
    Unittest for auth control, user role 0 means admin
    """

    fake_user = "fake-user-001"
    fake_admin = "fake-admin-001"
    fake_password = "an-awful-123-password"

    def setup_method(self):
        self.client = TestClient(app)        

    def test_user_creation(self):
        for u, r in [(self.fake_user, [1]), (self.fake_admin, [0,1])]:
            response = self.client.post("/auth/register", json={
                "username": u,
                "email": "XXXXXXXXX@email.domain",
                "full_name": "I don't have a full name",
                "roles": r,
                "password": self.fake_password
            })
            assert response.status_code == 201

    def test_deny_anonymous(self):
        response = self.client.get(f"/admin/user/me")
        assert response.status_code in [401, 403]

    def test_deny_anonymous_and_non_admin(self):
        response = self.client.get(f"/admin/list-users")
        assert response.status_code in [401, 403]

    def test_deny_wrong_username_password(self):
        """
        no token if login challenge failed
        not that /token require a form data
        """
        response = self.client.post(f"/auth/token", data={
            "username": self.fake_user,
            "password": "wrong-password"
        })
        assert response.status_code in [401, 403]
        assert "access_token" not in response.json()

    def test_deny_forged_token(self):
        """
        provided a forged/wrong token shall not grant access
        """
        token = "eyJhbGciOixxIUzI1NiIsInR5cCI6IkpXVCJ9.eyJxxWIiOiJmYWtlLXVzZXItMSIsImV4cCI6MTY4Nzc2MTg0NH0.YrZfAmLYihSvnhqt5iMk8brfIL_X4otzQgWvIfjK1io"
        response = self.client.get(f"/admin/user/me", headers={
            "Authorization": f"Bearer {token}"
        })
        assert response.status_code in [401, 403]

    def test_allow_check_myself(self):
        """
        with token, any user is able to determine WhoAmI
        """
        for u in [self.fake_user, self.fake_admin]:
            response = self.client.post(f"/auth/token", data={
                "username": u,
                "password": self.fake_password
            })
            token = response.json()["access_token"]
            response = self.client.get(f"/admin/user/me", headers={
                "Authorization": f"Bearer {token}"
            })
            assert response.status_code == 200
            assert response.json()["username"] == u

    def test_deny_non_admin_list_users(self):
        """
        /admin endpoints requires user have admin role (number 0)
        """
        response = self.client.post(f"/auth/token", data={
                "username": self.fake_user,
                "password": self.fake_password
            })
        token = response.json()["access_token"]
        response = self.client.get(f"/admin/list-users", headers={
            "Authorization": f"Bearer {token}"
        })
        assert response.status_code in [401, 403]

    def test_allow_admin_list_user(self):
        response = self.client.post(f"/auth/token", data={
            "username": self.fake_admin,
            "password": self.fake_password
        })
        token = response.json()["access_token"]
        response = self.client.get(f"/admin/list-users", headers={
            "Authorization": f"Bearer {token}"
        })
        print(response.json())
        assert response.status_code == 200
