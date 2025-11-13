from unittest.mock import patch


def test_analysis_endpoint(client):
    response = client.get("/v2/analysis/sample-1")
    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert len(body["data"]) > 0


def test_analysis_invalid_sample(client):
    response = client.get("/v2/analysis/foo")
    assert response.status_code == 200
    body = response.json()
    assert "error" in body


def test_query_endpoint(client):
    response = client.get("/v2/query")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) > 0


def test_query_select_one_column(client):
    response = client.get("/v2/query?select=title")
    assert response.status_code == 200
    body = response.json()
    assert len(body) > 0
    assert len(body[0]) == 1


@patch(
    "api.v2.services.chat_service.inference_service.use_hugging_face_pipeline",
    return_value="mock-response",
)
def test_chat_endpoint_with_mock(_mock_infer, client):
    response = client.post("/v2/chat?use_rag=false", json={"prompt": "Hi"})
    assert response.status_code == 200
    assert response.json() == "mock-response"
