"""
Created to test Onvif Analytics service properties.

craeted by : enstns
created time : 23.05.23
"""
import path 
import sys
 
# directory reach
directory = path.Path(__file__).abspath()
 
# setting path
parent_directory = directory.parent.parent
sys.path.append(parent_directory)
 
# importing
from lib.params.analytics_request_params import AnalyticsRequestParams
from lib.services.analytics_service import AnalyticsService
from lib.requests_messages.analytics_request_messages import AnalyticsRequestMessages

from lib.onvif import OnvifService
from lib.services.media_service import MediaService

onvif_device = OnvifService()

# device information
# onvif_device.ip = "192.168.1.168"
# onvif_device.username = "admin"
# onvif_device.password = "9999"
# onvif_device.port = "80"

DEBUG = False

onvif_device.ip = "11.63.1.6"
onvif_device.username = "admin"
onvif_device.password = "12345"
onvif_device.port = "80"

onvif_device.wsdl_directory = parent_directory+ "/wsdl"

# onvif device connection
onvif_device.connect_onvif()

class XYZPoint:
    def __init__(self,x = 0.0, y = 0.0, z = 0.0) -> None:
        self.x = x
        self.y = y
        self.z = z

class XYZPolygon:
    def __init__(self,points = [],id = 0) -> None:
        self.points = points
        self.id = id

def is_inside_polygon(point : XYZPoint,polygon : XYZPolygon) -> bool:
    return False

def generateActiveCells(layout = {},roi = [],width = 0,height = 0):
    cell_bits = ""
    cell_count = int(layout["Columns"]) * int(layout["Rows"])
    for i in range(cell_count):
        cell_bits += "0"
    
    cell_width = width / int(layout["Columns"])
    cell_height = height / int(layout["Rows"])	
    cell_number = 0

    polygons = []

    for i in range(roi):
        p1 = XYZPoint()
        p2 = XYZPoint()
        p3 = XYZPoint()
        p4 = XYZPoint()

        p1.x = roi[i].get_roi_points().get(0).x
        p1.y = roi[i].get_roi_points().get(0).y
        p2.x = roi[i].get_roi_points().get(1).x
        p2.y = roi[i].get_roi_points().get(1).y
        p3.x = roi[i].get_roi_points().get(2).x
        p3.y = roi[i].get_roi_points().get(2).y
        p4.x = roi[i].get_roi_points().get(3).x
        p4.y = roi[i].get_roi_points().get(3).y

        points = []
        points.append(p1)
        points.append(p2)
        points.append(p3)
        points.append(p4)

        polygon = XYZPolygon()
        polygon.points = points

        polygons.append(polygon)

    counter_1 = 0
    counter_2 = 0
    while counter_1<height:
        while counter_2<width:
            if (counter_2 + cell_width > width): break
            p1 = XYZPoint()
            p2 = XYZPoint()
            p3 = XYZPoint()
            p4 = XYZPoint()
            mid = XYZPoint()

            p1.x = counter_2
            p1.y = counter_1
            p2.x = (counter_2 + cell_width)
            p2.y = (counter_1)
            p3.x = (counter_2)
            p3.y = (counter_1 + cell_height)
            p4.x = (counter_2 + cell_width)
            p4.y = (counter_1 + cell_height)

            mid.x = (p1.x + p4.x)/2
            mid.y = (p1.y + p4.y)/2

            for p in polygons:
                if is_inside_polygon(mid,p):
                    cell_bits[cell_number] = "1"
                    break
            cell_number = cell_number + 1
            counter_2 = counter_2 + cell_width
        counter_1 = counter_1 + cell_height

    if len(cell_bits) % 8 != 0:
        add_bit_count = 8 - len(cell_bits) % 8
        for i in range(add_bit_count):
            # cell_bits


print(f'Analytics Capabilities response :\n{onvif_device.capabilities.Analytics}')

print(f'Start to Test Analytics Service...') 

