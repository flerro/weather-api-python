import json
import sys

from models import WeatherEvent


def weather_import(event, context):
    try:
        items = json.loads(event['body'])
        if isinstance(items, list):
            for item in items:
                WeatherEvent(**item).save()
        else:
            w = WeatherEvent(**items)
            w.save()

        return apigw_response(200, "")

    except KeyError as k:
        return bad_request("Invalid request, %s" % str(k))

    except Exception as e:
        print(e, sys.exc_info()[0])
        return server_error()


def weather_by_location(event, context):
    try:
        location = event['queryStringParameters']['loc']
        event = WeatherEvent.get(location)
        if not event:
            return not_found("No item for location name: %s" % location)

        return apigw_response(200, event.to_json())

    except Exception as e:
        print(e, sys.exc_info()[0])
        return server_error()


def server_error(msg = "Unhandled error"):
    return apigw_response(500, {"message": msg})


def bad_request(msg):
    return apigw_response(400, {"message": msg})


def not_found(msg):
    return apigw_response(404, {"message": msg})


def apigw_response(code, payload):
    return {"statusCode": code, "body": jsonpickle.encode(payload)}
