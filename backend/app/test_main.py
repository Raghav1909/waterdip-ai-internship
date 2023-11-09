from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_get_total_visitors_in_range():
    response = client.get("/visitors?start_date=2015-07-01&end_date=2015-07-03")
    assert response.status_code == 200
    assert response.json() == {
  "adults": [
    62,
    68,
    73
  ],
  "children": [
    1,
    4,
    4
  ],
  "babies": [
    0,
    0,
    0
  ],
  "total": [
    {
      "x": "2015-07-01",
      "y": 63
    },
    {
      "x": "2015-07-02",
      "y": 72
    },
    {
      "x": "2015-07-03",
      "y": 77
    }
  ]
}


def test_get_total_visitors_in_wrong_range():
    response = client.get("/visitors?start_date=2015-07-01&end_date=2014-08-09")
    assert response.status_code == 400
    assert response.json() == {"detail": "Start date cannot be greater than end date"}


def test_get_visitors_by_country():
    response = client.get("/visitors/country")
    assert response.status_code == 200
    assert response.json() == {
  "countries": ["PRT", "GBR", "USA", "ESP", "IRL", "FRA", "NULL", "ROU", "NOR", "OMN", "ARG", "POL", "DEU", "BEL", "CHE", "CN", "GRC", "ITA", "NLD", "DNK", "RUS", "SWE", "AUS", "EST", "CZE", "BRA", "FIN", "MOZ", "BWA", "LUX", "SVN", "ALB", "IND", "CHN", "MEX"],
  "visitorPercentage": [65.6, 7.4, 1.7, 11.3, 3.3, 1.9, 0, 0.6, 0.4, 0.1, 0.2, 0.5, 0.4, 0.4, 0.9, 0.9, 0.1, 0.2, 0.3, 0.5, 0.7, 0.3, 0.2, 0.2, 0.1, 0.4, 0.3, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
}


def test_get_visitors_by_country_in_wrong_range():
    response = client.get("/visitors/country?start_date=2015-07-01&end_date=2014-08-09")
    assert response.status_code == 400
    assert response.json() == {"detail": "Start date cannot be greater than end date"}