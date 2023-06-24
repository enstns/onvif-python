import datetime
from logging.handlers import RotatingFileHandler
from zeep.client import Client, CachingClient, Settings
from zeep.wsse.username import UsernameToken
import json
import sys
import logging
import os
from zeep.plugins import HistoryPlugin

HISTORY = HistoryPlugin()

LOG = False
DEBUG = True

LOG_FILENAME = "log/onvif_service.log"

logger = logging.getLogger('onvif_service')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# logging.basicConfig(filename="onvif_service.log",format='%(asctime)s - %(levelname)s : %(message)s',level=logging.DEBUG)

if DEBUG:
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

if LOG: 
    log = RotatingFileHandler(LOG_FILENAME, mode='a', maxBytes=5*1024*1024,backupCount=2, encoding=None, delay=True)
    # log = logging.FileHandler(filename=LOG_FILENAME, mode='w', encoding=None, delay=False, errors=None)
    log.setLevel(logging.DEBUG)
    log.setFormatter(formatter)
    logger.addHandler(log)

SETTINGS = Settings()
SETTINGS.strict = False
SETTINGS.xml_huge_tree = True

DEVICE_SERVICE_NS = "http://www.onvif.org/ver10/device/wsdl"
MEDIA_SERVICE_NS = "http://www.onvif.org/ver10/media/wsdl"
IMAGING_SERVICE_NS = "http://www.onvif.org/ver10/image/wsdl"
PTZ_SERVICE_NS = "http://www.onvif.org/ver10/ptz/wsdl"

def isfile_exist(path = "wsdl/test.txt"):
    return os.path.isfile(path)

def get_caching_client(isAuth = True,wsdl_URL = "wsdl/devicemgmt.wsdl",username_token = UsernameToken(username="admin",password="9999")):
    global SETTINGS
    caching_client = None
    if isfile_exist(wsdl_URL) or wsdl_URL.find("http://www.onvif.org") != -1:
        try:
            if isAuth: 
                caching_client = CachingClient(wsdl=wsdl_URL, wsse=username_token, settings=SETTINGS,plugins=[HISTORY])
            else: 
                caching_client = CachingClient(wsdl=wsdl_URL, settings=SETTINGS,plugins=[HISTORY])
        except Exception as emsg:
            logger.error(f"Create caching client exception : \n{emsg}")
    else:
        logger.error(f"No such a file directory : {str(wsdl_URL)}")
    return caching_client

