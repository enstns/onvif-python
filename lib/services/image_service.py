"""
Created to control Onvif Image service properties.

craeted by : enstns
created time : 01.04.23
"""
from zeep.client import Settings
import logging
from zeep.wsse.utils import WSU

from lib.onvif import OnvifService, get_caching_client
from lib.requests_messages.image_request_messages import ImageRequestMessages

DEBUG = True
LOG = False

logger = logging.getLogger('imaging_service')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

IMAGING_SERVICE_NS = "http://www.onvif.org/ver10/image/wsdl"

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

def get_image_namespace(services = [],xaddr=""):
    if services and services != None:
        for serv in services:
            ns = str(serv.Namespace)
            if serv.XAddr == xaddr and "imaging" in ns:
                return serv.Namespace
    else:
        return None

class ImageService:
    def __init__(self,onvif_service = OnvifService()) -> None:
        self.is_imaging_service_supported = False
        self.onvif_service = onvif_service
        self.wsdlUrl = ""
        self.xAddr = ""
        self.image_name_space = ""
        self.video_source_token = None
        self.set_image_service_variables()

    def set_image_service_variables(self) -> None:
        if self.onvif_service.get_con_status() and self.onvif_service.capabilities.Imaging != None:
            self.is_imaging_service_supported = True
            self.wsdlUrl = self.onvif_service.wsdl_directory + "/imaging.wsdl"
            self.xAddr = self.onvif_service.capabilities.Imaging.XAddr
            self.image_name_space = get_image_namespace(services = self.onvif_service.services,xaddr=self.xAddr)
            self.video_source_token = self.onvif_service.get_first_profile().VideoSourceConfiguration.SourceToken
        else:
            logger.error(f"Imaging service not sported from {self.onvif_service.ip}")
            
    def GetImagingSettings(self,vs_token = None) -> dict:
        """
        Get the ImagingConfiguration for the requested VideoSource.
        - requirements; 
            - vs_token : [string] 
                Reference token to the VideoSource for which the ImagingSettings.
        - return;
            - ImagingSettings [dict]
                ImagingSettings for the VideoSource that was requested.
        """
        image_settings = {}
        if vs_token == None: vs_token = self.video_source_token
        if self.is_imaging_service_supported and self.video_source_token != None:
            logger.info(f"Try to GetImagingSettings information..")
            try:
                zeepImageClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_image = zeepImageClient.create_service("{" + self.image_name_space + "}ImagingBinding", self.xAddr)
                image_settings = ws_client_image.GetImagingSettings(VideoSourceToken = vs_token)
            except Exception as emsg:
                logger.error(f"GetImagingSettings unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetImagingSettings complete with success..")
        return image_settings

    def GetCurrentPreset(self,vs_token = None) -> dict:
        """
        Via this command the last Imaging Preset applied can be requested. If the camera configuration does not match any of the existing Imaging Presets, the output of GetCurrentPreset shall be Empty. GetCurrentPreset shall return 0 if Imaging Presets are not supported by the Video Source.
        - requirements; 
            - vs_token : [string] 
                Reference token to the VideoSource where the current Imaging Preset should be requested.
        - return;
            - CurrentPreset [dict]
                Current Imaging Preset in use for the specified Video Source.
        """
        current_preset = {}
        if vs_token == None: vs_token = self.video_source_token
        if self.is_imaging_service_supported and self.video_source_token != None:
            logger.info(f"Try to GetCurrentPreset information..")
            try:
                zeepImageClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_image = zeepImageClient.create_service("{" + self.image_name_space + "}ImagingBinding", self.xAddr)
                current_preset = ws_client_image.GetCurrentPreset(VideoSourceToken = vs_token)
            except Exception as emsg:
                logger.error(f"GetCurrentPreset unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetCurrentPreset complete with success..")
        return current_preset

    def GetMoveOptions(self,vs_token = None) -> dict:
        """
        Imaging move operation options supported for the Video source.
        - requirements; 
            - vs_token : [string] 
                Reference token to the VideoSource for the requested move options.
        - return;
            - MoveOptions [dict]
                Valid ranges for the focus lens move options.
        """
        move_options = {}
        if vs_token == None: vs_token = self.video_source_token
        if self.is_imaging_service_supported and self.video_source_token != None:
            logger.info(f"Try to GetMoveOptions information..")
            try:
                zeepImageClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_image = zeepImageClient.create_service("{" + self.image_name_space + "}ImagingBinding", self.xAddr)
                message = zeepImageClient.get_element("ns0:GetMoveOptions")
                message.VideoSourceToken = vs_token
                move_options = ws_client_image.GetMoveOptions(VideoSourceToken=vs_token)
            except Exception as emsg:
                logger.error(f"GetMoveOptions unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetMoveOptions complete with success..")
        return move_options

    def GetOptions(self,vs_token = None) -> dict:
        """
        This operation gets the valid ranges for the imaging parameters that have device specific ranges. This command is mandatory for all device implementing the imaging service. 
        The command returns all supported parameters and their ranges such that these can be applied to the SetImagingSettings command.
        For read-only parameters which cannot be modified via the SetImagingSettings command only a single option or identical Min and Max values is provided.
        - requirements; 
            - vs_token : [string] 
                Reference token to the VideoSource for which the imaging parameter options are requested.
        - return;
            - ImagingOptions [dict]
                Valid ranges for the imaging parameters that are categorized as device specific.
        """
        options = {}
        if vs_token == None: vs_token = self.video_source_token
        if self.is_imaging_service_supported and self.video_source_token != None:
            logger.info(f"Try to GetOptions information..")
            try:
                zeepImageClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_image = zeepImageClient.create_service("{" + self.image_name_space + "}ImagingBinding", self.xAddr)
                options = ws_client_image.GetOptions(VideoSourceToken = vs_token)
            except Exception as emsg:
                logger.error(f"GetOptions unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetOptions complete with success..")
        return options

    def GetPresets(self,vs_token = None) -> list:
        """
        Via this command the list of available Imaging Presets can be requested.
        - requirements; 
            - vs_token : [string] 
                A reference to the VideoSource where the operation should take place.
        - return;
            - Presets [list]
                List of Imaging Presets which are available for the requested VideoSource.
        """
        presets = {}
        if vs_token == None: vs_token = self.video_source_token
        if self.is_imaging_service_supported and self.video_source_token != None:
            logger.info(f"Try to GetPresets information..")
            try:
                zeepImageClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_image = zeepImageClient.create_service("{" + self.image_name_space + "}ImagingBinding", self.xAddr)
                presets = ws_client_image.GetPresets(VideoSourceToken = vs_token)
            except Exception as emsg:
                logger.error(f"GetPresets unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetPresets complete with success..")
        return presets

    def GetServiceCapabilities(self) -> dict:
        """
        Returns the capabilities of the imaging service. The result is returned in a typed answer.
        - return;
            - Capabilities [dict]
                The capabilities for the imaging service is returned in the Capabilities element.
        """
        service_cap = {}
        if self.is_imaging_service_supported and self.video_source_token != None:
            logger.info(f"Try to GetServiceCapabilities information..")
            try:
                zeepImageClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_image = zeepImageClient.create_service("{" + self.image_name_space + "}ImagingBinding", self.xAddr)
                service_cap = ws_client_image.GetServiceCapabilities()
            except Exception as emsg:
                logger.error(f"GetServiceCapabilities unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetServiceCapabilities complete with success..")
        return service_cap

    def GetStatus(self,vs_token = None) -> dict:
        """
        Via this command the current status of the Move operation can be requested. 
        Supported for this command is available if the support for the Move operation is signalled via GetMoveOptions.
        - requirements; 
            - vs_token : [string] 
                Reference token to the VideoSource where the imaging status should be requested.
        - return;
            - ImagingStatus [dict]
                Requested imaging status.
        """
        status_info = {}
        if vs_token == None: vs_token = self.video_source_token
        if self.is_imaging_service_supported and self.video_source_token != None:
            logger.info(f"Try to GetStatus information..")
            try:
                zeepImageClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_image = zeepImageClient.create_service("{" + self.image_name_space + "}ImagingBinding", self.xAddr)
                status_info = ws_client_image.GetStatus(VideoSourceToken = vs_token)
            except Exception as emsg:
                logger.error(f"GetStatus unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetStatus complete with success..")
        return status_info

    def GetServiceCapabilities(self) -> dict:
        """
        Returns the capabilities of the imaging service. The result is returned in a typed answer.
        - return;
            - Capabilities [dict]
                The capabilities for the imaging service is returned in the Capabilities element.
        """
        service_cap = {}
        if self.is_imaging_service_supported and self.video_source_token != None:
            logger.info(f"Try to GetServiceCapabilities information..")
            try:
                zeepImageClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_image = zeepImageClient.create_service("{" + self.image_name_space + "}ImagingBinding", self.xAddr)
                service_cap = ws_client_image.GetServiceCapabilities()
            except Exception as emsg:
                logger.error(f"GetServiceCapabilities unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetServiceCapabilities complete with success..")
        return service_cap

    def SetCurrentPreset(self,preset_token : str,vs_token = None) -> bool: # not tested
        """
        The SetCurrentPreset command shall request a given Imaging Preset to be applied to the specified Video Source. 
        SetCurrentPreset shall only be available for Video Sources with Imaging Presets Capability. 
        Imaging Presets are defined by the Manufacturer, and offered as a tool to simplify Imaging Settings adjustments for specific scene content. 
        When the new Imaging Preset is applied by SetCurrentPreset, the Device shall adjust the Video Source settings to match those defined by the specified Imaging Preset.
        - requirements; 
            - vs_token : [string] 
                Reference token to the VideoSource to which the specified Imaging Preset should be applied.
            - preset_token : [string] 
                Reference token to the Imaging Preset to be applied to the specified Video Source.
        - return;
            - Set Preset Status [boolean]
                SetCurrentPresetResponse status.
        """
        if vs_token == None: vs_token = self.video_source_token
        if self.is_imaging_service_supported and self.video_source_token != None:
            logger.info(f"Try to SetCurrentPreset with {preset_token}..")
            try:
                zeepImageClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_image = zeepImageClient.create_service("{" + self.image_name_space + "}ImagingBinding", self.xAddr)
                ws_client_image.SetCurrentPreset(VideoSourceToken = vs_token,PresetToken = preset_token)
            except Exception as emsg:
                logger.error(f"SetCurrentPreset unsuccess.. -> {emsg}")
            else:
                logger.info(f"SetCurrentPreset complete with success..")
        else:
            logger.warning(f"SetCurrentPreset unsuccess, please define a preset_token!")

    def SetImagingSettings(self,request_message : ImageRequestMessages.SetImagingSettingsMessage) -> bool:
        """
        Set the ImagingConfiguration for the requested VideoSource.
        - requirements; 
            - request_message:
                SetImagingSettings request message Object
        - return;
            - Set Imaging Settings Status [boolean]
                SetImagingSettingsResponse status.
        """
        set_image_status = False
        if self.is_imaging_service_supported and self.video_source_token != None:
            logger.info(f"Try to SetImagingSettings..")
            try:
                zeepImageClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_image = zeepImageClient.create_service("{" + self.image_name_space + "}ImagingBinding", self.xAddr)
                ws_client_image.SetImagingSettings(**request_message.to_dict())
            except Exception as emsg:
                logger.error(f"SetImagingSettings unsuccess.. -> {emsg}")
            else:
                logger.info(f"SetImagingSettings complete with success..")
                set_image_status = True
        else:
            logger.warning(f"SetImagingSettings unsuccess, please define a focus dict!")
        return set_image_status

    def Move(self,request_message : ImageRequestMessages.MoveMessage) -> bool: # control move options
        """
        The Move command moves the focus lens in an absolute, a relative or in a continuous manner from its current position. The speed argument is optional for absolute and relative control, but required for continuous. If no speed argument is used, the default speed is used. Focus adjustments through this operation will turn off the autofocus. A device with support for remote focus control should support absolute, relative or continuous control through the Move operation. The supported MoveOpions are signalled via the GetMoveOptions command. At least one focus control capability is required for this operation to be functional.
        The move operation contains the following commands:
        Absolute – Requires position parameter and optionally takes a speed argument. A unitless type is used by default for focus positioning and speed. Optionally, if supported, the position may be requested in m-1 units.
        Relative – Requires distance parameter and optionally takes a speed argument. Negative distance means negative direction. Continuous – Requires a speed argument. Negative speed argument means negative direction.
        - reqirements : 
            - request_message : [MoveMessage]
                An Object for Move Request message 
        - return [boolean] Move status
        """
        status = False
        if self.onvif_service.get_con_status():
            logger.info(f"Try to Move request..")
            if self.is_imaging_service_supported and self.video_source_token != None:
                try:
                    zeep_device_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_device = zeep_device_client.create_service("{" + self.image_name_space + "}ImagingBinding", self.xAddr)
                    ws_client_device.Move(**request_message.to_dict())
                except Exception as emsg:
                    logger.error(f"Move unsuccess.. -> {emsg}")
                else:
                    status = True
                    logger.info(f"Move complete with success..")
            else:
                logger.error(f"Image Service not supported..")
        return status

    def Stop(self,vs_token = None) -> bool:
        """
        The Stop command stops all ongoing focus movements of the lense. 
        A device with support for remote focus control as signalled via the GetMoveOptions supports this command.
        The operation will not affect ongoing autofocus operation.
        - requirements; 
            - vs_token : [string] 
                Reference token to the VideoSource where the focus movement should be stopped.
        - return;
            - Stop Status [boolean]
        """
        stop_status = False
        if vs_token == None: vs_token = self.video_source_token
        if self.is_imaging_service_supported and self.video_source_token != None:
            logger.info(f"Try to Stop moving..")
            try:
                zeepImageClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_image = zeepImageClient.create_service("{" + self.image_name_space + "}ImagingBinding", self.xAddr)
                ws_client_image.Stop(VideoSourceToken = vs_token)
            except Exception as emsg:
                logger.error(f"Stop moving unsuccess.. -> {emsg}")
            else:
                logger.info(f"Stop moving complete with success..")
                stop_status = True
        return stop_status

