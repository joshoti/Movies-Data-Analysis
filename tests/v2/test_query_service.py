from api.v2.services.query_service import query_service


def test_query_default():
    response = query_service.get_data({})
    assert len(response) > 0
    assert len(response) <= 30
    # Expect some known columns present
    assert "Movie_Title" in response[0]
    assert "Total_Gross" in response[0]


def test_query_with_select():
    query = {"select": "title"}
    response = query_service.get_data(query)
    assert len(response) > 0
    assert len(response[0].keys()) == 1
    assert "Movie_Title" in response[0]


def test_query_with_where():
    query = {"where": "AND-title-=-The Shawshank Redemption"}
    response = query_service.get_data(query)
    # One result expected
    assert len(response) == 1
    assert "Movie_Title" in response[0]


def test_query_with_select_and_where():
    query = {"select": "title", "where": "AND-title-=-The Shawshank Redemption"}
    response = query_service.get_data(query)
    assert len(response) == 1
    assert len(response[0].keys()) == 1
    assert "Movie_Title" in response[0]
