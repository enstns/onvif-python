import datetime
import signal
import cv2

from lib.params.analytics_request_params import AnalyticsEnumParams,AnalyticsRequestParams
from lib.params.device_request_params import DeviceEnumParams, DeviceRequestParams
from lib.params.media_request_params import MediaEnumParams, MediaRequestParams
from lib.params.ptz_request_params import PTZEnumParams, PTZRequestParams
from lib.params.image_request_params import ImagesEnumParams,ImageRequestParams
from lib.params.event_request_params import EventEnumParams, EventRequestParams

from lib.requests_messages.analytics_request_messages import AnalyticsRequestMessages
from lib.requests_messages.media_request_messages import MediaRequestMessages
from lib.requests_messages.ptz_request_messages import PTZRequestMessages
from lib.requests_messages.image_request_messages import ImageRequestMessages
from lib.requests_messages.device_request_messages import DeviceRequestMessages
from lib.requests_messages.event_request_messages import EventRequestMessages

from lib.services.device_service import DeviceService
from lib.services.event_service import EventService
from lib.services.media_service import MediaService
from lib.services.ptz_service import PTZService
from lib.services.image_service import ImageService
from lib.services.analytics_service import AnalyticsService
from lib.onvif import OnvifService
import time

onvif_device = OnvifService()

# globals 
# True -> Able to test / False -> Disable to test
TEST_DEVICE_SERVICE = False
TEST_PTZ_SERVICE = False
TEST_IMAGE_SERVICE = False
TEST_MEDIA_SERVICE = False
TEST_EVENT_SERVICE = False
TEST_ANALYTICS_SERVICE = True

STOP = False

# to Configure Onvif Device
onvif_device.ip = "11.63.1.6"
onvif_device.username = "admin"
onvif_device.password = "12345"
onvif_device.port = "80"

onvif_device.wsdl_directory = "wsdl"
onvif_device.connect_onvif()

# TODO: control keyboard interrupt
def signal_sigint_handler(signal, frame):
    global STOP
    STOP = True
    print("SIGINT received closing program!")

signal.signal(signal.SIGINT, signal_sigint_handler)

