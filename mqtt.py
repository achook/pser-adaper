from const import MQTT_ALARM_TOPIC, MQTT_DATA_TOPIC
import logger

import paho.mqtt.client as mqtt


class MQTTClient:
    def __init__(self, on_connect, on_message):
        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.on_message = on_message

    @classmethod
    def default(cls, new_data_hander: callable):
        return cls(
            _default_on_connect,
            lambda client, userdata, msg: _default_on_message(new_data_hander, client, userdata, msg)
        )

    def connect(self, host: str, port: int = 1883, keepalive: int = 60) -> None:
        self.client.connect(host, port, keepalive)

    def loop_forever(self) -> None:
        self.client.loop_forever()


def _default_on_connect(client: mqtt.Client, userdata: any, flags, rc: int) -> None:
    if rc == 0:
        logger.log_info("Connected successfully")
    else:
        logger.log_fatal("Connect failed with code: " + str(rc), rc)

    # Connect to the data and alarm topics
    client.subscribe(MQTT_DATA_TOPIC)
    client.subscribe(MQTT_ALARM_TOPIC)
    logger.log_info("Subscribed to data topic: " + MQTT_DATA_TOPIC + " and alarm topic: " + MQTT_ALARM_TOPIC)


def _default_on_message(new_data_hander: callable, client: mqtt.Client, userdata: any, msg: mqtt.MQTTMessage) -> None:
    logger.log_info("Message received")
    logger.log_info("Topic: " + msg.topic)
    logger.log_info("Raw payload: " + msg.payload.decode())

    if msg.topic == MQTT_DATA_TOPIC:
        new_data_hander(msg.payload.decode())
