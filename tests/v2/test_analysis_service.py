from api.v2.services.analysis_service import analysis_service


def test_complete_sample_data_functions():
    number_of_samples = 5
    for i in range(1, number_of_samples + 1):
        response = analysis_service.get_sample_data(f"sample-{i}")
        assert response is not None


def test_get_sample_data():
    response = analysis_service.get_sample_data("sample-1")
    assert "data" in response
    assert "min_rating" in response
    assert "max_rating" in response
    assert len(response["data"]) > 0
