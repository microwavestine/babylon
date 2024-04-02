in /etc/mosquitto
set mosquitto.conf as follows
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
