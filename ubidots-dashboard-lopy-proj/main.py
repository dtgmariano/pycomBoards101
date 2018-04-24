from network import WLAN
import urequests as requests
import machine
import time

TOKEN = "BBFF-owDdQ4eVqsu0E3WOO6bLQ31oDk5atr" #Put here your TOKEN
DELAY = 5  # Delay in seconds


fuel = [100, 98, 96, 95, 94, 50, 20, 10, 100, 90, 80, 58, 45, 23, 10, 100, 89, 60, 59, 54, 50, 20]  # Data values
speed = [234, 200, 158, 120, 30, 10, 0, 20, 50, 90, 110, 150, 200, 210, 200, 234, 200, 158, 120, 30, 10, 0] # Data values
coordinates = [[51.4793, 5.6570], [51.4416, 5.4697], [51.5606,5.0919]]
sin = [0.00, 0.30, 0.56, 0.78, 0.93, 1.00, 0.97, 0.86, 0.68, 0.43, 0.14, -0.16, -0.44, -0.69, -0.87, -0.98, -1.00, -0.93, -0.77, -0.55, -0.28, 0.02]

limit_t1 = 21
limit_t2 = 2

COUNTER = 0
COUNTER2 = 0

wlan = WLAN(mode=WLAN.STA)
wlan.antenna(WLAN.INT_ANT)

# Assign your Wi-Fi credentials
wlan.connect("Pycom", auth=(WLAN.WPA2, "PyE!ndh0ven#"), timeout=5000)

while not wlan.isconnected ():
    machine.idle()
print("Connected to Wifi\n")

# Builds the json to send the request
def build_json(variable1, value1, variable2, value2, variable3, value3, variable4, value4, value5):
    try:
        lat = value5[0]
        lng = value5[1]
        data = {variable1: {"value": value1},
                variable2: {"value": value2, "context": {"lat": lat, "lng": lng}},
                variable3: {"value": value3},
                variable4: {"value": value4}}
        return data
    except:
        return None

# Sends the request. Please reference the REST API reference https://ubidots.com/docs/api/
def post_var(device, value1, value2, value3, value4, value5):
    try:
        url = "https://things.ubidots.com/"
        url = url + "api/v1.6/devices/" + device
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        data = build_json("fuel", value1, "position", value2, "speed", value3, "sinwave", value4, value5)
        if data is not None:
            print(data)
            req = requests.post(url=url, headers=headers, json=data)
            return req.json()
        else:
           pass
    except:
        pass

while True:

    post_var("pycom", fuel[COUNTER], COUNTER, speed[COUNTER], sin[COUNTER], coordinates[COUNTER2])
    time.sleep(DELAY)

    if COUNTER < limit_t1:
        COUNTER += 1
    else:
        COUNTER = 0

    if COUNTER2 < limit_t2:
        COUNTER2 += 1
    else:
        COUNTER2 = 0
