import asyncio 
import websockets 
import json 
import xml.etree.ElementTree as ET 
import ssl 
import socket 
import sys 

hostname = socket.gethostname() 
IPAddr = socket.gethostbyname(hostname) 
im_url_appx = 'https://'+IPAddr+':8000/IM/USER1/APPX'
  
 

def process_intent(intent): 
    print(intent)
 

async def connect(): 
    uri = "wss://"+IPAddr+":8005/IM/USER1/APP" 

    #connect to secure websocket server and open certificate 
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT) 
    #context.load_cert_chain(certfile='/certificados/cert.pem', keyfile='/certificados/key.pem')
 

    #error because Selfsigned certificate 
    context.check_hostname = False 
    context.verify_mode = ssl.CERT_NONE
 
    async with websockets.connect(uri, ssl=context) as websocket:

        print("Connected to server") 
        sys.stdout.flush()

        while True:

            message = await websocket.recv() 
            #print(message) 

            if(message!="OK" and message!="RENEW"): 

                # parse the message in xml format 
                xml = root = ET.fromstring(message) 
                for child in root.iter('*'): 
                    if child.tag == "command": 
                        json_data = json.loads(child.text)

                        if "recognized" not in json_data: continue
 
                        process_intent(json_data)
 
            sys.stdout.flush() 

asyncio.get_event_loop().run_until_complete(connect()) 
asyncio.get_event_loop().run_forever()

 