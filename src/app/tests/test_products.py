from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_list_products():
    # setup
    products = [
        {"id": f"abc{i}cba", "name": f"name {i}", "price": i * 10} for i in range(10)
    ]
    for p in products:
        client.post("/products/", json=p)

    response = client.get("/products/", params={"limit": 5, "offset": 0})
    assert response.status_code == 200
    assert response.json() == products[:5]

    response = client.get("/products/", params={"limit": 5, "offset": 5})
    assert response.status_code == 200
    assert response.json() == products[5:]

    # clean up
    for p in products:
        client.delete(f"/products/{p['id']}")


def test_create_product():
    new_product = {
        "id": "10525022",
        "name": "【Apple 蘋果】iPhone 14 128G(6.1吋)",
        "price": 26784
    }

    response = client.post("/products/", json=new_product)
    assert response.status_code == 200

    response = client.get("/products/10525022")
    assert response.json() == new_product

    # clean up
    client.delete("/products/10525022")


def test_update_product():
    # setup
    new_product = {
        "id": "10525022",
        "name": "【Apple 蘋果】iPhone 14 128G(6.1吋)",
        "price": 26784
    }
    response = client.post("/products/", json=new_product)

    response = client.put("/products/10525022", json={"price": 100})
    assert response.status_code == 200
    assert response.json()["price"] == 100

    response = client.put("/products/10525022", json={"name": "new name"})
    assert response.status_code == 200
    assert response.json()["name"] == "new name"

    # clean up
    client.delete("/products/10525022")


def test_rud_not_exist_product():
    not_exist_id = "abcdefg"
    response = client.delete(f"/products/{not_exist_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

    response = client.put(f"/products/{not_exist_id}", json={"price": 100})
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

    response = client.get(f"/products/{not_exist_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_c_when_product_id_exists():
    # setup
    new_product = {
        "id": "10525022",
        "name": "【Apple 蘋果】iPhone 14 128G(6.1吋)",
        "price": 26784
    }
    client.post("/products/", json=new_product)

    another_product = {
        "id": "10525022",
        "name": "testtest",
        "price": 100
    }
    response = client.post("/products/", json=another_product)
    assert response.status_code == 400
    assert response.json() == {"detail": "Product id already exists"}

    # clean up
    client.delete("/products/10525022")
