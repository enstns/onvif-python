"""
Created to control Onvif Device service properties.

craeted by : enstns
created time : 01.04.23
"""
from zeep.client import Settings
import logging

from lib.onvif import OnvifService, get_caching_client
from lib.params.device_request_params import DeviceEnumParams
from lib.requests_messages.device_request_messages import DeviceRequestMessages

DEBUG = True
LOG = False

logger = logging.getLogger('device_service')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

DEVICE_SERVICE_NS = "http://www.onvif.org/ver10/device/wsdl"

if DEBUG:
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

if LOG: 
    log = logging.FileHandler(filename="log/onvif_service.log", mode='a', encoding=None, delay=False, errors=None)
    log.setLevel(logging.DEBUG)
    log.setFormatter(formatter)
    logger.addHandler(log)

settings = Settings()
settings.strict = False
settings.xml_huge_tree = True

def get_image_addr_namespace(services = []):
    if services and services != None:
        for serv in services:
            ns = str(serv.Namespace)
            if "device" in ns:
                return serv.XAddr, serv.Namespace
    else:
        return None,None

class DeviceService:
    def __init__(self,onvif_service = OnvifService()) -> None:
        self.onvif_service = onvif_service
        self.wsdlUrl = self.onvif_service.wsdl_directory + "/devicemgmt.wsdl"
        self.xAddr = self.onvif_service.get_con_xaddr()

    def CreateUsers(self,request_message = DeviceRequestMessages.CreateUsersMessage) -> bool: # not working
        """
        This operation creates new device users and corresponding credentials on a device for authentication purposes. 
        The device shall support creation of device users and their credentials through the CreateUsers command. 
        Either all users are created successfully or a fault message shall be returned without creating any user.
        - requirements : 
            - user - unbounded; [CreateUsersMessage] 
                Creates new device users object and corresponding credentials. 
        - return [boolean]; 
            - CreateUser status
        """
        status = False
        if self.onvif_service.get_con_status():
            logger.info(f"Try to CreateUsers information..")
            try:
                zeep_device_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_device = zeep_device_client.create_service("{" + DEVICE_SERVICE_NS + "}DeviceBinding", self.xAddr)
                ws_client_device.CreateUsers(**request_message.to_dict())
            except Exception as emsg:
                logger.error(f"CreateUsers unsuccess.. -> {emsg}")
            else:
                status = True
                logger.info(f"CreateUsers complete with success..")
        return status

    def DeleteUsers(self,username = str) -> bool:
        """
        This operation deletes users on a device. The device shall support deletion of device users and their credentials through the DeleteUsers command. 
        - requirements : 
            - username - unbounded; [string]
                Deletes users on an device and there may exist users that cannot be deleted to ensure access to the unit. 
                Either all users are deleted successfully or a fault message MUST be returned and no users be deleted. 
                If a username exists multiple times in the request, then a fault message is returned.
        - return [boolean]:
            - Delete user status
        """
        status = False
        if self.onvif_service.get_con_status():
            logger.info(f"Try to DeleteUsers information..")
            try:
                zeep_device_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_device = zeep_device_client.create_service("{" + DEVICE_SERVICE_NS + "}DeviceBinding", self.xAddr)
                ws_client_device.DeleteUsers(Username=username)
            except Exception as emsg:
                logger.error(f"DeleteUsers unsuccess.. -> {emsg}")
            else:
                status = True
                logger.info(f"DeleteUsers complete with success..")
        return status

    def GetUsers(self) -> list:
        """
        This operation lists the registered users and corresponding credentials on a device. 
        The device shall support retrieval of registered device users and their credentials for the user token through the GetUsers command.
        - return [list]
            - User - optional, unbounded; [User]
                Contains a list of the onvif users and following information is included in each entry: username and user level.
        """
        users = []
        if self.onvif_service.get_con_status():
            logger.info(f"Try to GetUsers information..")
            try:
                zeep_device_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_device = zeep_device_client.create_service("{" + DEVICE_SERVICE_NS + "}DeviceBinding", self.xAddr)
                users = ws_client_device.GetUsers()
            except Exception as emsg:
                logger.error(f"GetUsers unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetUsers complete with success..")
        return users

    def GetDeviceInformation(self) -> dict:
        """
        This operation gets basic device information from the device.
        - return [dict];
            - Manufacturer [string]
                The manufactor of the device.
            - Model [string]
                The device model.
            - FirmwareVersion [string]
                The firmware version in the device.
            - SerialNumber [string]
                The serial number of the device.
            - HardwareId [string]
                The hardware ID of the device.
        """
        device_info = {}
        if self.onvif_service.get_con_status():
            logger.info(f"Try to GetDeviceInformation information..")
            try:
                zeep_device_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_device = zeep_device_client.create_service("{" + DEVICE_SERVICE_NS + "}DeviceBinding", self.xAddr)
                device_info = ws_client_device.GetDeviceInformation()
            except Exception as emsg:
                logger.error(f"GetDeviceInformation unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetDeviceInformation complete with success..")
        return device_info

    def SetDiscoveryMode(self,discovery_mode = DeviceEnumParams.DiscoveryMode)-> bool:
        '''
        This operation sets the discovery mode operation of a device. See Section 7.2 for the definition of the different device discovery modes. 
        The device shall support configuration of the discovery mode setting through the SetDiscoveryMode command.
        - requirements:
            - discovery_mode  [DiscoveryMode]
                Indicator of discovery mode: Discoverable, NonDiscoverable.    
        - return [boolean]:
            - Set discovery mode status
        '''
        status = False
        if self.onvif_service.get_con_status():
            logger.info(f"Try to SetDiscoveryMode information..")
            try:
                zeep_device_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_device = zeep_device_client.create_service("{" + DEVICE_SERVICE_NS + "}DeviceBinding", self.xAddr)
                ws_client_device.SetDiscoveryMode(DiscoveryMode  = discovery_mode.value)
            except Exception as emsg:
                logger.error(f"SetDiscoveryMode unsuccess.. -> {emsg}")
            else:
                status = True
                logger.info(f"SetDiscoveryMode complete with success..")
        return status

    def GetDiscoveryMode(self) -> dict:
        """
        This operation gets the discovery mode of a device.
        - return [dict];
            - DiscoveryMode [DiscoveryMode]
                Indicator of discovery mode: Discoverable, NonDiscoverable.
        """
        discovery_mode = {}
        if self.onvif_service.get_con_status():
            logger.info(f"Try to GetDiscoveryMode information..")
            try:
                zeep_device_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_device = zeep_device_client.create_service("{" + DEVICE_SERVICE_NS + "}DeviceBinding", self.xAddr)
                discovery_mode = ws_client_device.GetDiscoveryMode()
            except Exception as emsg:
                logger.error(f"GetDiscoveryMode unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetDiscoveryMode complete with success..")
        return discovery_mode

    def SetHostname(self,name : str) -> bool:
        '''
        This operation sets the hostname on a device. 
        It shall be possible to set the device hostname configurations through the SetHostname command.
        - requirements:
            - name [token]
                The hostname to set.   
        - return [boolean]:
            - Set Host name status
        '''
        status = False
        if self.onvif_service.get_con_status():
            logger.info(f"Try to SetHostname information..")
            try:
                zeep_device_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_device = zeep_device_client.create_service("{" + DEVICE_SERVICE_NS + "}DeviceBinding", self.xAddr)
                ws_client_device.SetHostname(Name = name)
            except Exception as emsg:
                logger.error(f"SetHostname unsuccess.. -> {emsg}")
            else:
                status = True
                logger.info(f"SetHostname complete with success..")
        return status

    def GetHostname(self) -> dict:
        """
        This operation is used by an endpoint to get the hostname from a device. 
        The device shall return its hostname configurations through the GetHostname command.
        - return [dict];
            - HostnameInformation [HostnameInformation]
                Contains the hostname information.
        """
        hostname_info = {}
        if self.onvif_service.get_con_status():
            logger.info(f"Try to GetHostname information..")
            try:
                zeep_device_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_device = zeep_device_client.create_service("{" + DEVICE_SERVICE_NS + "}DeviceBinding", self.xAddr)
                hostname_info = ws_client_device.GetHostname()
            except Exception as emsg:
                logger.error(f"GetHostname unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetHostname complete with success..")
        return hostname_info

    def SystemReboot(self) -> dict:
        '''
        This operation reboots the device.
        - return [dict];
            - Message [string]
                Contains the reboot message sent by the device.
        '''
        reboot_message = {}
        if self.onvif_service.get_con_status():
            logger.info(f"Try to SystemReboot..")
            try:
                zeep_device_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_device = zeep_device_client.create_service("{" + DEVICE_SERVICE_NS + "}DeviceBinding", self.xAddr)
                reboot_message = ws_client_device.SystemReboot()
            except Exception as emsg:
                logger.error(f"SystemReboot unsuccess.. -> {emsg}")
            else:
                logger.info(f"SystemReboot complete with success..")
        return reboot_message

    def SetSystemDateAndTime(self,request_message : DeviceRequestMessages.SetSystemDateAndTimeMessage) -> bool:
        """
        This operation sets the device system date and time. 
        The device shall support the configuration of the daylight saving setting and of the manual system date and time (if applicable) or indication of NTP time (if applicable) through the SetSystemDateAndTime command.
        - requirements : 
            - request_message - [SetSystemDateAndTimeMessage] 
                Created new System DateTime object. 
        - return [boolean]:
            - Set System DateTime status
        """
        status = False
        if self.onvif_service.get_con_status():
            logger.info(f"Try to SetSystemDateAndTime..")
            try:
                zeep_device_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_device = zeep_device_client.create_service("{" + DEVICE_SERVICE_NS + "}DeviceBinding", self.xAddr)
                ws_client_device.SetSystemDateAndTime(**request_message.to_dict())
            except Exception as emsg:
                logger.error(f"SetSystemDateAndTime unsuccess.. -> {emsg}")
            else:
                status = True
                logger.info(f"SetSystemDateAndTime complete with success..")
        return status

    def GetSystemDateAndTime(self) -> dict:
        """
        This operation gets the device system date and time. 
        The device shall support the return of the daylight saving setting and of the manual system date and time (if applicable) or indication of NTP time (if applicable) through the GetSystemDateAndTime command.
        - return [dict];
            - SystemDateAndTime [SystemDateTime]
                Contains information whether system date and time are set manually or by NTP, \
                    daylight savings is on or off, time zone in POSIX 1003.1 format and \
                        system date and time in UTC and also local system date and time.
        """
        date_time_info = {}
        if self.onvif_service.get_con_status():
            logger.info(f"Try to GetSystemDateAndTime information..")
            try:
                zeep_device_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_device = zeep_device_client.create_service("{" + DEVICE_SERVICE_NS + "}DeviceBinding", self.xAddr)
                date_time_info = ws_client_device.GetSystemDateAndTime()
            except Exception as emsg:
                logger.error(f"GetSystemDateAndTime unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetSystemDateAndTime complete with success..")
        return date_time_info

    def SetRemoteDiscoveryMode(self,remote_discovery_mode = DeviceEnumParams.DiscoveryMode)-> bool:
        '''
        This operation sets the remote discovery mode of operation of a device. See Section 7.4 for the definition of remote discovery remote extensions.
        A device that supports remote discovery shall support configuration of the discovery mode setting through the SetRemoteDiscoveryMode command.
        - requirements:
            - remote_discovery_mode  [DiscoveryMode]
                Indicator of discovery mode: Discoverable, NonDiscoverable.   
        - return [boolean]:
            - Set discovery mode status
        '''
        status = False
        if self.onvif_service.get_con_status():
            logger.info(f"Try to SetRemoteDiscoveryMode information..")
            try:
                zeep_device_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_device = zeep_device_client.create_service("{" + DEVICE_SERVICE_NS + "}DeviceBinding", self.xAddr)
                ws_client_device.SetRemoteDiscoveryMode(RemoteDiscoveryMode = remote_discovery_mode.value)
            except Exception as emsg:
                logger.error(f"SetRemoteDiscoveryMode unsuccess.. -> {emsg}")
            else:
                status = True
                logger.info(f"SetRemoteDiscoveryMode complete with success..")
        return status
    
    def GetRemoteDiscoveryMode(self) -> dict:
        """
        This operation gets the remote discovery mode of a device. See Section 7.4 for the definition of remote discovery extensions.
        - return [dict];
            - RemoteDiscoveryMode [DiscoveryMode]
                Indicator of discovery mode: Discoverable, NonDiscoverable.
        """
        remote_discoverymode_info = {}
        if self.onvif_service.get_con_status():
            logger.info(f"Try to GetRemoteDiscoveryMode information..")
            try:
                zeep_device_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_device = zeep_device_client.create_service("{" + DEVICE_SERVICE_NS + "}DeviceBinding", self.xAddr)
                remote_discoverymode_info = ws_client_device.GetRemoteDiscoveryMode()
            except Exception as emsg:
                logger.error(f"GetRemoteDiscoveryMode unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetRemoteDiscoveryMode complete with success..")
        return remote_discoverymode_info

    def SetNTP(self,request_message = DeviceRequestMessages.SetNTPMessage)-> bool:
        '''
        This operation sets the NTP settings on a device. If the device supports NTP, it shall be possible to set the NTP server settings through the SetNTP command.
        A device shall accept string formated according to RFC 1123 section 2.1 or alternatively to RFC 952, other string shall be considered as invalid strings.
        Changes to the NTP server list will not affect the clock mode DateTimeType. Use SetSystemDateAndTime to activate NTP operation.
        - requirements : 
            - request_message - [SetNTPMessage] 
                Created SetNTPMessage object. 
        - return [boolean]:
            - Set NTP  status
        '''
        status = False
        if self.onvif_service.get_con_status():
            logger.info(f"Try to SetNTP..")
            try:
                zeep_device_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_device = zeep_device_client.create_service("{" + DEVICE_SERVICE_NS + "}DeviceBinding", self.xAddr)
                ws_client_device.SetNTP(**request_message.to_dict())
            except Exception as emsg:
                logger.error(f"SetNTP unsuccess.. -> {emsg}")
            else:
                status = True
                logger.info(f"SetNTP complete with success..")
        return status
    
    def GetNTP(self) -> dict:
        """
        This operation gets the NTP settings from a device. 
        If the device supports NTP, it shall be possible to get the NTP server settings through the GetNTP command.
        - return [dict];
            - NTPInformation [NTPInformation]
                NTP information.
        """
        ntp_information = {}
        if self.onvif_service.get_con_status():
            logger.info(f"Try to GetNTP information..")
            try:
                zeep_device_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_device = zeep_device_client.create_service("{" + DEVICE_SERVICE_NS + "}DeviceBinding", self.xAddr)
                ntp_information = ws_client_device.GetNTP()
            except Exception as emsg:
                logger.error(f"GetNTP unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetNTP complete with success..")
        return ntp_information