import socket 
import requests
 

hostname = socket.gethostname() 
IPAddr = socket.gethostbyname(hostname) 
im_url_appx = 'https://'+IPAddr+':8000/IM/USER1/APPX' 

def CreateTts():

    message = '''<mmi:mmi xmlns:mmi="http://www.w3.org/2008/04/mmi-arch" mmi:version="1.0">

        <mmi:startRequest mmi:context="ctx-1" mmi:requestId="app-1" mmi:source=\"%s\" mmi:target="IM">

            <mmi:data>

            <emma:emma xmlns:emma="http://www.w3.org/2003/04/emma" emma:version="1.0">

                <emma:interpretation emma:confidence="1" emma:id="app-" emma:medium="display" emma:mode="command" emma:start="0">

                <command>%s</command>

                </emma:interpretation>

            </emma:emma>

            </mmi:data>

        </mmi:startRequest>

        </mmi:mmi>''' % ("APP", "ler algo")

   

    try:

        headers = {'Content-Type': 'application/xml'}  # set what your server accepts 
        requests.post(im_url_appx, data=message, headers=headers, verify=False)

    except requests.exceptions.ConnectionError or requests.exceptions.Timeout or requests.exceptions.TooManyRedirects or requests.exceptions.RequestException:

        print("Connection error")