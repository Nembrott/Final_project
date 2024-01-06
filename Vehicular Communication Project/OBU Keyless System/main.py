import paho.mqtt.client as mqtt
from aiohttp import web

HTTP_PORT = 8888
MQTT_BROKER = 'test.mosquitto.org'
MQTT_PORT = 1883
MQTT_TOPIC = 'vc2023/key-is-ok'

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    """
    Callback function for mqtt client connection
    """
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    """
    Callback function for mqtt client message
    """
    print(msg.topic + ' ' + str(msg.payload))

def on_disconnect(client, userdata, rc):
    """
    Callback function for mqtt client disconnect
    """
    print('Disconnected with result code ' + str(rc))

def on_publish(client, userdata, mid):
    """
    Callback function for mqtt client publish
    """
    print('Message ' + str(mid) + ' published')

def on_subscribe(client, userdata, mid, granted_qos):
    """
    Callback function for mqtt client subscribe
    """
    print('Subscribed to topic ' + str(mid))


mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_publish = on_publish
mqtt_client.on_subscribe = on_subscribe

async def keyless_handler(request):
    """
    Http handler function for /keyless post route
    """

    return web.Response(text='Keyless')

async def driver_handler(request):
    """
    Http handler function for /driver get route
    """

    return web.Response(text='Driver')




httpServer = web.Application()
httpServer.router.add_post('/keyless', keyless_handler)
httpServer.router.add_get('/driver', driver_handler)



if __name__ == '__main__':
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
    mqtt_client.loop_start()
    web.run_app(httpServer, port=HTTP_PORT)
