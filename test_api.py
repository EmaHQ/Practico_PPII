from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_questions():
    response = client.get("/questions?limit=3")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_stats():
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_questions" in data
    assert "by_category" in data


def test_create_question_post():
    payload = {
        "question": "¿Cuál es la capital de Francia?",
        "answer": "París",
        "category": "geografia",
        "source": "test",
    }
    response = client.post("/questions", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["question"] == payload["question"]
    assert "id" in data