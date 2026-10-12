
def create_work_order(client, title="Fix login issue"):
    return client.post(
        "/work-orders/",
        json={
            "title": title,
            "description": "Investigate login failure",
        },
    )


def test_create_work_order(client):
    response = create_work_order(client)

    assert response.status_code == 201

    data = response.json()
    assert data["id"] is not None
    assert data["title"] == "Fix login issue"
    assert data["status"] == "OPEN"
    assert "created_at" in data


def test_create_work_order_invalid_title(client):
    response = create_work_order(client, title="Hi")

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_get_work_order(client):
    created = create_work_order(client)
    work_order_id = created.json()["id"]

    response = client.get(f"/work-orders/{work_order_id}")

    assert response.status_code == 200
    assert response.json()["id"] == work_order_id


def test_get_missing_work_order(client):
    response = client.get("/work-orders/99999")

    assert response.status_code == 404
    assert (
        response.json()["error"]["code"]
        == "WORK_ORDER_NOT_FOUND"
    )


def test_list_work_orders(client):
    create_work_order(client, title="Fix login issue")
    create_work_order(client, title="Update dashboard")

    response = client.get("/work-orders/")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["title"] == "Fix login issue"
    assert response.json()[1]["title"] == "Update dashboard"


def test_update_work_order_status(client):
    created = create_work_order(client)
    work_order_id = created.json()["id"]

    response = client.patch(
        f"/work-orders/{work_order_id}/status",
        json={"status": "IN_PROGRESS"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "IN_PROGRESS"

    # Verify that the update persisted
    fetched = client.get(f"/work-orders/{work_order_id}")
    assert fetched.json()["status"] == "IN_PROGRESS"


def test_update_work_order_invalid_status(client):
    created = create_work_order(client)
    work_order_id = created.json()["id"]

    response = client.patch(
        f"/work-orders/{work_order_id}/status",
        json={"status": "WAITING"},
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"