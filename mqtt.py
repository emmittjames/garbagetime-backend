#!/usr/bin/env python3

import base64
import configparser
from datetime import datetime
import json
import struct

import paho.mqtt.client as mqtt

# Read in config file with MQTT details.
config = configparser.ConfigParser()
config.read("config.ini")

# MQTT broker details
broker_address = config["mqtt"]["broker"]
username = config["mqtt"]["username"]
password = config["mqtt"]["password"]

# MQTT topic to subscribe to. We subscribe to all uplink messages from the
# devices.
topic = "v3/+/devices/+/up"

# Callback when successfully connected to MQTT broker.
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker.")
    # can send something to frontend on connect if wanted

    if rc != 0:
        print(" Error, result code: {}".format(rc))


# Callback function to handle incoming MQTT messages
def on_message(client, userdata, message):
    # Timestamp on reception.
    current_date = datetime.now()

    # Handle TTN packet format.
    message_str = message.payload.decode("utf-8")
    message_json = json.loads(message_str)
    encoded_payload = message_json["uplink_message"]["frm_payload"]
    raw_payload = base64.b64decode(encoded_payload)

    if len(raw_payload) == 0:
        # Nothing we can do with an empty payload.
        return

    # First byte should be the group number, remaining payload must be parsed.

    # See if we can decode this payload.
    print("ID:",raw_payload[0])
    float_value = struct.unpack('!f',raw_payload[1:])[0]
    print("Distance:",float_value)
    # RIGHT HERE: send http packet to frontend
    # requests.post(frontendurl, payload)


# MQTT client setup
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

# Setup callbacks.
client.on_connect = on_connect
client.on_message = on_message

# Connect to broker.
client.username_pw_set(username, password)
client.tls_set()
client.connect(broker_address, 8883)

# Subscribe to the MQTT topic and start the MQTT client loop
client.subscribe(topic)
client.loop_forever()