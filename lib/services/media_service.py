"""
Created to control Onvif Media service properties.

craeted by : enstns
created time : 01.04.23
"""
import datetime
import logging
import requests
from requests.auth import HTTPDigestAuth

from lib.onvif import OnvifService, get_caching_client
from lib.requests_messages.media_request_messages import MediaRequestMessages

DEBUG = True
LOG = False

logger = logging.getLogger('media_service')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

MEDIA_SERVICE_NS = "http://www.onvif.org/ver10/media/wsdl"

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

def get_media_namespace(services = [],xaddr=""):
    if services and services != None:
        for serv in services:
            ns = str(serv.Namespace)
            if serv.XAddr == xaddr and "media" in ns:
                return serv.Namespace
    else:
        return None
     
class MediaService:
    def __init__(self,onvif_service = OnvifService()) -> None:
        self.is_media_service_supported = False
        self.onvif_service = onvif_service
        self.wsdlUrl = ""
        self.xAddr = "" 
        self.media_name_space = ""
        self.profiles = None
        self.media_capabilities = {}
        self.set_media_service_variables()

    def set_media_service_variables(self) -> None:
        if self.onvif_service.get_con_status() and self.onvif_service.capabilities.Media != None:
            self.is_media_service_supported = True
            self.xAddr = self.onvif_service.capabilities.Media.XAddr
            self.wsdlUrl = self.onvif_service.wsdl_directory + "/media.wsdl"
            self.media_name_space = get_media_namespace(services = self.onvif_service.services,xaddr = self.xAddr)
            # self.media_name_space = "http://www.onvif.org/ver10/media/wsdl"
            self.profiles = self.GetProfiles()
            self.media_capabilities = self.GetServiceCapabilities()
        else:
            logger.error(f"Imaging service not sported from {self.onvif_service.ip}")
     
    def GetServiceCapabilities(self) -> dict:
        """
        This command lists all available physical video inputs of the device.
        - return; [dict]
            - Capabilities [Capabilities]
                The capabilities for the imaging service is returned in the Capabilities element.
                - ImageStabilization [boolean]
                    Indicates whether or not Image Stabilization feature is supported. The use of this capability is deprecated, a client should use GetOption to find out if image stabilization is supported.
                - Presets [boolean]
                    Indicates whether or not Imaging Presets feature is supported.
                - AdaptablePreset [boolean]
                    Indicates whether or not imaging preset settings can be updated.
        """
        service_cap = {}
        if self.is_media_service_supported:
            logger.info(f"Try to GetServiceCapabilities information..")
            try:
                zeepMediaClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_media = zeepMediaClient.create_service("{" + self.media_name_space + "}MediaBinding", self.xAddr)
                service_cap = ws_client_media.GetServiceCapabilities()
            except Exception as emsg:
                logger.error(f"GetServiceCapabilities unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetServiceCapabilities complete with success..")
        return service_cap
    
    def GetVideoSources(self) -> list:
        """
        This command lists all available physical video inputs of the device.
        - return [list];
            - VideoSources - optional, unbounded; [VideoSource]
                List of existing Video Sources
        """
        video_sources = {}
        if self.is_media_service_supported:
            logger.info(f"Try to GetVideoSources information..")
            try:
                zeepMediaClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_media = zeepMediaClient.create_service("{" + self.media_name_space + "}MediaBinding", self.xAddr)
                video_sources = ws_client_media.GetVideoSources()
            except Exception as emsg:
                logger.error(f"GetVideoSources unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetVideoSources complete with success..")
        return video_sources

    def GetProfiles(self) -> dict:
        """
        This command lists all available physical video inputs of the device.
        - return;
            - Profiles - optional, unbounded; [Profile]
                lists all profiles that exist in the media service
        """
        profiles = {}
        if self.is_media_service_supported:
            logger.info(f"Try to GetProfiles information..")
            try:
                zeepMediaClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_media = zeepMediaClient.create_service("{" + self.media_name_space + "}MediaBinding", self.xAddr)
                profiles = ws_client_media.GetProfiles()
            except Exception as emsg:
                logger.error(f"GetProfiles unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetProfiles complete with success..")
        return profiles

    def GetStreamUri(self,request_message : MediaRequestMessages.GetStreamUriMessage) -> dict:
        """        
        This operation requests a URI that can be used to initiate a live media stream using RTSP as the control protocol. The returned URI shall remain valid indefinitely even if the profile is changed. The ValidUntilConnect, ValidUntilReboot and Timeout Parameter shall be set accordingly (ValidUntilConnect=false, ValidUntilReboot=false, timeout=PT0S).

        The correct syntax for the StreamSetup element for these media stream setups defined in 5.1.1 of the streaming specification are as follows:
            1 - RTP unicast over UDP: StreamType = "RTP_unicast", TransportProtocol = "UDP"
            2 - RTP over RTSP over HTTP over TCP: StreamType = "RTP_unicast", TransportProtocol = "HTTP"
            3 - RTP over RTSP over TCP: StreamType = "RTP_unicast", TransportProtocol = "RTSP"

        If a multicast stream is requested at least one of VideoEncoderConfiguration, AudioEncoderConfiguration and MetadataConfiguration shall have a valid multicast setting.

        For full compatibility with other ONVIF services a device should not generate Uris longer than 128 octets.

        - reqirements;
            - request_message -> [GetStreamUriRequestParams] 
        - return:
            - [dict] GetStreamUriResponse;
                - MediaUri [MediaUri]
                    - Uri [anyURI]
                        Stable Uri to be used for requesting the media stream
                    - InvalidAfterConnect [boolean]
                        Indicates if the Uri is only valid until the connection is established. The value shall be set to "false".
                    - InvalidAfterReboot [boolean]
                        Indicates if the Uri is invalid after a reboot of the device. The value shall be set to "false".
                    - Timeout [duration]
                        Duration how long the Uri is valid. This parameter shall be set to PT0S to indicate that this stream URI is indefinitely valid even if the profile changes
        """
        stream_uri = {}
        if self.is_media_service_supported:
            logger.info(f"Try to GetStreamUri..")
            try:
                zeepMediaClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_media = zeepMediaClient.create_service("{" + self.media_name_space + "}MediaBinding", self.xAddr)
                stream_uri = ws_client_media.GetStreamUri(**request_message.to_dict())
            except Exception as emsg:
                logger.error(f"GetStreamUri unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetStreamUri complete with success..")
                logger.info(f"Stream URI : {stream_uri.Uri}")
        else:
            logger.warning(f"GetStreamUri unsuccess, Media service not supported!")
        return stream_uri

    def GetSnapshotUri(self,profile_token : str) -> dict:
        """
        This command lists all available physical video inputs of the device.
        - requirements; 
            - profile_token : [string] 
                The ProfileToken element indicates the media profile to use and will define the source and dimensions of the snapshot.
        - return;
            - GetSnapshotUri [dict]
        """
        snapshot_uri = None
        if self.is_media_service_supported:
            logger.info(f"Try to GetSnapshotUri information..")
            try:
                zeepMediaClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_media = zeepMediaClient.create_service("{" + self.media_name_space + "}MediaBinding", self.xAddr)
                snapshot_uri = ws_client_media.GetSnapshotUri(ProfileToken=profile_token)
            except Exception as emsg:
                logger.error(f"GetSnapshotUri unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetSnapshotUri complete with success..")
        return snapshot_uri
    
    def DownloadSnapshot(self,snap_shot_uri : str,path = "download") -> bool:
        """
        This download image from and URI to the given location path
        - requirements:
            - snap_shot_uri -> Image URL
            - path -> Download location
        - return;
            - status [boolean]
                Download image status
        """
        cam_auth=HTTPDigestAuth(self.onvif_service.username, self.onvif_service.password)
        download_status = False
        image_location = f'{path}/{self.onvif_service.ip}_{datetime.datetime.now().strftime(f"%y%m%dT%H%M%S")}.jpg'
        logger.info(f"Try to DownloadSnapshot image -> {image_location} ..")
        try:
            response = requests.get(snap_shot_uri.Uri, stream = True,auth=cam_auth,timeout=1)
            if response.status_code == 200:
                response.raw.decode_content = True
                with open(image_location, 'wb') as outfile:
                    outfile.write(response.content)
            else:
                logger.error(f"DownloadSnapshot image Request unsuccess -> {response.status_code} - {response.reason}")
        except Exception as emsg:
            logger.error(f"DownloadSnapshot image unsuccess.. -> {emsg}")
        else:
            download_status = True
            logger.info(f"DownloadSnapshot image complete with success {image_location}")
        return download_status

    def GetVideoSourceConfigurations(self) -> list:
        """
        Returns the capabilities of the media service. The result is returned in a typed answer.
        - return [list];
            - Configurations - optional, unbounded; [VideoSourceConfiguration]
                This element contains a list of video source configurations.
        """
        videosource_configs = []
        if self.is_media_service_supported:
            logger.info(f"Try to GetVideoSourceConfigurations information..")
            try:
                zeepMediaClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_media = zeepMediaClient.create_service("{" + self.media_name_space + "}MediaBinding", self.xAddr)
                videosource_configs = ws_client_media.GetVideoSourceConfigurations()
            except Exception as emsg:
                logger.error(f"GetVideoSourceConfigurations unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetVideoSourceConfigurations complete with success..")
        return videosource_configs

    def GetCompatibleVideoAnalyticsConfigurations(self,profile_token : str) -> list:
        """
        This operation requests all video analytic configurations of the device that are compatible with a certain media profile. 
        Each of the returned configurations shall be a valid input parameter for the AddVideoAnalyticsConfiguration command on the media profile. 
        The result varies depending on the capabilities, configurations and settings in the device.
        - requirements; 
            - profile_token : [str]
                Contains the token of an existing media profile the configurations shall be compatible with.
        - return [list];
            - Configurations - optional, unbounded; [VideoAnalyticsConfiguration]
                Contains a list of video analytics configurations that are compatible with the specified media profile.
        """
        configurations = []
        if self.is_media_service_supported:
            logger.info(f"Try to GetCompatibleVideoAnalyticsConfigurations information..")
            try:
                zeepMediaClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_media = zeepMediaClient.create_service("{" + self.media_name_space + "}MediaBinding", self.xAddr)
                configurations = ws_client_media.GetCompatibleVideoAnalyticsConfigurations(ProfileToken  = profile_token)
            except Exception as emsg:
                logger.error(f"GetCompatibleVideoAnalyticsConfigurations unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetCompatibleVideoAnalyticsConfigurations complete with success..")
        return configurations
    
    def GetOSD(self,osd_token : str) -> dict:
        """
        This command lists all available physical video inputs of the device.
        - requirements; 
            - osd_token : [ReferenceToken] 
                The GetOSD command fetches the OSD configuration if the OSD token is known.
        - return [dict];
            - OSD [OSDConfiguration]
                The requested OSD configuration.
        """
        osd = {}
        if self.is_media_service_supported and self.media_capabilities.OSD:
            logger.info(f"Try to GetOSD information..")
            try:
                zeepMediaClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_media = zeepMediaClient.create_service("{" + self.media_name_space + "}MediaBinding", self.xAddr)
                osd = ws_client_media.GetOSD(OSDToken = osd_token)
            except Exception as emsg:
                logger.error(f"GetOSD unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetOSD complete with success..")
        else: logger.warning(f"GetOSD is not supported !")
        return osd

    def GetOSDs(self,configuration_token = None) -> dict:
        """
        This command lists all available physical video inputs of the device.
        - requirements: 
            - configuration_token : optional [ReferenceToken] 
                Token of the Video Source Configuration, which has OSDs associated with are requested. If token not exist, request all available OSDs.
        - return;
            - OSDS [list] : list of OSD
        """
        osds = []
        if self.is_media_service_supported and self.media_capabilities.OSD:
            logger.info(f"Try to GetOSDs information..")
            try:
                zeepMediaClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_media = zeepMediaClient.create_service("{" + self.media_name_space + "}MediaBinding",self.xAddr)
                osds = ws_client_media.GetOSDs(ConfigurationToken=configuration_token)
            except Exception as emsg:
                logger.error(f"GetOSDs unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetOSDs complete with success..")
        else: logger.warning(f"GetOSDs is not supported !")
        return osds
    
    def GetOSDOptions(self,configuration_token : str) -> dict:
        """
        This command lists all available physical video inputs of the device.
        - requirements: 
            - configuration_token : optional [ReferenceToken] 
                Token of the Video Source Configuration, which has OSDs associated with are requested. If token not exist, request all available OSDs.
        - return [dict];
            - OSDOptions [OSDConfigurationOptions]
        """
        osd_options = {}
        if self.is_media_service_supported and self.media_capabilities.OSD:
            logger.info(f"Try to GetOSDOptions information..")
            try:
                zeepMediaClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_media = zeepMediaClient.create_service("{" + self.media_name_space + "}MediaBinding", self.xAddr)
                osd_options = ws_client_media.GetOSDOptions(ConfigurationToken=configuration_token)
            except Exception as emsg:
                logger.error(f"GetOSDOptions unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetOSDOptions complete with success..")
        else: logger.warning(f"GetOSDOptions is not supported !")
        return osd_options
    
    def DeleteOSD(self,osd_token : str) -> bool:
        """
        This command lists all available physical video inputs of the device.
        - requirements : 
            - osd_token : [ReferenceToken] 
                This element contains a reference to the OSD configuration that should be deleted.
        - return [boolean]; 
            - DeleteOSD status
        """
        delete_status = False
        if self.is_media_service_supported and self.media_capabilities.OSD:
            logger.info(f"Try to DeleteOSD information..")
            try:
                zeepMediaClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_media = zeepMediaClient.create_service("{" + self.media_name_space + "}MediaBinding", self.xAddr)
                ws_client_media.DeleteOSD(OSDToken = osd_token)
            except Exception as emsg:
                logger.error(f"DeleteOSD unsuccess.. -> {emsg}")
            else:
                logger.info(f"DeleteOSD complete with success..")
                delete_status = True
        else: logger.warning(f"DeleteOSD is not supported !")
        return delete_status
    
    def CreateOSD(self,request_message : MediaRequestMessages.CreateOSDMessage) -> str:
        """
        This command lists all available physical video inputs of the device.
        - reqirements : 
            - request_message : [CreateOSDMessage]
                An Object for Create OSD Request message 
        - return [str];
            - OSD Token
        """
        osd_token = ""
        if self.is_media_service_supported and self.media_capabilities.OSD:
            logger.info(f"Try to CreateOSD request..")
            try:
                zeepMediaClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_media = zeepMediaClient.create_service("{" + self.media_name_space + "}MediaBinding", self.xAddr)
                osd_token_response = ws_client_media.CreateOSD(**request_message.to_dict())
                osd_token = osd_token_response.OSDToken
            except Exception as emsg:
                logger.error(f"CreateOSD unsuccess.. -> {emsg}")
            else:
                logger.info(f"CreateOSD complete with success..")
                logger.info(f"Created OSD Token : {osd_token}")
        else: logger.warning(f"CreateOSD is not supported !")
        return osd_token
   