import requests_mock
from app import fetch_quote, app


def test_fetch_quote_success():
    mock_response = [
        {
            "q": "Test quote",
            "a": "Test author"
        }
    ]

    with requests_mock.Mocker() as m:
        m.get("https://zenquotes.io/api/random",
              json=mock_response, status_code=200)
        data = fetch_quote()

        assert data is not None
        assert data["quote"] == "Test quote"
        assert data["author"] == "Test author"


def test_index_route():
    client = app.test_client()

    with requests_mock.Mocker() as m:
        m.get(
            "https://zenquotes.io/api/random",
            json=[{"q": "Hello CI/CD", "a": "DevOps"}],
            status_code=200
        )
        response = client.get("/")
        html = response.data.decode("utf-8")

        assert response.status_code == 200
        assert "Hello CI/CD" in html
        assert "DevOps" in html
