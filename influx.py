import logger

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class DBClient:
    def __init__(self, host: str, port: str, user: str, token: str, org: str, bucket: str):
        self.client = InfluxDBClient(url=host, token=token, org=org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.org = org
        self.bucket = bucket

    def write_if_keys_in_dict(self, data: dict, keys: list) -> list:
        point = Point("env")
        raw_data = []

        for key in keys:
            if key in data and data[key] is not None:
                point = point.field(key, float(data[key]))
                raw_data.append(float(data[key]))
            else:
                logger.log_warning("Problem parsing received JSON data - no " + key + " field")
                raw_data.append(None)

        self.write_api.write(bucket=self.bucket, org=self.org, record=point)

        return raw_data
