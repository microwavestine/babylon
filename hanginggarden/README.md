# Hanging Garden - Aquaponics & Aeroponics

This project involves four parts :

1. controltower: a Django web app dashboard for manual control and editing auto scheduler settings. Lives on Rapberry Pi.
2. (Auto) scheduler background job. Lives on Rapberry Pi.
3. Real-time monitoring: just a standard InfluxDB+Telegraf+Grafana stack with MQTT. Lives on Rapberry Pi.
4. Camera for environment monitoring: ESP32 server that streams camera data, can be opened on Raspberry Pi for ease of access.

# Architectural Decision & Philosophy

The project started off with a lack of requirements, while having a pressing deadline. Therefore I chose for a divide and conquer system design that would make it easier for teammates to QA and iterate quickly like a lean product development cycle. One mistake I made with this design is that I did not think too much about hardware QA - and that happened to be the major failing point for our team. However, the software system design itself worked smoothly.

Some factors I considered were:

- Everyone on the team used iPhone, and no one knew how to develop phone apps. I could work with a Django web app.
- Teammates need to be able to control and respond to abnoramlies anytime, anywhere; not just at the school. What's the point of making a smart system in-house only, if you are going to be there anyway to see it grow?
- However, I did not want to compromise on security by exposing a smart farm control system to outside.
- Arduino Uno R4 Wifi has issues with timers. So I am going to design in such a way that Arduino only communicates with Rapberry Pi to receive or publish information, but doesn't do any timezone or time related calculations.
- Since the temperatures and other sensors don't fluctuate dramatically, I don't have to worry too much about data granularity. After some testing, it seems I have to be more worried about sensors malfunctioning.

(Diagrams to be updated)

# Getting Started

I recommend setting up Raspberry Pi + Common first, then work on Arduino last.

## Common

1. Install RealVNC
2. Install Tailscale, make an account.

## Arduino

See https://github.com/microwavestine/k-digital-smart-farm/tree/main/arduino/mqtt

**Change mqtt_server to [raspberrypi_IP], and set SSID, passwords**

## Raspberry Pi

After doing the initial setup for Raspberry Pi, we need to enable ssh and vnc first for ease of access. `sudo rasp-config` then in `Interface Options`, enable VNC and SSH.

### Installing Tailscale

Installing tailscale on Raspberry Pi allows you to access it anywhere via Tailscale VPN network.

`curl -fsSL https://tailscale.com/install.sh | sudo bash`
`sudo tailscale up`

Then click on the login link to link raspberry pi to your account.

### Installing MQTT server

https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi/

Follow through the first 1~6 steps. Then in /etc/mosquitto, set mosquitto.conf as follows

```
pid_file /run/mosquitto/mosquitto.pid

persistence true
persistence_location /var/lib/mosquitto/

log_dest file /var/log/mosquitto/mosquitto.log

listener 8883
protocol websockets

listener 1883
allow_anonymous true
include_dir /etc/mosquitto/conf.d
```

make sure to `sudo systemctl restart mosquitto`.

### Installing Python packages

### Installing tmux to keep background process running

# Next Steps

## Sanity check

1. Upload Arduino sketch
2. Use tools like MQTT explorer; fill in raspberry pi IP to inspect MQTT server, and check that signals sent from the MQTT explorer is processed correctly on Arduino side.
3. If there are no issues, continue...

## Let's start!
