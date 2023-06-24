"""
Created to test Onvif Image service properties.

craeted by : enstns
created time : 23.05.23
"""
import path 
import sys
import time
import random
 
# directory reach
directory = path.Path(__file__).abspath()
 
# setting path
parent_directory = directory.parent.parent
sys.path.append(parent_directory)

from lib.requests_messages.image_request_messages import ImageRequestMessages
from lib.params.image_request_params import ImageRequestParams, ImagesEnumParams
from lib.services.image_service import ImageService
from lib.onvif import OnvifService

onvif_device = OnvifService()

# device information
onvif_device.ip = "11.63.1.6"
onvif_device.username = "admin"
onvif_device.password = "12345"
onvif_device.port = "80"
onvif_device.wsdl_directory = parent_directory + "/wsdl"

# onvif device connection
onvif_device.connect_onvif()

print(f'Image Service Capabilities: \n{onvif_device.capabilities.Imaging}')
image_serv = ImageService(onvif_service=onvif_device)
if image_serv.is_imaging_service_supported:
    print(f'image service wsdl URL : {image_serv.wsdlUrl}\nimage service video source token : {image_serv.video_source_token}\nimage service xAddr : {image_serv.xAddr}\nimage service nameSpace : {image_serv.image_name_space}')
    image_service_cap = image_serv.GetServiceCapabilities()
    print(f'GetServiceCapabilities response : \n{image_service_cap}')
    if image_service_cap.Presets:
        current_preset_info = image_serv.GetCurrentPreset() 
        print(f'GetCurrentPreset response : \n{current_preset_info}')
    else:
        print(f'Preset not Supported!')
    move_options = image_serv.GetMoveOptions()
    print(f'GetMoveOptions response : \n{move_options}')
    move_request_message = ImageRequestMessages.MoveMessage(vs_token=image_serv.video_source_token,focus=ImageRequestParams.FocusMove(continuous=ImageRequestParams.ContinuousFocus(speed=3)))
    print(f'Created Move request message : \n{move_request_message.to_dict()}')
    image_serv.Move(request_message=move_request_message)
    time.sleep(1)
    image_serv.Stop(vs_token=image_serv.video_source_token)
    image_settings_info = image_serv.GetImagingSettings() 
    print(f'GetImagingSettings response for Focus: \n{image_settings_info.Focus}')
    print(f'GetImagingSettings response for Brightness: \n{image_settings_info.Brightness}')
    focus_config = ImageRequestParams.FocusConfiguration20(auto_focus_mode=ImagesEnumParams.AutoFocusMode.MANUAL)
    image_settings_message = ImageRequestMessages.SetImagingSettingsMessage(imaging_settings= ImageRequestParams.ImagingSettings20(focus=focus_config),vs_token=image_serv.video_source_token)
    print(f"Created Image Settings message : {image_settings_message.to_dict()}")

    image_serv.SetImagingSettings(request_message=image_settings_message)
    image_settings_info = image_serv.GetImagingSettings() 
    print(f'GetImagingSettings response for Focus: \n{image_settings_info.Focus}')

    options = image_serv.GetOptions(vs_token=image_serv.video_source_token)
    print(f'GetOptions response : \n{options}')
    brightness_min = options.Brightness.Min
    brightness_max = options.Brightness.Max

    random_brightness = random.randint(brightness_min,brightness_max)
    
    image_settings_20 = ImageRequestParams.ImagingSettings20(brightness=random_brightness)
    image_settings_message = ImageRequestMessages.SetImagingSettingsMessage(imaging_settings=image_settings_20,vs_token=image_serv.video_source_token)
    print(f"Created Image Settings message : {image_settings_message.to_dict()}")
    image_serv.SetImagingSettings(image_settings_message)

    image_settings_info = image_serv.GetImagingSettings() 
    print(f'GetImagingSettings response for Brightness: \n{image_settings_info.Brightness}')



