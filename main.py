from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import base64, configparser, json, struct, random
import paho.mqtt.client as mqtt
from datetime import datetime

global_distance = -1

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
    global_distance = float_value
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

client.subscribe(topic)
client.loop_forever()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Hello World",
        "temp": random.randint(0, 100),
        "distance": global_distance,
    }