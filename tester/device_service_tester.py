"""
Created to test Onvif Device service properties.

craeted by : enstns
created time : 23.05.23
"""
import path 
import sys
import datetime
 
# directory reach
directory = path.Path(__file__).abspath()
 
# setting path
parent_directory = directory.parent.parent
sys.path.append(parent_directory)

from lib.requests_messages.device_request_messages import DeviceRequestMessages
from lib.params.device_request_params import DeviceEnumParams, DeviceRequestParams
from lib.services.device_service import DeviceService
from lib.onvif import OnvifService

onvif_device = OnvifService()

# device information
onvif_device.ip = "11.61.1.160"
onvif_device.username = "admin"
onvif_device.password = "888888"
onvif_device.port = "8082"
onvif_device.wsdl_directory = parent_directory + "/wsdl"

# onvif device connection
onvif_device.connect_onvif()


print(f'Device Capabilities response : \n{onvif_device.capabilities}')
device_serv = DeviceService(onvif_service=onvif_device)
device_hostname = device_serv.GetHostname()
print(f'GetHostname response : \n{device_hostname}')

# GET device Time
device_time = device_serv.GetSystemDateAndTime()
print(f'GetSystemDateAndTime response : \n{device_time}')
time_zone_obj = DeviceRequestParams.TimeZone(tz="CST-8")
time_obj = DeviceRequestParams.Time(hour=datetime.datetime.now().hour,minute=datetime.datetime.now().minute,second=datetime.datetime.now().second)
date_obj = DeviceRequestParams.Date(year=datetime.datetime.now().year,month=datetime.datetime.now().month,day=datetime.datetime.now().day)
utc_datetime_obj = DeviceRequestParams.DateTime(time=time_obj,date=date_obj)
set_date_time_req = DeviceRequestMessages.SetSystemDateAndTimeMessage(date_time_type=DeviceEnumParams.SetDateTimeType.Manual,daylight_savings=False,time_zone=time_zone_obj,UTC_datetime=utc_datetime_obj)
print(f'Created SetSystemDateAndTimeRequest message : \n{set_date_time_req.to_dict()}')
set_date_time_req_status = device_serv.SetSystemDateAndTime(request_message=set_date_time_req)
if set_date_time_req_status: print(f'SetSystemDateAndTime complete with success...')

discovery_mode = device_serv.GetRemoteDiscoveryMode()
print(f'GetRemoteDiscoveryMode response : \n{discovery_mode}')

discovery_mode = device_serv.GetDiscoveryMode()
print(f'GetDiscoveryMode response : \n{discovery_mode}')

print(f'Try to change DiscoveryMode to Discoverable..')
device_serv.SetDiscoveryMode(discovery_mode=DeviceEnumParams.DiscoveryMode.Discoverable)

create_user_req = DeviceRequestMessages.CreateUsersMessage(user=DeviceRequestParams.User(username="aselsan",userlevel=DeviceEnumParams.UserLevel.Administrator,password="12345"))
print(f'Created CreateUsers Request message : \n{create_user_req.to_dict()}')
device_serv.CreateUsers(request_message=create_user_req)

users_info = device_serv.GetUsers()
print(f'GetUsers response : \n{users_info}')

print(f'Try to delete Users..')
delete_users_status = device_serv.DeleteUsers(username="aselsan")
if delete_users_status : print(f'CreateUsers complete with success...')

ntp_info = device_serv.GetNTP()
print(f'GetNTP response : \n{ntp_info}')

ntp_req_message = DeviceRequestMessages.SetNTPMessage(from_DHCP=False,NTP_manual=DeviceRequestParams.NetworkHost(network_host_type=DeviceEnumParams.NetworkHostType.IPv4,IPv4Address="10.0.0.1"))
print(f'Created SetNTPRequest Request message : \n{ntp_req_message.to_dict()}')
device_serv.SetNTP(request_message = ntp_req_message)      
ntp_info = device_serv.GetNTP()
print(f'GetNTP response : \n{ntp_info}')
