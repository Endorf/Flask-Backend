import pytest
from app.password_grand_type.views import app
from app.service.common import status


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK


def test_health(client):
    """ It should be healthy """
    response = client.get('/health')
    assert response.status_code == status.HTTP_200_OK


if __name__ == '__main__':
    pytest.main()
