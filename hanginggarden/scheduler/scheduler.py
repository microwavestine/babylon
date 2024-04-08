"""
import schedule
import time
import paho.mqtt.client as mqtt
from datetime import datetime

# MQTT broker configuration
mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic = "group3/led"

# Function to read the setting from the text file
def read_setting_from_file(current_hour):
    with open("led_schedule.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            line_hour = int(line.split(":")[0])
            print("line_hour")
            print(line_hour)
            print("current_hour")
            print(current_hour)
            if line_hour == current_hour:
                setting = line.split()[1]
                return setting
    return None

# Function to publish the setting via MQTT
def publish_setting(setting):
    client = mqtt.Client(client_id="my_client")
    client.connect(mqtt_broker, mqtt_port)
    client.publish(mqtt_topic, setting)
    client.disconnect()

# Function to run every hour
def job():
    current_hour = datetime.now().hour
    setting = read_setting_from_file(current_hour)
    if setting:
        publish_setting(1 if setting == "ON" else 0)
        print(f"Published setting '{setting}' for hour {current_hour}")
    else:
        print(f"No setting found for hour {current_hour}")

# Schedule the job to run every hour
schedule.every().hour.do(job)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
"""
import schedule
import time
import paho.mqtt.client as mqtt
from datetime import datetime

# MQTT broker configuration
mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic = "group3/led"

# Function to read the setting from the text file
def read_setting_from_file(current_hour):
    with open("led_schedule.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            line_hour = int(line.split(":")[0])
            if line_hour == current_hour:
                setting = line.split()[1]
                return setting
    return None

# Function to publish the setting via MQTT
def publish_setting(setting):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(mqtt_broker, mqtt_port)
    client.publish(mqtt_topic, setting)
    client.disconnect()

# Function to run every hour at the start of the hour
def job():
    current_hour = datetime.now().hour
    setting = read_setting_from_file(current_hour)
    if setting:
        publish_setting(1 if setting == "ON" else 0)
        print(f"Published setting '{setting}' for hour {current_hour}")
    else:
        print(f"No setting found for hour {current_hour}")

# Schedule the job to run every hour at the start of the hour
for hour in range(24):
    schedule.every().day.at(f"{hour:02d}:00").do(job)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
