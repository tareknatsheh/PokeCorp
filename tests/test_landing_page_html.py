from fastapi.testclient import TestClient
from app import app

client  = TestClient(app)

def test_home_page_render():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<title>PokeCorp Dashboard</title>" in response.text
