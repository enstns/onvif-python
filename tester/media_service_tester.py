"""
Created to test Onvif Media service properties.

craeted by : enstns
created time : 23.05.23
"""
import path 
import sys
import cv2
 
# directory reach
directory = path.Path(__file__).abspath()
 
# setting path
parent_directory = directory.parent.parent
sys.path.append(parent_directory)

from lib.requests_messages.media_request_messages import MediaRequestMessages
from lib.params.media_request_params import MediaEnumParams, MediaRequestParams
from lib.services.media_service import MediaService
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
if onvif_device.get_con_status():
    print(f'Media Service Capabilities: \n{onvif_device.capabilities.Media}')
    media_serv = MediaService(onvif_service=onvif_device)
    if media_serv.is_media_service_supported:
        print(f'Media Service NameSpace: {media_serv.media_name_space}\nMedia Service XADDR: {media_serv.xAddr}')
        video_sources = media_serv.GetVideoSources()
        print(f'GetVideoSources response : \n{video_sources}')
        profiles = media_serv.GetProfiles()
        print(f'GetProfiles response number is : {len(profiles)}')
        media_cap = media_serv.GetServiceCapabilities()
        print(f'GetServiceCapabilities response : \n{media_cap}')

        media_videosource_configs = media_serv.GetVideoSourceConfigurations()
        print(f'GetVideoSourceConfigurations response : \n{media_videosource_configs}')
        if media_videosource_configs:
            first_video_source_token = media_videosource_configs[0].token
            print(f'First Video Source Config Token : {first_video_source_token}')
        
        if media_serv.media_capabilities.OSD:
            
            osds = media_serv.GetOSDOptions(configuration_token=first_video_source_token) # not working ,need token
            print(f'GetOSDOptions response : \n{media_cap}')

            osds = media_serv.GetOSDs() # not working need token
            print(f'Before DeleteOSD GetOSDs response : \n{osds}')

            for osd in osds:
                media_serv.DeleteOSD(osd_token=osd.token)
            
            position_configs = MediaRequestParams.OSDPosConfiguration(osd_pos_type=MediaEnumParams.OSDPositionType.LowerRight)
            text_configs = MediaRequestParams.OSDTextConfiguration(osd_text_type=MediaEnumParams.OSDTextStringType.DateAndTime,date_format="MM/dd/yyyy",time_format="hh:mm:ss tt",font_color="Black",background_color="White")
            createdOSD_configs = MediaRequestParams.OSDConfiguration(token="TestOSD",videosource_configuration_token=first_video_source_token,osd_type=MediaEnumParams.OSDType.Text,position=position_configs,text_string=text_configs)
            createOSD_request_message = MediaRequestMessages.CreateOSDMessage(osd = createdOSD_configs)
            print(f'Created OSD message : \n{createOSD_request_message.to_dict()}')
            createdOSD_token = media_serv.CreateOSD(request_message=createOSD_request_message)
            osds = media_serv.GetOSDs()
            print(f'After CreateOSD GetOSDs response : \n{osds}')
        
        profile = onvif_device.get_first_profile()
        profile_token = profile.token
        
        transport_obj = MediaRequestParams.Transport(protocol=MediaEnumParams.TransportProtocol.RTSP)
        stream_setup_obj =  MediaRequestParams.StreamSetup(stream=MediaEnumParams.StreamType.Unicast,transport=transport_obj)
        getting_streamuri_request = MediaRequestMessages.GetStreamUriMessage(stream_setup=stream_setup_obj,profile_token=profile_token)
        print(f"Created GETStreamURI Message : {getting_streamuri_request.to_dict()}")
        media_streamuri_dict = media_serv.GetStreamUri(getting_streamuri_request)
        print(f'GetStreamUri response : \n{media_streamuri_dict}')
        
        snapshot_uri = media_serv.GetSnapshotUri(profile_token=profile.token)
        print(f'Profile Token : {profile.token}\tSnapshotUri : {snapshot_uri}')   
        download_picture_status = media_serv.DownloadSnapshot(snapshot_uri,path=parent_directory+ "/download")

        # to play camera rtsp stream
        if media_streamuri_dict:
            rtsp_uri = "rtsp://" + onvif_device.username + ":" + onvif_device.password + "@" + media_streamuri_dict.Uri.split("//")[1]
            print(f"Created rtsp URI : {rtsp_uri}")
            try:
                cap = cv2.VideoCapture(rtsp_uri)
            except Exception as msg:
                print(msg)
            else:
                while(cap.isOpened()):
                    ret, frame = cap.read()
                    frame = cv2.resize(frame, (980, 540))
                    cv2.imshow('frame', frame)
                    if cv2.waitKey(20) & 0xFF == ord('q'):
                        break
                cap.release()
                cv2.destroyAllWindows()
