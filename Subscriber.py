import paho.mqtt.client as mqtt
import time
import csv
import json
import numpy 

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
    client.subscribe("ritalobo22")

print("Antes do on_connect")
def on_message(client, userdata, msg):
    print("saving")
    print("")
    print("received message =" + str(msg.payload.decode()))
    print(msg.payload.decode("utf-8"))
    print("")
    res = json.loads(msg.payload.decode()) #Retornar à lista
    print("outro print")
    with open("outro_teste2.csv", "w") as f:
        write = csv.writer(f)
        write.writerows(res)
    
    print("Done")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.eclipseprojects.io", 1883, 60)
client.loop_forever()
