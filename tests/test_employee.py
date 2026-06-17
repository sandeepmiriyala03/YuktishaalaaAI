from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_department():

    response = client.post(
        "/department",
        json={
            "departmentName": "TEST Department",
            "location": "  Test Location"
        }
    )

    assert response.status_code == 200

    assert response.json() == {
        "message": "Department Created"
    }


def test_create_employee():

    response = client.post(
        "/employee",
        json={
            "name": "Test Employee",
            "salary": 50000,
            "age": 35,
            "departmentId": 1
        }
    )

    assert response.status_code == 200

    assert response.json() == {
        "message": "Test Employee Created"
    }