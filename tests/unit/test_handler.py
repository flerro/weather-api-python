import json

import pytest

from app import handlers
from app.models import WeatherEvent
from moto import mock_dynamodb2


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
        "body": '{'
                ' "location_name": "Oxford, UK", '
                ' "temperature": 64, '
                ' "timestamp": "1564428898", '
                ' "position": {"lat": 51.75, "lng": -1.25}'
                '}',
        "resource": "/{proxy+}",
    }

@pytest.fixture()
def badreq_event():
    """ Generates API GW Event"""

    return {
        "body": '{'
                ' "invalid_name": "Oxford, UK", '
                ' "temperature": 64, '
                ' "timestamp": "1564428898", '
                ' "position": {"lat": 51.75, "lng": -1.25}'
                '}',
        "resource": "/{proxy+}",
    }


def test_import_badrequest(badreq_event):
    ret = handlers.weather_import(badreq_event, "")
    assert ret["statusCode"] == 400   # ValueError
    assert "message" in ret["body"]
    response = json.loads(ret["body"])
    assert response["message"] == "Invalid request, Attribute invalid_name specified does not exist"


@mock_dynamodb2
def test_import_handler(apigw_event):
    WeatherEvent.create_table(wait=True)
    ret = handlers.weather_import(apigw_event, "")
    assert ret["statusCode"] == 200
    assert ret["body"] == ""

    a = WeatherEvent.get("Oxford, UK")
    assert a.timestamp == "1564428898"

