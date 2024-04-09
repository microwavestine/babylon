# import schedule
# import time
# import paho.mqtt.client as mqtt
# from datetime import datetime

# # MQTT broker configuration
# mqtt_broker = "localhost"
# mqtt_port = 1883
# mqtt_topic = "group3/led"

# # Function to read the setting from the text file
# def read_setting_from_file(current_hour):
#     with open("led_schedule.txt", "r") as file:
#         lines = file.readlines()
#         for line in lines:
#             line_hour = int(line.split(":")[0])
#             if line_hour == current_hour:
#                 setting = line.split()[1]
#                 return setting
#     return None

# # Function to publish the setting via MQTT
# def publish_setting(setting):
#     client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
#     client.connect(mqtt_broker, mqtt_port)
#     client.publish(mqtt_topic, setting)
#     client.disconnect()

# # Function to run every hour at the start of the hour
# def job():
#     current_hour = datetime.now().hour
#     setting = read_setting_from_file(current_hour)
#     if setting:
#         publish_setting(1 if setting == "ON" else 0)
#         print(f"Published setting '{setting}' for hour {current_hour}")
#     else:
#         print(f"No setting found for hour {current_hour}")

# # Schedule the job to run every hour at the start of the hour
# for hour in range(24):
#     schedule.every().day.at(f"{hour:02d}:00").do(job)

# # Run the scheduler
# while True:
#     schedule.run_pending()
#     time.sleep(1)
import schedule
import time
import paho.mqtt.client as mqtt
from datetime import datetime, timedelta

# MQTT broker configuration
mqtt_broker = "localhost"
mqtt_port = 1883
mqtt_topic_hourly = "group3/led"
mqtt_topic_5min = "group3/pumpmotor"
mqtt_topic_5min_2 = "group3/fan"

# Function to read the hourly setting from the text file
def read_hourly_setting_from_file(current_hour):
    with open("led_schedule.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            line_hour = int(line.split(":")[0])
            if line_hour == current_hour:
                setting = line.split()[1]
                return setting
    return None

# Function to read the 5-minute setting from the text file
def read_5min_setting_from_file(current_time):
    with open("pumpmotor_schedule.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            line_time = line.split()[0]
            if line_time == current_time:
                setting = line.split()[1]
                return setting
    return None
    
# Function to read the 5-minute setting from the text file
def read_5min_setting_from_file_2(current_time):
    with open("fan_schedule.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            line_time = line.split()[0]
            if line_time == current_time:
                setting = line.split()[1]
                return setting
    return None

# Function to publish the setting via MQTT
def publish_setting(topic, setting):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(mqtt_broker, mqtt_port)
    client.publish(topic, 1 if setting == "ON" else 0)
    client.disconnect()

# Function to run every hour at the start of the hour
def hourly_job():
    current_hour = datetime.now().hour
    setting = read_hourly_setting_from_file(current_hour)
    if setting:
        publish_setting(mqtt_topic_hourly, setting)
        print(f"Published hourly setting '{setting}' for hour {current_hour}")
    else:
        print(f"No hourly setting found for hour {current_hour}")

# Function to run at fixed 5-minute intervals
def five_min_job():
    current_time = datetime.now().strftime("%H:%M")
    print(current_time) # debugging purpose
    setting = read_5min_setting_from_file(current_time)
    setting2 = read_5min_setting_from_file_2(current_time)
    if setting:
        publish_setting(mqtt_topic_5min, setting)
        print(f"Published 5-minute setting for Pump Motor'{setting}' for time {current_time}")
    if setting2:
        publish_setting(mqtt_topic_5min_2, setting)
        print(f"Published 5-minute setting for Fan'{setting}' for time {current_time}")
    else:
        print(f"No 5-minute setting found for time {current_time}")

        

# Schedule the hourly job to run every hour at the start of the hour
for hour in range(24):
    schedule.every().day.at(f"{hour:02d}:00").do(hourly_job)

# Schedule the 5-minute job to run at fixed 5-minute intervals
start_time = datetime.now().replace(minute=(datetime.now().minute // 5) * 5, second=0, microsecond=0)
next_run = start_time
while next_run <= datetime.now() + timedelta(days=1):
    schedule.every().day.at(next_run.strftime("%H:%M")).do(five_min_job)
    next_run += timedelta(minutes=5)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
