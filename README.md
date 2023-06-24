# Onvif Python Zeep Libraries

ONVIF Client Implementation in Python. 

Supported Onvif Services: 
  - Device  Service
  - Image Service
  - Media Service
  - Analytics Service
  - Event Service
  - PTZ Service


## Installation

Install some libraries with pip

```bash
  pip install zeep
  pip install opencv-python
```
    
## Run Locally

Clone the project

```bash
  git clone https://link-to-project
```

Go to the project directory

```bash
  cd onvif-python
```

Configure Project 

This project have different testers for each Onvif services.

```bash
tester\device_service_tester.py
tester\analytics_service_tester.py
tester\event_service_tester.py
tester\image_service_tester.py
tester\media_service_tester.py
tester\ptz_service_tester.py
```
and 
```bash
main.py
```

Onvif Device configurations should be changed for service which was wanted to run.

For example :
```python
# to Configure Onvif Device
onvif_device.ip = "11.63.1.6"
onvif_device.username = "admin"
onvif_device.password = "12345"
onvif_device.port = "80"
```

Test project 

```bash
  python.exe .\tester\device_service_tester.py
  python.exe .\tester\analytics_service_tester.py
  python.exe .\tester\event_service_tester.py
  python.exe .\tester\image_service_tester.py
  python.exe .\tester\media_service_tester.py
  python.exe .\tester\ptz_service_tester.py
```

or 
```
python.exe main.py
```

It should be configured global veriables in main file, to be able to test main. The globals are ;

```python
# globals 
# True -> Able to test / False -> Disable to test
TEST_DEVICE_SERVICE = False
TEST_PTZ_SERVICE = False
TEST_IMAGE_SERVICE = False
TEST_MEDIA_SERVICE = False
TEST_EVENT_SERVICE = False
TEST_ANALYTICS_SERVICE = True
```


## Test Services
First of all, you should create an Onvif Service object ;
 
```python
from lib.onvif import OnvifService
from lib.services.device_service import DeviceService
from lib.services.image_service import ImageService
from lib.services.media_service import MediaService
from lib.services.analytics_service import AnalyticsService
from lib.services.ptz_service import PTZService
from lib.services.event_service import EventService

onvif_device = OnvifService()
# to Configure Onvif Device
onvif_device.ip = "11.63.1.6"
onvif_device.username = "admin"
onvif_device.password = "12345"
onvif_device.port = "80"
onvif_device.wsdl_directory = "wsdl" # define wsdl directory
onvif_device.connect_onvif()
```

  - Device  Service

	For device service you should create ```DeviceService``` object. Then you can test ```GetHostname``` request like this;

      ```python
      print(f'Onvif Capabilities response : \n{onvif_device.capabilities}')
      device_serv = DeviceService(onvif_service=onvif_device)
      device_hostname = device_serv.GetHostname()
      print(f'GetHostname response : \n{device_hostname}')
      ```
  - Image Service
  
  	For Image service you should create ```DeviceService``` object. Then you can test ```GetHostname``` request like this;

      ```python
      print(f'Image Service Capabilities: \n{onvif_device.capabilities.Image}')
      image_serv = ImageService(onvif_service=onvif_device)
      image_service_cap = image_serv.GetServiceCapabilities()
      print(f'GetServiceCapabilities response : \n{image_service_cap}')
      ```
  - Media Service

	For Media service you should create ```MediaService``` object. Then you can test ```GetVideoSources``` request like this;
   
      ```python
      print(f'Media Service Capabilities: \n{onvif_device.capabilities.Media}')
      media_serv = MediaService(onvif_service=onvif_device)
      video_sources = media_serv.GetVideoSources()
      print(f'GetVideoSources response : \n{video_sources}')
      ```

  - Analytics Service
  
	For Analytics service you should create ```AnalyticsService``` object. Then you can test ```GetServiceCapabilities``` request like this;
      
      ```python
      print(f'Analytics Service Capabilities: \n{onvif_device.capabilities.Analytics}')
      analytics_serv = AnalyticsService(onvif_service=onvif_device)
      analy_capabilities = analytics_serv.GetServiceCapabilities()
      print(f'GetServiceCapabilities response :\n{analy_capabilities}')
      ```

  - Event Service

	For Event service you should create ```EventService``` object. Then you can test ```GetServiceCapabilities``` request like this;

      ```python
      print(f'Event Service Capabilities: \n{onvif_device.capabilities.Events}')
      event_serv = EventService(onvif_service=onvif_device)
      serv_caps = event_serv.GetServiceCapabilities()
      print(f'GetServiceCapabilities response for : \n{serv_caps}')
      ```

  - PTZ Service

	For PTZ service you should create ```PTZService``` object. Then you can test ```GetServiceCapabilities``` request like this;
   
      ```python
      print(f'PTZ Service Capabilities: \n{onvif_device.capabilities.PTZ}')
      ptz_serv = PTZService(onvif_service=onvif_device)
      ptz_caps = ptz_serv.GetServiceCapabilities()
      print(f'GetServiceCapabilities response : \n{ptz_caps}')
      ```

## Documentation
 - [Zeep SOAP Client Lib](https://docs.python-zeep.org/en/master/)
 - [OpenCV](https://docs.opencv.org/4.7.0/d6/d00/tutorial_py_root.html)