class OnvifService:
    def __init__(self,ip = "192.168.1.168",username = "admin" , password = "9999",port = 80,wsdldirectory = "wsdl") -> None:
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        self.con_xaddr = "http://192.168.1.168:80/onvif/device_service"
        self.device_created_time = datetime.datetime.now()
        self.first_local_time = datetime.datetime.now()
        self.wsdl_directory = wsdldirectory
        self.capabilities = {}
        self.device_info = {}
        self.profiles = []
        self.services = []
        self.con_status = False
        self.username_token = UsernameToken(username=self.username,password=self.password,zulu_timestamp=True, use_digest=True)

    def get_con_xaddr(self) -> str:
        return "http://"+ str(self.ip) +":"+ str(self.port) +"/onvif/device_service"

    def get_con_status(self) -> bool:
        return self.con_status

    def get_username_token(self) -> UsernameToken(username="admin",password="9999"):
        created_time = datetime.datetime.now() - self.first_local_time + self.device_created_time
        self.username_token = UsernameToken(username = self.username,password= self.password, created = created_time,zulu_timestamp=True, use_digest=True)
        return self.username_token

    def get_device_time(self,xaddr = "http://192.168.1.168:80/onvif/device_service") -> dict: 
        response = {}
        global DEVICE_SERVICE_NS
        try:            
            zeep_client_device = get_caching_client(isAuth = True,wsdl_URL= self.wsdl_directory + "/devicemgmt.wsdl",username_token=self.get_username_token())
            if zeep_client_device != None:
                ws_client_device = zeep_client_device.create_service("{" + DEVICE_SERVICE_NS + "}DeviceBinding", xaddr)
                response = ws_client_device.GetSystemDateAndTime()
            else:
                self.con_status = False
        except Exception as emsg:
            logger.error(f"Get device time exception : \n{emsg}")
            self.con_status = False
        
        if zeep_client_device != None and response:
            self.con_status = True
            try:
                self.device_created_time = datetime.datetime(year=response["UTCDateTime"]["Date"]["Year"],\
                                                            month=response["UTCDateTime"]["Date"]["Month"],\
                                                                day=response["UTCDateTime"]["Date"]["Day"],\
                                                                    hour=response["UTCDateTime"]["Time"]["Hour"],\
                                                                        minute=response["UTCDateTime"]["Time"]["Minute"],\
                                                                            second=response["UTCDateTime"]["Time"]["Second"])
            except Exception as emsg:
                logger.error(f"Create device time exception : \n{emsg}")

        return response
                 
    def get_capabilities(self,xaddr = "http://192.168.1.168:80/onvif/device_service",category = "All") -> dict:
        global DEVICE_SERVICE_NS
        capabilities = {}
        try:
            zeep_client_device = get_caching_client(isAuth = True,wsdl_URL= self.wsdl_directory + "/devicemgmt.wsdl",username_token=self.get_username_token())
            ws_client_device = zeep_client_device.create_service("{" + DEVICE_SERVICE_NS + "}DeviceBinding", xaddr)
            capabilities = ws_client_device.GetCapabilities(Category = category) 
        except Exception as emsg:
            logger.error(f'Get capabilities error : \n{emsg}\n')
        return capabilities

    def get_services(self,xaddr = "http://192.168.1.168:80/onvif/device_service" , include_capability = False) -> list:
        global DEVICE_SERVICE_NS
        services = []
        try:
            zeep_client_device = get_caching_client(isAuth = True,wsdl_URL= self.wsdl_directory + "/devicemgmt.wsdl",username_token=self.get_username_token())
            ws_client_device = zeep_client_device.create_service("{" + DEVICE_SERVICE_NS + "}DeviceBinding", xaddr)
            services = ws_client_device.GetServices(IncludeCapability = str(include_capability).lower()) 
        except Exception as emsg:
            logger.error(f'Get services error : \n{emsg}\n')
        return services

    def get_profiles(self,xaddr = "http://192.168.1.168:80/onvif/media_service") -> list:
        global MEDIA_SERVICE_NS
        profiles = []
        try:
            zeep_client_media = get_caching_client(isAuth= True,wsdl_URL=self.wsdl_directory+"/media.wsdl",username_token=self.get_username_token())
            ws_client_media = zeep_client_media.create_service("{" + MEDIA_SERVICE_NS + "}MediaBinding", xaddr)                               
            profiles = ws_client_media.GetProfiles()
        except Exception as emsg:
            logger.error(f'Get profiles error : \n{emsg}\n')
        return profiles

    def get_first_profile(self) -> dict:
        first_profile = None
        try:
            first_profile = self.profiles[0]    
        except Exception as emsg:
            logger.error(f"can not get_first_profile : \n{emsg}")
        return first_profile
            
    def get_device_information(self,xaddr = "http://192.168.1.168:80/onvif/device_service"):
        # GetDeviceInformation
        global DEVICE_SERVICE_NS
        device_info = {}
        try:
            zeep_client_device = get_caching_client(isAuth = True,wsdl_URL= self.wsdl_directory + "/devicemgmt.wsdl",username_token=self.get_username_token())
            ws_client_device = zeep_client_device.create_service("{" + DEVICE_SERVICE_NS + "}DeviceBinding", xaddr)
            device_info = ws_client_device.GetDeviceInformation() 
        except Exception as emsg:
            logger.error(f'Get device info error : \n{emsg}\n')
        return device_info

    def connect_onvif(self):
        global DEVICE_SERVICE_NS  
        logger.info(f"Try to connect onvif device : {str(self.ip)}")
        self.get_device_time(xaddr=self.get_con_xaddr())
        if self.get_con_status():
            logger.info(f"Device connection successful : {str(self.ip)}")
            logger.info(f"Onvif device connection complete with succes.. {str(self.ip)}")
            logger.info(f"Try to get device informations..")
            self.device_info = self.get_device_information(xaddr=self.get_con_xaddr())
            if self.device_info:
                logger.info(f"Getting device informations complete with success..")
                logger.info(f"Try to get device capabilities..")
                self.capabilities = self.get_capabilities(xaddr=self.get_con_xaddr())
                if self.capabilities:
                    logger.info(f"Getting device capabilities complete with success..")
                    logger.info(f"Try to get device profiles..")
                    self.profiles = self.get_profiles(xaddr= self.capabilities["Media"]["XAddr"])
                    if self.profiles:
                        logger.info(f"Getting device profiles complete with success..")
                        logger.info(f"Try to get device services..")
                        self.services = self.get_services(xaddr=self.get_con_xaddr(),include_capability=False)
                        if self.services:
                            logger.info(f"Getting device services complete with success..")
                        else:
                            logger.error(f'Can not Getting device services for {self.ip}\n')
                    else:
                        logger.error(f'Can not Getting device profiles for {self.ip}\n')
                else:
                    logger.error(f'Can not Getting device capabilities for {self.ip}\n')
            else:
                logger.error(f'Can not Getting device information for {self.ip}\n')
        else:
            logger.error(f'No onvif connection to : {self.ip}\n')

    def get_history(self):
        global HISTORY
        return HISTORY
            
            



            


    