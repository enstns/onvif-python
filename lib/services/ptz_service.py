"""
Created to control Onvif PTZ service properties.

craeted by : enstns
created time : 01.04.23
"""
import logging

from lib.onvif import OnvifService, get_caching_client
from lib.requests_messages.ptz_request_messages import PTZRequestMessages
from lib.params.ptz_request_params import PTZEnumParams

DEBUG = True
LOG = False

logger = logging.getLogger('ptz_service')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

PTZ_SERVICE_NS = "http://www.onvif.org/ver10/ptz/wsdl"

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

def get_ptz_namespace(services = [],xaddr=""):
    if services and services != None:
        for serv in services:
            ns = str(serv.Namespace)
            if serv.XAddr == xaddr and "ptz" in ns:
                return serv.Namespace
    else:
        return None
        
class PTZService:
    def __init__(self,onvif_service = OnvifService()) -> None:
        self.is_ptz_service_supported = False
        self.onvif_service = onvif_service
        self.wsdlUrl = self.onvif_service.wsdl_directory + "/ptz.wsdl"
        self.xAddr = "" 
        self.ptz_name_space = ""
        self.capabilities = {}
        self.profile_token = None
        self.set_ptz_service_variables()

    def set_ptz_service_variables(self) -> None:
        if self.onvif_service.get_con_status() and self.onvif_service.capabilities.PTZ != None:
            self.is_ptz_service_supported = True
            self.xAddr = self.onvif_service.capabilities.PTZ.XAddr
            self.ptz_name_space = get_ptz_namespace(services = self.onvif_service.services,xaddr = self.xAddr)
            self.capabilities = self.GetServiceCapabilities()
            if self.onvif_service.get_first_profile() != None: self.profile_token = self.onvif_service.get_first_profile().token
        else:
            logger.error(f"PTZ service not sported from {self.onvif_service.ip}")
     
    def GetServiceCapabilities(self) -> dict:
        """
        Returns the capabilities of the PTZ service. The result is returned in a typed answer.
        - return [dict];
            - Capabilities [Capabilities]
                The capabilities for the PTZ service is returned in the Capabilities element.
        """
        service_cap = {}
        if self.is_ptz_service_supported:
            logger.info(f"Try to GetServiceCapabilities information..")
            try:
                zeepPTZClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_ptz = zeepPTZClient.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                service_cap = ws_client_ptz.GetServiceCapabilities()
            except Exception as emsg:
                logger.error(f"GetServiceCapabilities unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetServiceCapabilities complete with success..")
        return service_cap

    def GetConfigurations(self) -> list:
        """
        Get all the existing PTZConfigurations from the device.
        The default Position/Translation/Velocity Spaces are introduced to allow NVCs sending move requests without the need to specify a certain coordinate system. 
        The default Speeds are introduced to control the speed of move requests (absolute, relative, preset), where no explicit speed has been set.
        - return [dict];
            - PTZConfiguration - optional, unbounded; [PTZConfiguration]
                A list of all existing PTZConfigurations on the device.
        """
        configs = []
        if self.is_ptz_service_supported:
            logger.info(f"Try to GetConfigurations information..")
            try:
                zeepPTZClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_ptz = zeepPTZClient.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                configs = ws_client_ptz.GetConfigurations()
            except Exception as emsg:
                logger.error(f"GetConfigurations unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetConfigurations complete with success..")
        return configs

    def GetConfiguration(self,ptz_configuration_token : str) -> dict:
        """
        Get a specific PTZconfiguration from the device, identified by its reference token or name.
        The default Position/Translation/Velocity Spaces are introduced to allow NVCs sending move requests without the need to specify a certain coordinate system. 
        The default Speeds are introduced to control the speed of move requests (absolute, relative, preset), where no explicit speed has been set.
        - reqirements; 
            - ptz_configuration_token [ReferenceToken]
                Token of the requested PTZConfiguration.
        - return [dict];
            - PTZConfiguration [PTZConfiguration]
                A requested PTZConfiguration.
        """
        configs = {}
        if self.is_ptz_service_supported:
            logger.info(f"Try to GetConfiguration information..")
            try:
                zeepPTZClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_ptz = zeepPTZClient.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                configs = ws_client_ptz.GetConfiguration(PTZConfigurationToken = ptz_configuration_token)
            except Exception as emsg:
                logger.error(f"GetConfiguration unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetConfiguration complete with success..")
        return configs

    def GetCompatibleConfigurations(self,profile_token : str) -> dict:
        """
        Operation to get all available PTZConfigurations that can be added to the referenced media profile.
        - requirements ;
            - profile_token [str]: 
                Contains the token of an existing media profile the configurations shall be compatible with.
        - return [dict]; 
            - PTZConfiguration - optional, unbounded; [PTZConfiguration]
                A list of all existing PTZConfigurations on the NVT that is suitable to be added to the addressed media profile.
        """
        compatible_configs = {}
        if profile_token == None: profile_token = self.profile_token
        if self.is_ptz_service_supported:
            logger.info(f"Try to GetCompatibleConfigurations information..")
            try:
                zeepPTZClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_ptz = zeepPTZClient.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                compatible_configs = ws_client_ptz.GetCompatibleConfigurations(ProfileToken = profile_token)
            except Exception as emsg:
                logger.error(f"GetCompatibleConfigurations unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetCompatibleConfigurations complete with success..")
        return compatible_configs

    def GetNodes(self) -> list:
        """
        Get the descriptions of the available PTZ Nodes.
        - return [list];
            - PTZNode - optional, unbounded; [PTZNode]
                A list of the existing PTZ Nodes on the device.
        """
        nodes = []
        if self.is_ptz_service_supported:
            logger.info(f"Try to GetNodes information..")
            try:
                zeepPTZClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_ptz = zeepPTZClient.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                nodes = ws_client_ptz.GetNodes()
            except Exception as emsg:
                logger.error(f"GetNodes unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetNodes complete with success..")
        return nodes

    def GetNode(self,node_token : str) -> list:
        """
        Get a specific PTZ Node identified by a reference token or a name.
        - params : 
            - NodeToken : Token of the requested PTZNode.
        - return [dict];
            - PTZNode [PTZNode]
                A requested PTZNode.
        """
        node = {}
        if self.is_ptz_service_supported:
            logger.info(f"Try to GetNode information..")
            try:
                zeepPTZClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_ptz = zeepPTZClient.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                node = ws_client_ptz.GetNode(NodeToken = node_token)
            except Exception as emsg:
                logger.error(f"GetNode unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetNode complete with success..")
        return node

    def AbsoluteMove(self,request_message : PTZRequestMessages.AbsoluteMoveRequestMessage) -> bool:
        """
        Operation to move pan,tilt or zoom to a absolute destination.
        The speed argument is optional. If an x/y speed value is given it is up to the device to either use the x value as absolute resoluting speed vector or to map x and y to the component speed. If the speed argument is omitted, the default speed set by the PTZConfiguration will be used.
        - requirements;
            - request_message : [AbsoluteMoveRequestMessage]
                An Object for AbsoluteMove Request message 
        - return [boolean]; 
            - status : True means OK else False 
        """
        status = False
        if self.onvif_service.get_con_status():
            logger.info(f"Try to AbsoluteMove request..")
            if self.is_ptz_service_supported:
                try:
                    zeep_ptz_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_ptz = zeep_ptz_client.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                    ws_client_ptz.AbsoluteMove(**request_message.to_dict())
                except Exception as emsg:
                    logger.error(f"AbsoluteMove unsuccess.. -> {emsg}")
                else:
                    status = True
                    logger.info(f"Move complete with success..")
            else:
                logger.error(f"PTZ Service not supported..")
        return status

    def ContinuousMove(self,request_message : PTZRequestMessages.ContinuousMoveRequestMessage) -> bool:
        """
        Operation for continuous Pan/Tilt and Zoom movements. The operation is supported if the PTZNode supports at least one continuous Pan/Tilt or Zoom space. If the space argument is omitted, the default space set by the PTZConfiguration will be used.
        - requirements;
            - request_message : [ContinuousMoveRequestMessage]
                An Object for ContinuousMove request message 
        - return [boolean];
            - status : True means OK else False 
        """
        status = False
        if self.onvif_service.get_con_status():
            logger.info(f"Try to ContinuousMove request..")
            if self.is_ptz_service_supported:
                try:
                    zeep_ptz_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_ptz = zeep_ptz_client.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                    ws_client_ptz.ContinuousMove(**request_message.to_dict())
                except Exception as emsg:
                    logger.error(f"ContinuousMove unsuccess.. -> {emsg}")
                else:
                    status = True
                    logger.info(f"ContinuousMove complete with success..")
            else:
                logger.error(f"PTZ Service not supported..")
        return status

    def GetPresets(self,profile_token  = None) -> list:
        """
        Operation to request all PTZ presets for the PTZNode in the selected profile. The operation is supported if there is support for at least on PTZ preset by the PTZNode.
        - params : 
            - ProfileToken : optional
                A reference to the MediaProfile where the operation should take place.
        - return [list];
            - Preset - optional, unbounded; [PTZPreset]
                A list of presets which are available for the requested MediaProfile.
        """
        presets = []
        if profile_token == None: profile_token = self.profile_token
        if self.is_ptz_service_supported:
            logger.info(f"Try to GetPresets information..")
            try:
                zeepPTZClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_ptz = zeepPTZClient.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                presets = ws_client_ptz.GetPresets(ProfileToken = profile_token)
            except Exception as emsg:
                logger.error(f"GetPresets unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetPresets complete with success..")
        return presets 

    def SetPreset(self,profile_token = None,preset_name = None,preset_token = None) -> dict:
        """
        The SetPreset command saves the current device position parameters so that the device can move to the saved preset position through the GotoPreset operation.\
            In order to create a new preset, the SetPresetRequest contains no PresetToken. \
                If creation is successful, the Response contains the PresetToken which uniquely identifies the Preset.
        - requirements;
            - ProfileToken [ReferenceToken]
                A reference to the MediaProfile where the operation should take place.
            - PresetName - optional; [string]
                A requested preset name.
            - PresetToken - optional; [ReferenceToken]
                A requested preset token.
        - return ;
            - PresetToken : [str]
                A token to the Preset which has been set.
        """
        preset_token = None
        request_params = {}
        if profile_token == None: profile_token = self.profile_token
        request_params["ProfileToken"] = profile_token
        if preset_name != None:
            request_params["PresetName"] = preset_name
        if preset_name != None:
            request_params["PresetToken"] = preset_token
        if self.is_ptz_service_supported:
            logger.info(f"Try to SetPreset information..")
            try:
                zeepPTZClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_ptz = zeepPTZClient.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                preset_token = ws_client_ptz.SetPreset(**request_params)
            except Exception as emsg:
                logger.error(f"SetPreset unsuccess.. -> {emsg}")
            else:
                logger.info(f"SetPreset complete with success..")
        return preset_token

    def RemovePreset(self,preset_token : str,profile_token = None) -> bool:
        """
        Operation to remove a PTZ preset for the Node in the selected profile. The operation is supported if the PresetPosition capability exists for teh Node in the selected profile.
        - requirements;
            - ProfileToken [ReferenceToken]
                A reference to the MediaProfile where the operation should take place.
            - PresetToken  [ReferenceToken]
                A requested preset token.
        - return [boolean]; 
            - status : True means OK else NotOK 
        """
        status = False
        if profile_token == None: profile_token = self.profile_token
        if self.onvif_service.get_con_status():
            logger.info(f"Try to RemovePreset request..")
            if self.is_ptz_service_supported:
                try:
                    zeep_ptz_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_ptz = zeep_ptz_client.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                    ws_client_ptz.RemovePreset(ProfileToken = profile_token,PresetToken = preset_token)
                except Exception as emsg:
                    logger.error(f"RemovePreset unsuccess.. -> {emsg}")
                else:
                    status = True
                    logger.info(f"RemovePreset complete with success..")
            else:
                logger.error(f"PTZ Service not supported..")
        return status

    def GotoPreset(self,preset_token : str,speed = None,profile_token = None) -> bool:
        """
        Operation to go to a saved preset position for the PTZNode in the selected profile. The operation is supported if there is support for at least on PTZ preset by the PTZNode.
        - requirements;
            - profile_token [ReferenceToken]
                A reference to the MediaProfile where the operation should take place.
            - preset_token [ReferenceToken]
                A requested preset token.
            - speed - optional; [PTZSpeed] [dict]
                A requested speed.The speed parameter can only be specified when Speed Spaces are available for the PTZ Node.
        - return [boolean]; 
            - status : True means OK else False 
        """
        status = False
        request_params = {}
        if profile_token == None: profile_token = self.profile_token
        request_params["ProfileToken"] = profile_token
        request_params["PresetToken"] = preset_token
        if speed != None: request_params["Speed"] = speed
        if self.onvif_service.get_con_status():
            logger.info(f"Try to GotoPreset request..")
            if self.is_ptz_service_supported:
                try:
                    zeep_ptz_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_ptz = zeep_ptz_client.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                    ws_client_ptz.GotoPreset(**request_params)
                except Exception as emsg:
                    logger.error(f"GotoPreset unsuccess.. -> {emsg}")
                else:
                    status = True
                    logger.info(f"GotoPreset complete with success..")
            else:
                logger.error(f"PTZ Service not supported..")
        return status

    def SetHomePosition(self,profile_token = None) -> bool:
        """
        Operation to save current position as the home position. The SetHomePosition command returns with a failure if the “home” position is fixed and cannot be overwritten. If the SetHomePosition is successful, it is possible to recall the Home Position with the GotoHomePosition command.
        - requirements;
            - ProfileToken [ReferenceToken]
                A reference to the MediaProfile where the operation should take place.
        - return [boolean]; 
            - status : True means OK else False 
        """
        status = False
        if profile_token == None: profile_token = self.profile_token
        if self.onvif_service.get_con_status():
            logger.info(f"Try to SetHomePosition request..")
            if self.is_ptz_service_supported:
                try:
                    zeep_ptz_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_ptz = zeep_ptz_client.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                    ws_client_ptz.SetHomePosition(ProfileToken = profile_token)
                except Exception as emsg:
                    logger.error(f"SetHomePosition unsuccess.. -> {emsg}")
                else:
                    status = True
                    logger.info(f"SetHomePosition complete with success..")
            else:
                logger.error(f"PTZ Service not supported..")
        return status

    def GotoHomePosition(self,speed = None,profile_token = None) -> bool:
        """
        Operation to move the PTZ device to it's "home" position. The operation is supported if the HomeSupported element in the PTZNode is true.
        - requirements;
            - ProfileToken [ReferenceToken]
                A reference to the MediaProfile where the operation should take place.
            - Speed - optional; [PTZSpeed] [dict]
                    A requested speed.The speed parameter can only be specified when Speed Spaces are available for the PTZ Node.
                - PanTilt - optional; [Vector2D]
                    Pan and tilt speed. The x component corresponds to pan and the y component to tilt. If omitted in a request, the current (if any) PanTilt movement should not be affected.
                - Zoom - optional; [Vector1D]
                    A zoom speed. If omitted in a request, the current (if any) Zoom movement should not be affected.
        - return [boolean]; 
            status : True means OK else False 
        """
        status = False
        request_params = {}
        if profile_token == None: profile_token = self.profile_token
        request_params["ProfileToken"] = profile_token
        if speed != None: request_params["Speed"] = speed
        if self.onvif_service.get_con_status():
            logger.info(f"Try to GotoHomePosition request..")
            if self.is_ptz_service_supported:
                try:
                    zeep_ptz_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_ptz = zeep_ptz_client.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                    ws_client_ptz.GotoHomePosition(**request_params)
                except Exception as emsg:
                    logger.error(f"GotoHomePosition unsuccess.. -> {emsg}")
                else:
                    status = True
                    logger.info(f"GotoHomePosition complete with success..")
            else:
                logger.error(f"PTZ Service not supported..")
        return status

    def GetPresetTours(self,profile_token  = None) -> list:
        """
        Operation to request PTZ preset tours in the selected media profiles.
        - params : 
            - profile_token : optional
                A reference to the MediaProfile where the operation should take place.
        - return [dict];
            - PresetTour - optional, unbounded; [PresetTour] 
                List of PresetTour
        """
        preset_tours = []
        if profile_token == None: profile_token = self.profile_token
        if self.is_ptz_service_supported:
            logger.info(f"Try to GetPresetTours information..")
            try:
                zeepPTZClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_ptz = zeepPTZClient.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                preset_tours = ws_client_ptz.GetPresetTours(ProfileToken = profile_token)
            except Exception as emsg:
                logger.error(f"GetPresetTours unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetPresetTours complete with success..")
        return preset_tours
    
    def GetPresetTour(self,preset_tour_token : str,profile_token = None) -> dict:
        """
        Operation to request a specific PTZ preset tour in the selected media profile.
        - requirement : 
            - profile_token : [str]
                A reference to the MediaProfile where the operation should take place.
            - preset_tour_token : [str]
        - return [dict];
            - PresetTour [PresetTour]
        """
        preset_tour = {}
        if profile_token == None: profile_token = self.profile_token
        if self.is_ptz_service_supported:
            logger.info(f"Try to GetPresetTour information..")
            try:
                zeepPTZClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_ptz = zeepPTZClient.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                preset_tour = ws_client_ptz.GetPresetTour(ProfileToken = profile_token,PresetTourToken = preset_tour_token)
            except Exception as emsg:
                logger.error(f"GetPresetTour unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetPresetTour complete with success..")
        return preset_tour
    
    def GetPresetTourOptions(self,preset_tour_token : str,profile_token = None) -> list:
        """
        Operation to request available options to configure PTZ preset tour.
        - requirement : 
            - profile_token : [str]
                A reference to the MediaProfile where the operation should take place.
            - preset_tour_token : [str]
        - return [dict];
            - Options [PTZPresetTourOptions]
        """
        preset_tour_options = {}
        if profile_token == None: profile_token = self.profile_token
        if self.is_ptz_service_supported:
            logger.info(f"Try to GetPresetTourOptions information..")
            try:
                zeepPTZClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_ptz = zeepPTZClient.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                preset_tour_options = ws_client_ptz.GetPresetTourOptions(ProfileToken = profile_token,PresetTourToken = preset_tour_token)
            except Exception as emsg:
                logger.error(f"GetPresetTourOptions unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetPresetTourOptions complete with success..")
        return preset_tour_options

    def CreatePresetTour(self,profile_token = None) -> dict:
        """
        Operation to create a preset tour for the selected media profile.
        - requirements;
            - ProfileToken [ReferenceToken]
                A reference to the MediaProfile.
        - return [dict];
            - PresetTourToken
                A token to the Preset Tour which has been set.
        """
        preset_tour_token = None
        if profile_token == None: profile_token = self.profile_token
        if self.is_ptz_service_supported:
            logger.info(f"Try to CreatePresetTour information..")
            try:
                zeepPTZClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_ptz = zeepPTZClient.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                preset_tour_token = ws_client_ptz.CreatePresetTour(ProfileToken = profile_token)
            except Exception as emsg:
                logger.error(f"CreatePresetTour unsuccess.. -> {emsg}")
            else:
                logger.info(f"CreatePresetTour complete with success..")
        return preset_tour_token

    def ModifyPresetTour(self,request_message : PTZRequestMessages.ModifyPresetTourRequestMessage) -> bool:
        """
        Operation to modify a preset tour for the selected media profile.
        - requirements;
            - request_params : [ModifyPresetTourRequestParams] 
        - return [boolean]; 
            - status : True means OK else False 
        """
        status = False
        if self.onvif_service.get_con_status():
            logger.info(f"Try to ModifyPresetTour request..")
            if self.is_ptz_service_supported:
                try:
                    zeep_ptz_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_ptz = zeep_ptz_client.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                    ws_client_ptz.ModifyPresetTour(**request_message.to_dict())
                except Exception as emsg:
                    logger.error(f"ModifyPresetTour unsuccess.. -> {emsg}")
                else:
                    status = True
                    logger.info(f"ModifyPresetTour complete with success..")
            else:
                logger.error(f"PTZ Service not supported..")
        return status

    def RemovePresetTour(self,preset_tour_token : str,profile_token = None) -> bool:
        """
        Operation to remove a PTZ preset for the Node in the selected profile. The operation is supported if the PresetPosition capability exists for teh Node in the selected profile.
        - requirements;
            - ProfileToken [ReferenceToken]
                A reference to the MediaProfile where the operation should take place.
            - PresetTourToken  [ReferenceToken]
                A requested PresetTourToken token.
        - return [boolean]; 
            - status : True means OK else NotOK 
        """
        status = False
        if profile_token == None: profile_token = self.profile_token
        if self.onvif_service.get_con_status():
            logger.info(f"Try to RemovePresetTour request..")
            if self.is_ptz_service_supported:
                try:
                    zeep_ptz_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_ptz = zeep_ptz_client.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                    ws_client_ptz.RemovePresetTour(ProfileToken = profile_token,PresetTourToken = preset_tour_token)
                except Exception as emsg:
                    logger.error(f"RemovePresetTour unsuccess.. -> {emsg}")
                else:
                    status = True
                    logger.info(f"RemovePresetTour complete with success..")
            else:
                logger.error(f"PTZ Service not supported..")
        return status

    def OperatePresetTour(self,preset_tour_token : str,operation : PTZEnumParams.PTZPresetTourOperation,profile_token = None) -> bool:
        """
        Operation to perform specific operation on the preset tour in selected media profile.
        - requirements;
            - ProfileToken [ReferenceToken]
                A reference to the MediaProfile where the operation should take place.
            - PresetTourToken [ReferenceToken]
                A requested preset token.
            - Operation [PTZPresetTourOperation]- enum { 'Start', 'Stop', 'Pause', 'Extended' 
        - return [boolean]; 
            - status : True means OK else False 
        """
        status = False
        if profile_token == None: profile_token = self.profile_token
        if self.onvif_service.get_con_status():
            logger.info(f"Try to OperatePresetTour request..")
            if self.is_ptz_service_supported:
                try:
                    zeep_ptz_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_ptz = zeep_ptz_client.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                    ws_client_ptz.OperatePresetTour(ProfileToken = profile_token,PresetTourToken = preset_tour_token,Opetation = operation)
                except Exception as emsg:
                    logger.error(f"OperatePresetTour unsuccess.. -> {emsg}")
                else:
                    status = True
                    logger.info(f"OperatePresetTour complete with success..")
            else:
                logger.error(f"PTZ Service not supported..")
        return status

    def Stop(self,profile_token = None,pantilt = False,zoom = False) -> bool:
        """
        Operation to stop ongoing pan, tilt and zoom movements of absolute relative and continuous type.\
             If no stop argument for pan, tilt or zoom is set, the device will stop all ongoing pan, tilt and zoom movements.
        - requirements;
            - ProfileToken [ReferenceToken]
                A reference to the MediaProfile that indicate what should be stopped.
            - PanTilt - optional; [boolean]
                Set true when we want to stop ongoing pan and tilt movements.If PanTilt arguments are not present, this command stops these movements.
            - Zoom - optional; [boolean]
                Set true when we want to stop ongoing zoom movement.If Zoom arguments are not present, this command stops ongoing zoom movement.
        - return [boolean]; 
            - status : True means OK else NotOK 
        """
        status = False
        if profile_token == None: profile_token = self.profile_token
        if self.onvif_service.get_con_status():
            logger.info(f"Try to Stop request..")
            if self.is_ptz_service_supported:
                try:
                    zeep_ptz_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_ptz = zeep_ptz_client.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                    ws_client_ptz.Stop(ProfileToken = profile_token,PanTilt = pantilt,Zoom = zoom)
                except Exception as emsg:
                    logger.error(f"Stop unsuccess.. -> {emsg}")
                else:
                    status = True
                    logger.info(f"Stop complete with success..")
            else:
                logger.error(f"PTZ Service not supported..")
        return status

    def SendAuxiliaryCommand(self,auxilary_data : str,profile_token = None) -> dict:
        """
        Operation to send auxiliary commands to the PTZ device mapped by the PTZNode in the selected profile. The operation is supported if the AuxiliarySupported element of the PTZNode is true
        - requirements;
            - ProfileToken [ReferenceToken]
                A reference to the MediaProfile where the operation should take place.
            - AuxiliaryData [AuxiliaryData]
                The Auxiliary request data.
        - return [dict]; 
            - AuxiliaryResponse [AuxiliaryData]
                The response contains the auxiliary response.
        """
        auxiliary_response = {}
        if profile_token == None: profile_token = self.profile_token
        if self.onvif_service.get_con_status():
            logger.info(f"Try to SendAuxiliaryCommand request..")
            try:
                zeep_ptz_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_ptz = zeep_ptz_client.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                auxiliary_response = ws_client_ptz.SendAuxiliaryCommand(ProfileToken = profile_token,AuxiliaryData = auxilary_data)
            except Exception as emsg:
                logger.error(f"SendAuxiliaryCommand unsuccess.. -> {emsg}")
            else:
                logger.info(f"SendAuxiliaryCommand complete with success..")
        return auxiliary_response

    def RelativeMove(self,request_message : PTZRequestMessages.RelativeMoveRequestMessage) -> bool:
        """
        Operation for Relative Pan/Tilt and Zoom Move. The operation is supported if the PTZNode supports at least one relative Pan/Tilt or Zoom space.
        - requirements;
            - request_message : [RelativeMoveRequestMessage]
                An Object for RelativeMove request message 
        - return; status : [boolean] True means OK else NotOK 
        """
        status = False
        if self.onvif_service.get_con_status():
            logger.info(f"Try to RelativeMove request..")
            if self.is_ptz_service_supported:
                try:
                    zeep_ptz_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_ptz = zeep_ptz_client.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                    ws_client_ptz.RelativeMove(**request_message.to_dict())
                except Exception as emsg:
                    logger.error(f"RelativeMove unsuccess.. -> {emsg}")
                else:
                    status = True
                    logger.info(f"RelativeMove complete with success..")
            else:
                logger.error(f"PTZ Service not supported..")
        return status

    def GetStatus(self,profile_token = None) -> dict:
        """
        Operation to request PTZ status for the Node in the selected profile.
        - requirements;
            - ProfileToken [ReferenceToken]:
                A reference to the MediaProfile where the PTZStatus should be requested.
        - return [dict];
            - PTZStatus [PTZStatus]
                The PTZStatus for the requested MediaProfile.
        """
        status = {}
        if profile_token == None: profile_token = self.profile_token
        if self.is_ptz_service_supported:
            logger.info(f"Try to GetStatus information..")
            try:
                zeepPTZClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_ptz = zeepPTZClient.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                status = ws_client_ptz.GetStatus(ProfileToken = profile_token)
            except Exception as emsg:
                logger.error(f"GetStatus unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetStatus complete with success..")
        return status

    def GeoMove(self,request_message : PTZRequestMessages.GeoMoveRequestMessage) -> bool:
        """
        Operation for Relative Pan/Tilt and Zoom Move. The operation is supported if the PTZNode supports at least one relative Pan/Tilt or Zoom space.
        - requirements;
            - request_message : [GeoMoveRequestMessage]
                An Object for GeoMove request message 
        - return [boolean]; 
            - status : True means OK else NotOK 
        """
        status = False
        if self.onvif_service.get_con_status():
            logger.info(f"Try to GeoMove request..")
            if self.is_ptz_service_supported:
                try:
                    zeep_ptz_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_ptz = zeep_ptz_client.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                    ws_client_ptz.GeoMove(**request_message.to_dict())
                except Exception as emsg:
                    logger.error(f"GeoMove unsuccess.. -> {emsg}")
                else:
                    status = True
                    logger.info(f"GeoMove complete with success..")
            else:
                logger.error(f"PTZ Service not supported..")
        return status
    
    def MoveAndStartTracking(self,request_message : PTZRequestMessages.MoveAndStartTrackingRequestMessage) -> bool:
        """
        Operation to send an an atomic command to the device: move the camera to a wanted position and then delegate the PTZ control to the tracking algorithm. 
        - requirements;
            - request_message : [MoveAndStartTrackingRequestMessage]
                An Object for MoveAndStartTracking request message 
        - return [boolean]; 
            - status : True means OK else NotOK 
        """
        status = False
        if self.onvif_service.get_con_status():
            logger.info(f"Try to MoveAndStartTracking request..")
            if self.is_ptz_service_supported:
                try:
                    zeep_ptz_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_ptz = zeep_ptz_client.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                    ws_client_ptz.MoveAndStartTracking(**request_message.to_dict())
                except Exception as emsg:
                    logger.error(f"MoveAndStartTracking unsuccess.. -> {emsg}")
                else:
                    status = True
                    logger.info(f"MoveAndStartTracking complete with success..")
            else:
                logger.error(f"PTZ Service not supported..")
        return status
    
    def SetConfiguration(self,request_message : PTZRequestMessages.SetConfigurationRequestMessage) -> bool:
        """
        Set/update a existing PTZConfiguration on the device. 
        - requirements;
            - request_message : [SetConfigurationRequestMessage]
                An Object for SetConfiguration request message 
        - return [boolean]; 
            - status : True means OK else NotOK 
        """
        status = False
        if self.onvif_service.get_con_status():
            logger.info(f"Try to SetConfiguration request..")
            if self.is_ptz_service_supported:
                try:
                    zeep_ptz_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_ptz = zeep_ptz_client.create_service("{" + self.ptz_name_space + "}PTZBinding", self.xAddr)
                    ws_client_ptz.SetConfiguration(**request_message.to_dict())
                except Exception as emsg:
                    logger.error(f"SetConfiguration unsuccess.. -> {emsg}")
                else:
                    status = True
                    logger.info(f"SetConfiguration complete with success..")
            else:
                logger.error(f"PTZ Service not supported..")
        return status
