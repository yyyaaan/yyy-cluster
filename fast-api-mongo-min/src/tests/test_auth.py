# Yan Pan
# python -m pytest -v -s
# relative path warning: only work using "python -m pytest" simply "pytest" may not work  # noqa
from fastapi.testclient import TestClient

from ..main import app
from settings.settings import Settings
# special import in code level if allow_public_registration is False
settings = Settings()


class TestAuth:
    """
    Unittest for auth control, user role 0 means admin
    """

    allow_public_registration = False
    fake_user = "fake-user-001"
    fake_admin = "fake-admin-001"
    fake_password = "an-awful-123-password"

    def setup_method(self):
        self.client = TestClient(app)

    def teardown_class(cls):
        """
        teardown test - remove the fake_admin user
        """
        client = TestClient(app)
        response = client.post("/auth/token", data={
            "username": cls.fake_admin,
            "password": cls.fake_password
        })
        token = response.json()["access_token"]
        response_deletion = client.delete(
            url=f"/admin/user/{cls.fake_admin}",
            headers={"Authorization": f"Bearer {token}"}
        )
        print(
            "\n>>> TestAuth tearing down completed",
            response_deletion.status_code == 204
        )

    def test_user_creation(self):
        """
        when public registration is closed, a DB-registered super is used
        """
        # create a super user in DB (API forbids) that can register user
        if not self.allow_public_registration:
            from asyncio import run
            from auth.JWT import create_user, create_access_token
            from auth.schemas import UserWithPassword
            super_user = UserWithPassword(**{
                "username": "super",
                "email": "super@super.super",
                "full_name": "Superuser Creation",
                "roles": [0, 1],
                "password": "this-is-A-bad-passwo3d"
            })
            run(create_user(super_user))
            token = create_access_token({"sub": "super"})["access_token"]

        for u, r in [(self.fake_user, [1]), (self.fake_admin, [0, 1])]:
            response = self.client.post(
                url="/auth/register",
                json={
                    "username": u,
                    "email": f"{u}@email.domain",
                    "full_name": f"{u} is a full name",
                    "roles": r,
                    "password": self.fake_password
                },
                headers={} if self.allow_public_registration else {"Authorization": f"Bearer {token}"}  # noqa: E501
            )
            assert response.status_code == 201

    def test_deny_anonymous(self):
        response = self.client.get("/admin/user/me")
        assert response.status_code in [401, 403]

    def test_deny_anonymous_and_non_admin(self):
        response = self.client.get("/admin/list-users")
        assert response.status_code in [401, 403]

    def test_deny_wrong_username_password(self):
        """
        no token if login challenge failed
        not that /token require a form data
        """
        response = self.client.post("/auth/token", data={
            "username": self.fake_user,
            "password": "wrong-password"
        })
        assert response.status_code in [401, 403]
        assert "access_token" not in response.json()

    def test_deny_forged_token(self):
        """
        provided a forged/wrong token shall not grant access, nor token refresh
        """
        token = "eyJhbGciOixxIUzI1NiIsInR5cCI6IkpXVCJ9.eyJxxWIiOiJmYWtlLXVzZXItMSIsImV4cCI6MTY4Nzc2MTg0NH0.YrZfAmLYihSvnhqt5iMk8brfIL_X4otzQgWvIfjK1io"  # noqa
        response = self.client.get(
            url="/admin/user/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code in [401, 403]
        response_refresh = self.client.post(
            url="/auth/token/refresh",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response_refresh.status_code in [401, 403]

    def test_allow_check_myself(self):
        """
        with token, any user is able to determine WhoAmI
        """
        for u in [self.fake_user, self.fake_admin]:
            response = self.client.post("/auth/token", data={
                "username": u,
                "password": self.fake_password
            })
            token = response.json()["access_token"]
            response = self.client.get(
                url="/admin/user/me",
                headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 200
            assert response.json()["username"] == u

    def test_refreshed_token(self):
        """
        refresh an token and test access
        """
        for u in [self.fake_user, self.fake_admin]:
            response = self.client.post("/auth/token", data={
                "username": u,
                "password": self.fake_password
            })
            token_original = response.json()["access_token"]
            token_refreshed = self.client.post(
                url="/auth/token/refresh",
                headers={"Authorization": f"Bearer {token_original}"}
            ).json()["access_token"]

            response = self.client.get(
                url="/admin/user/me",
                headers={"Authorization": f"Bearer {token_refreshed}"}
            )
            assert response.status_code == 200
            assert response.json()["username"] == u

    def test_deny_non_admin_list_users(self):
        """
        /admin endpoints requires user have admin role (number 0)
        """
        response = self.client.post("/auth/token", data={
                "username": self.fake_user,
                "password": self.fake_password
            })
        token = response.json()["access_token"]
        response = self.client.get(
            url="/admin/list-users",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code in [401, 403]

    def test_allow_admin_list_user(self):
        response = self.client.post("/auth/token", data={
            "username": self.fake_admin,
            "password": self.fake_password
        })
        token = response.json()["access_token"]
        response = self.client.get(
            url="/admin/list-users",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_destroy_users(self):
        """
        use admin token, destroy both user created.
        """
        response = self.client.post("/auth/token", data={
            "username": self.fake_admin,
            "password": self.fake_password
        })
        token = response.json()["access_token"]
        response_deletion = self.client.delete(
            url=f"/admin/user/{self.fake_user}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response_deletion.status_code == 204

        # confirm remaining user does not have deleted one
        response_list_users = self.client.get(
            url="/admin/list-users",
            headers={"Authorization": f"Bearer {token}"}
        )
        r_users = [x.get("username", "") for x in response_list_users.json()]
        assert self.fake_admin in r_users     # admin is still there
        assert self.fake_user not in r_users  # user has been deleted