analytics_serv = AnalyticsService(onvif_service=onvif_device)
if analytics_serv.is_analytics_service_supported:
    print(f'Analytics service is supported...')

    analy_capabilities = analytics_serv.GetServiceCapabilities()
    print(f'GetServiceCapabilities response :\n{analy_capabilities}')

    # create media service 
    media_serv = MediaService(onvif_service=onvif_device)
    profile_token = onvif_device.get_first_profile().token
    configurations = media_serv.GetCompatibleVideoAnalyticsConfigurations(profile_token=profile_token)
    if DEBUG: print(f'GetCompatibleVideoAnalyticsConfigurations response :\n{configurations}')
    if configurations:
        first_configs = configurations[0]
        video_analytics_configuration_token = first_configs.token

        supported_analytics_modules = analytics_serv.GetSupportedAnalyticsModules(configuration_token=video_analytics_configuration_token)
        if DEBUG: print(f'GetSupportedAnalyticsModules response :\n{supported_analytics_modules}')

        analytics_modules = analytics_serv.GetAnalyticsModules(configuration_token=video_analytics_configuration_token)
        if DEBUG: print(f'GetAnalyticsModules response :\n{analytics_modules}')

        is_layout_find = False
        for module in analytics_modules:
            module_element_items = module.Parameters.ElementItem
            for element_item in module_element_items: 
                if element_item.Name == "Layout":
                    module_layout =  element_item._value_1.attrib
                    module_name = module.Name
                    is_layout_find = True
                    break
            if is_layout_find:
                break
        
        if not DEBUG: print(f'Layout of {module_name} is -> {module_layout}')

        supported_rules = analytics_serv.GetSupportedRules(configuration_token=video_analytics_configuration_token)
        if DEBUG: print(f'GetSupportedRules response :\n{supported_rules}')

        rules = analytics_serv.GetRules(configuration_token=video_analytics_configuration_token)
        if DEBUG: print(f'Before Create Rule method GetRules response :\n{rules}')

        created_rule_simple_item = AnalyticsRequestParams.SimpleItem(name="MinCount",value="30").to_dict()
        my_item_list = AnalyticsRequestParams.ItemList(simple_item=created_rule_simple_item)
        created_rule_config = AnalyticsRequestParams.Config(name="TestMotionDetector",type_name="tt:CellMotionDetector",parameters=my_item_list)
        created_rule_req_mesg = AnalyticsRequestMessages.CreateRulesMessage(configuration_token=video_analytics_configuration_token,rule=created_rule_config)
        if DEBUG: print(f'Created CreateRulesMessage Request message is : \n{created_rule_req_mesg.to_dict()}')

        create_rule_status = analytics_serv.CreateRules(request_message=created_rule_req_mesg)
        rules = analytics_serv.GetRules(configuration_token=video_analytics_configuration_token)
        if DEBUG: print(f'After Create Rule method GetRules response :\n{rules}')

        analytics_serv.DeleteRules(configuration_token=video_analytics_configuration_token,rule_name="TestMotionDetector")
        rules = analytics_serv.GetRules(configuration_token=video_analytics_configuration_token)
        if DEBUG: print(f'After Delete Rule TestMotionDetector, GetRules response :\n{rules}')

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
        if DEBUG: print(f'Created ModifyRulesMessage Request message : \n{modify_rule_req_mesg.to_dict()}')

        modify_rule_status = analytics_serv.ModifyRules(request_message=modify_rule_req_mesg)

        if modify_rule_status:
            rules = analytics_serv.GetRules(configuration_token=video_analytics_configuration_token)
            for rule in rules:
                if DEBUG: print(f'Rule Name is "{rule.Name}" and Type is "{rule.Type}";\n{rule}')

        rule_options = analytics_serv.GetRuleOptions(configuration_token=video_analytics_configuration_token,rule_type=first_rule.Type)
        if DEBUG: print(f'GetRuleOptions response :\n{rule_options}')

else:
    if DEBUG: print(f'Analytics service not supported!')