if onvif_device.get_con_status():
    if TEST_DEVICE_SERVICE:
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

    if TEST_IMAGE_SERVICE:
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
            focus_config = ImageRequestParams.FocusConfiguration20(auto_focus_mode=ImagesEnumParams.AutoFocusMode.MANUAL)
            image_settings_message = ImageRequestMessages.SetImagingSettingsMessage(imaging_settings= ImageRequestParams.ImagingSettings20(focus=focus_config),vs_token=image_serv.video_source_token)
            print(image_settings_message.to_dict())
            image_serv.SetImagingSettings(request_message=image_settings_message)
            image_settings_info = image_serv.GetImagingSettings() 
            print(f'GetImagingSettings response for Focus: \n{image_settings_info.Focus}')

    if TEST_MEDIA_SERVICE:
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
            download_picture_status = media_serv.DownloadSnapshot(snapshot_uri)

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

    if TEST_PTZ_SERVICE:
        print("Start to Test PTZ service...")
        ptz_serv = PTZService(onvif_service=onvif_device)
        if ptz_serv.is_ptz_service_supported:
            ptz_caps = ptz_serv.GetServiceCapabilities()
            # print(f'GetServiceCapabilities response : \n{ptz_caps}')
            profile = ptz_serv.onvif_service.get_first_profile()
            # print(f'First Profile : \n{profile}')
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
            # time.sleep(3)
            ptz_serv.Stop(profile_token=profile.token,pantilt=True,zoom=True)      
        else:
            print("PTZ service not supported!")

    if TEST_EVENT_SERVICE:
        print("Start to Test Event service...")
        event_serv = EventService(onvif_service=onvif_device)
        if event_serv.is_event_service_supported:
            print('Event service is supported...')
            print(f'Event Service XAddr is : {event_serv.xAddr}')
            print(f'Event Service NameSpace is : {event_serv.event_name_space}')

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

    if TEST_ANALYTICS_SERVICE:
        print("Start to Test Analytics Service...")
        analytics_serv = AnalyticsService(onvif_service=onvif_device)
        if analytics_serv.is_analytics_service_supported:
            print("Analytics service is supported...")
            print(f'GetServiceCapabilities response :\n{analytics_serv.capabilities}')

            # create media service 
            media_serv = MediaService(onvif_service=onvif_device)
            profile_token = onvif_device.get_first_profile().token
            configurations = media_serv.GetCompatibleVideoAnalyticsConfigurations(profile_token=profile_token)
            print(f'GetCompatibleVideoAnalyticsConfigurations response :\n{configurations}')
            first_configs = configurations[0]
            video_analytics_configuration_token = first_configs.token

            supported_analytics_modules = analytics_serv.GetSupportedAnalyticsModules(configuration_token=video_analytics_configuration_token)
            print(f'GetSupportedAnalyticsModules response :\n{supported_analytics_modules}')

            supported_rules = analytics_serv.GetSupportedRules(configuration_token=video_analytics_configuration_token)
            print(f'GetSupportedRules response :\n{supported_rules}')
            
            rules = analytics_serv.GetRules(configuration_token=video_analytics_configuration_token)
            print(f'Before Create Rule method GetRules response :\n{rules}')
        
            created_rule_simple_item = AnalyticsRequestParams.SimpleItem(name="MinCount",value="30").to_dict()
            my_item_list = AnalyticsRequestParams.ItemList(simple_item=created_rule_simple_item)
            created_rule_config = AnalyticsRequestParams.Config(name="TestMotionDetector",type_name="tt:CellMotionDetector",parameters=my_item_list)
            created_rule_req_mesg = AnalyticsRequestMessages.CreateRulesMessage(configuration_token=video_analytics_configuration_token,rule=created_rule_config)
            print(f'Created CreateRulesMessage Request message is : \n{created_rule_req_mesg.to_dict()}')
            
            create_rule_status = analytics_serv.CreateRules(request_message=created_rule_req_mesg)
            rules = analytics_serv.GetRules(configuration_token=video_analytics_configuration_token)
            print(f'After Create Rule method GetRules response :\n{rules}')
        
            analytics_serv.DeleteRules(configuration_token=video_analytics_configuration_token,rule_name="TestMotionDetector")
            rules = analytics_serv.GetRules(configuration_token=video_analytics_configuration_token)
            print(f'After Delete Rule TestMotionDetector, GetRules response :\n{rules}')
            
            first_rule = rules[0]
            modified_items = first_rule.Parameters.SimpleItem
            element_items = first_rule.Parameters.ElementItem
            for simple_item in modified_items:
                if simple_item.Name == "MinCount":
                    simple_item.Value = 30
                else: pass
            my_item_list = AnalyticsRequestParams.ItemList(simple_item=modified_items,element_item=element_items)
            modified_rule_config = AnalyticsRequestParams.Config(name=first_rule.Name,type_name=first_rule.Type,parameters=my_item_list)
            modify_rule_req_mesg = AnalyticsRequestMessages.ModifyRulesMessage(configuration_token=video_analytics_configuration_token,rule=modified_rule_config)
            print(f'Created ModifyRulesMessage Request message : \n{modify_rule_req_mesg.to_dict()}')
            
            modify_rule_status = analytics_serv.ModifyRules(request_message=modify_rule_req_mesg)

            if modify_rule_status:
                rules = analytics_serv.GetRules(configuration_token=video_analytics_configuration_token)
                for rule in rules:
                    print(f'Rule Name is "{rule.Name}" and Type is "{rule.Type}";\n{rule}')

            rule_options = analytics_serv.GetRuleOptions(configuration_token=video_analytics_configuration_token,rule_type=first_rule.Type)
            print(f'GetRuleOptions response :\n{rule_options}')
        
        else:
            print("Analytics service not supported!")

