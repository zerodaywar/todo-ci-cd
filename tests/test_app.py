import os
import tempfile

import pytest

from app import app


@pytest.fixture
def client():

    db_fd, db_path = tempfile.mkstemp()

    app.config["TESTING"] = True

    import app as application

    application.DATABASE = db_path

    with app.test_client() as client:
        application.init_db()
        yield client

    os.close(db_fd)
    os.unlink(db_path)


def test_homepage(client):

    response = client.get("/")

    assert response.status_code == 200


def test_add_todo(client):

    response = client.post(
        "/api/todos",
        json={"title": "Learn CI/CD"}
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["title"] == "Learn CI/CD"


def test_empty_todo_rejected(client):

    response = client.post(
        "/api/todos",
        json={"title": ""}
    )

    assert response.status_code == 400
