from mqtt import MQTTClient
from influx import DBClient

from const import MQTT_ALARM_TOPIC, MQTT_SERVER_ADDRESS, MQTT_SERVER_PORT, INFLUX_ADDRESS, INFLUX_PORT, \
    INFLUX_USER, INFLUX_TOKEN, INFLUX_ORG, INFLUX_BUCKET

import json
import logger

influx_client = DBClient(INFLUX_ADDRESS, INFLUX_PORT, INFLUX_USER, INFLUX_TOKEN, INFLUX_ORG, INFLUX_BUCKET)


def check_if_data_in_bounds(temperature: float, humidity: float, luminosity: float) -> bool:
    # Check if the temperature is in bounds
    if temperature < 0 or temperature > 100:
        return False

    # Check if the humidity is in bounds
    if humidity < 0 or humidity > 100:
        return False

    # Check if the luminosity is in bounds
    if luminosity < 0 or luminosity > 100:
        return False

    # If all checks passed, return true
    return True


def handle_new_data(raw_data: str) -> None:
    # Try to parse the received JSON data
    # If it fails, handle it and return
    try:
        json_data = json.loads(raw_data)
    except json.JSONDecodeError as e:
        logger.log_warning("Error parsing received JSON data - not a valid JSON string")
        return

    [temperature, humidity, luminosity] = influx_client.write_if_keys_in_dict(
        json_data,
        ["temperature", "humidity", "light"]
    )

    # Check if the data is in bounds
    if not check_if_data_in_bounds(temperature, humidity, luminosity):
        logger.log_info("Data out of bounds, sending alarm")
        mqtt_client.publish(MQTT_ALARM_TOPIC, "ALARM")
    else:
        logger.log_info("Data in bounds, no alarm needed")
        mqtt_client.publish(MQTT_ALARM_TOPIC, "OK")


mqtt_client = MQTTClient.default(handle_new_data)
mqtt_client.connect(MQTT_SERVER_ADDRESS, MQTT_SERVER_PORT)

mqtt_client.loop_forever()
