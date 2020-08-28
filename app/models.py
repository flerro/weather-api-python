import json
import os
import datetime
from json import JSONEncoder

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, MapAttribute
from botocore.session import Session

locationTable = os.getenv('LOCATIONS_TABLE')
defaultRegion = Session().get_config_variable('region')


class ModelEncoder(JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'attribute_values'):
            return obj.attribute_values
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


class GeoPoint(MapAttribute):
    lat = NumberAttribute(default=0)
    lng = NumberAttribute(default=0)


class WeatherEvent(Model):

    class Meta:
        table_name = locationTable if locationTable else "locationsTable"
        region = defaultRegion
        # host = "http://localhost:8000"  # Local testing

    location_name = UnicodeAttribute(hash_key=True)
    temperature = NumberAttribute(default=0)
    timestamp = UnicodeAttribute(default="")
    position = GeoPoint()

    def to_json(self):
        return json.dumps(self, cls=ModelEncoder)


if __name__ == '__main__':
    if not WeatherEvent.exists():
         WeatherEvent.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)


    w = WeatherEvent(
          location_name="Oxford, UK",
          temperature=64,
          timestamp="1564428898",
          position=GeoPoint(lat=51.75,lng=-1.25))

    w.save()

    print(w.to_json())