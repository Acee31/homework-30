from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_recipe():
    resp = client.post(
        "/recipes", json={"title": "Пицца", "description": "Мясная", "cooking_time": 30}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "id" in data
    assert data["title"] == "Пицца"


def test_get_all_recipe():
    client.post(
        "/recipes", json={"title": "Пицца", "description": "Мясная", "cooking_time": 30}
    )

    resp = client.get("/recipes")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    first_recipe = data[0]
    assert "id" in first_recipe
    assert "title" in first_recipe


def test_get_recipe_by_id():
    create_resp = client.post(
        "/recipes", json={"title": "Пицца", "description": "Мясная", "cooking_time": 30}
    )
    id = create_resp.json()["id"]
    resp1 = client.get(f"/recipes/{id}")

    assert resp1.status_code == 200
    assert resp1.json()["views"] == 1

    resp2 = client.get(f"/recipes/{id}")
    assert resp2.status_code == 200
    assert resp2.json()["views"] == 2


def test_get_recipe_not_found():
    id = 1000000000
    resp = client.get(f"/recipes/{id}")
    assert resp.status_code == 404
    assert resp.json()["detail"] == f"Рецепт с id - {id} не найден"
