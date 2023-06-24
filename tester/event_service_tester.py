"""
Created to test Onvif Event service properties.

craeted by : enstns
created time : 23.05.23
"""
import signal
import path 
import sys
import time
 
# directory reach
directory = path.Path(__file__).abspath()
 
# setting path
parent_directory = directory.parent.parent
sys.path.append(parent_directory)

from lib.services.event_service import EventService
from lib.onvif import OnvifService

STOP = False

onvif_device = OnvifService()

# device information
onvif_device.ip = "11.63.1.6"
onvif_device.username = "admin"
onvif_device.password = "12345"
onvif_device.port = "80"
onvif_device.wsdl_directory = parent_directory + "/wsdl"

# onvif device connection
onvif_device.connect_onvif()

# TODO: control keyboard interrupt
def signal_sigint_handler(signal, frame):
    global STOP
    STOP = True
    print("SIGINT received closing program!")

signal.signal(signal.SIGINT, signal_sigint_handler)

print("Start to Test Event service...")
event_serv = EventService(onvif_service=onvif_device)
if event_serv.is_event_service_supported:
    print('Event service is supported...')
    print(f'Event Service XAddr is : {event_serv.xAddr}')
    print(f'Event Service NameSpace is : {event_serv.event_name_space}')
    print(f'Event Service Capabilities: \n{onvif_device.capabilities.Events}')

    serv_caps = event_serv.GetServiceCapabilities()
    print(f'GetServiceCapabilities response for : \n{serv_caps}')

    serv_properties = event_serv.GetEventProperties()
    print(f'GetEventProperties response for : \n{serv_properties}')

    pullpoint_subs = event_serv.CreatePullPointSubscription()
    print(f'CreatePullPointSubscription response for : \n{pullpoint_subs}')
    
    pull_response = event_serv.PullMessages(address=pullpoint_subs.SubscriptionReference.Address._value_1,timeout="PT1M",message_limit=1024)
    print(f'PullMessages response for : \n{pull_response}')
    print(f'NotificationMessage response for : \n{pull_response.NotificationMessage}')
    for message in pull_response.NotificationMessage:
        topic = message.Topic
        message_att = message.Message
        source = message.Source
        date = message.Data
        state = message.Data.Value
        print(f'--------------------------------------------')
        print(f'Topic : {topic} \n\t Message : {message_att} \n\t\t State : {state}')

    while not STOP and pullpoint_subs.SubscriptionReference.Address._value_1 != None and pull_response:
        for message in pull_response.NotificationMessage:
            topic = message.Topic
            message_att = message.Message
            source = message.Source
            date = message.Data
            state = message.Data.Value
            print(f'--------------------------------------------')
            print(f'Topic : {topic} \n\t Message : {message_att} \n\t\t State : {state}')
        pull_response = event_serv.PullMessages(address=pullpoint_subs.SubscriptionReference.Address._value_1,timeout="PT1M",message_limit=1024)
        renew_response = event_serv.Renew(address=pullpoint_subs.SubscriptionReference.Address._value_1,termination_time="PT1M")
        print(f'Renew response : \n{renew_response}')
        time.sleep(1)
    
    event_serv.Unsubscribe(address=pullpoint_subs.SubscriptionReference.Address._value_1)
else:
    print("Event service not supported!")
