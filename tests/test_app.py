import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.core.config import Settings
from app.main import create_app


def test_environment_overrides_dotenv(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text('MEDILUX_APP_NAME="File settings"\n', encoding="utf-8")
    monkeypatch.setenv("MEDILUX_APP_NAME", "Environment settings")
    monkeypatch.setenv("MEDILUX_CORS_ORIGINS", '["http://localhost:5173/"]')

    settings = Settings(_env_file=env_file)

    assert settings.app_name == "Environment settings"
    assert settings.cors_origins == ["http://localhost:5173"]


@pytest.mark.parametrize(
    "origin", ["*", "http://localhost:5173/path", "http://user:pass@localhost:5173"]
)
def test_invalid_cors_origins_fail_at_startup(origin):
    with pytest.raises(ValidationError):
        Settings(_env_file=None, cors_origins=[origin])


def test_frontend_can_read_health_and_api_schema():
    settings = Settings(_env_file=None, cors_origins=["http://localhost:5173"])
    with TestClient(create_app(settings)) as client:
        response = client.get("/api/v1/health", headers={"Origin": "http://localhost:5173"})
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
        assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
        assert "/api/v1/health" in client.get("/openapi.json").json()["paths"]


def test_unlisted_origin_fails_cors_preflight():
    with TestClient(create_app(Settings(_env_file=None, cors_origins=[]))) as client:
        response = client.options(
            "/api/v1/health",
            headers={
                "Origin": "https://unlisted.example",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.status_code == 400
        assert "access-control-allow-origin" not in response.headers


def test_docs_can_be_disabled_without_disabling_health():
    settings = Settings(_env_file=None, docs_enabled=False)
    with TestClient(create_app(settings)) as client:
        for path in ("/docs", "/redoc", "/openapi.json"):
            assert client.get(path).status_code == 404
        assert client.get("/api/v1/health").status_code == 200
