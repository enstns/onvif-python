"""
Created to test Onvif PTZ service properties.

craeted by : enstns
created time : 23.05.23
"""
import time
import path
import sys
# directory reach
directory = path.Path(__file__).abspath()
 
# setting path
parent_directory = directory.parent.parent
sys.path.append(parent_directory)

from lib.onvif import OnvifService
from lib.requests_messages.ptz_request_messages import PTZRequestMessages
from lib.params.ptz_request_params import PTZRequestParams
from lib.services.ptz_service import PTZService


onvif_device = OnvifService()

# device information
onvif_device.ip = "11.63.1.6"
onvif_device.username = "admin"
onvif_device.password = "12345"
onvif_device.port = "80"
onvif_device.wsdl_directory = parent_directory + "/wsdl"

# onvif device connection
onvif_device.connect_onvif()

print("Start to Test PTZ service...")
ptz_serv = PTZService(onvif_service=onvif_device)
if ptz_serv.is_ptz_service_supported:
    print(f'PTZ Service Capabilities: \n{onvif_device.capabilities.PTZ}')

    ptz_caps = ptz_serv.GetServiceCapabilities()
    print(f'GetServiceCapabilities response : \n{ptz_caps}')
    profile = ptz_serv.onvif_service.get_first_profile()
    print(f'First Profile : \n{profile}')
    print(f'First Profile Token : {profile.token}')

    ptz_configs = ptz_serv.GetConfigurations()
    # print(f'GetConfigurations response : \n{ptz_configs}')
    first_config_token = ptz_configs[0].token
    
    ptz_config_properties = ptz_serv.GetConfiguration(ptz_configuration_token=first_config_token)
    # print(f'GetConfiguration for {first_config_token} response is ;\n{ptz_config_properties}')

    ptz_nodes = ptz_serv.GetNodes()
    # print(f'GetNodes response : \n{ptz_nodes}')
    first_node_token = ptz_nodes[0].token

    node_properties = ptz_serv.GetNode(node_token=first_node_token)
    print(f'GetNode response for {first_node_token} : \n{node_properties}')

    presets = ptz_serv.GetPresets(profile_token=ptz_serv.profile_token)
    # print(f'GetPresets response : \n{presets}')

    ptz_serv.AbsoluteMove(PTZRequestMessages.AbsoluteMoveRequestMessage(profile_token=profile.token,position=PTZRequestParams.PTZVector(pantilt=PTZRequestParams.Vector2D(nspace_url="http://www.onvif.org/ver10/tptz/PanTiltSpaces/PositionGenericSpace",x = 0.3,y= 0.3))))
    # ptz_serv.ContinuousMove(PTZRequestMessages.ContinuousMoveRequestMessage(profile_token=profile.token,velocity=PTZSpeed(zoom=Vector1D(nspace_url="http://www.onvif.org/ver10/tptz/ZoomSpaces/VelocityGenericSpace",x=0.5))))
    ptz_serv.ContinuousMove(PTZRequestMessages.ContinuousMoveRequestMessage(profile_token=profile.token,velocity=PTZRequestParams.PTZSpeed(pantilt=PTZRequestParams.Vector2D(nspace_url="http://www.onvif.org/ver10/tptz/PanTiltSpaces/VelocityGenericSpace",x=0.5,y=-0.5))))
    time.sleep(3)
    ptz_serv.Stop(profile_token=profile.token,pantilt=True,zoom=True)      
else:
    print("PTZ service not supported!")
