import paho.mqtt.client as mqtt

# Define the MQTT broker and port
BROKER = "172.16.93.83"  # Public test broker
PORT = 1883  # Standard MQTT port
TOPIC = "test/topic"  # Topic to publish to
MESSAGE = "Hello from the publisher!"  # Message to send

# Initialize the MQTT client
client = mqtt.Client()

# Connect to the broker
client.connect(BROKER, PORT, 60)

# Publish a message
print(f"Publishing message: {MESSAGE} to topic: {TOPIC}")
client.publish(TOPIC, MESSAGE)

client.disconnect()
