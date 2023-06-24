"""
Created to control Onvif Analitic service properties.

craeted by : enstns
created time : 20.05.23
"""
import logging

from lib.onvif import OnvifService, get_caching_client
from lib.requests_messages.analytics_request_messages import AnalyticsRequestMessages

DEBUG = True
LOG = False

logger = logging.getLogger('analytics_service')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ANALYTIC_SERVICE_NS = "http://www.onvif.org/ver20/analytics/wsdl"

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

def get_analytics_namespace(services = [],xaddr=""):
    if services and services != None:
        for serv in services:
            ns = str(serv.Namespace)
            if serv.XAddr == xaddr and "analytics" in ns:
                return serv.Namespace
    else:
        return None
        
class AnalyticsService:
    def __init__(self,onvif_service = OnvifService()) -> None:
        self.is_analytics_service_supported = False
        self.onvif_service = onvif_service
        self.wsdlUrl = self.onvif_service.wsdl_directory + "/analytics.wsdl"
        self.xAddr = "" 
        self.analytics_name_space = ""
        self.capabilities = {}
        self.set_analytics_service_variables()

    def set_analytics_service_variables(self) -> None:
        if self.onvif_service.get_con_status() and self.onvif_service.capabilities.Analytics != None:
            self.is_analytics_service_supported = True
            self.xAddr = self.onvif_service.capabilities.Analytics.XAddr
            self.analytics_name_space = get_analytics_namespace(services = self.onvif_service.services,xaddr = self.xAddr)
            self.capabilities = self.GetServiceCapabilities()
        else:
            logger.error(f"Analytics service not sported from {self.onvif_service.ip}")
    # AnalyticsEngineBinding
    def GetServiceCapabilities(self) -> dict:
        """
        Returns the capabilities of the analytics service. The result is returned in a typed answer.
        - return [dict];
            - Capabilities [Capabilities]
                The capabilities for the analytics service is returned in the Capabilities element.
        """
        service_cap = {}
        if self.onvif_service.get_con_status():
            if self.is_analytics_service_supported:
                logger.info(f"Try to GetServiceCapabilities information..")
                try:
                    zeepAnalyticsClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_analytics = zeepAnalyticsClient.create_service("{" + self.analytics_name_space + "}AnalyticsEngineBinding", self.xAddr)
                    service_cap = ws_client_analytics.GetServiceCapabilities()
                except Exception as emsg:
                    logger.error(f"GetServiceCapabilities unsuccess.. -> {emsg}")
                else:
                    logger.info(f"GetServiceCapabilities complete with success..")
            else: logger.error(f"Analytics Service not supported..")
        else: logger.warning(f"No Onvif Connection!")
        return service_cap
    # AnalyticsEngineBinding
    def GetSupportedAnalyticsModules(self,configuration_token : str) -> list:
        """
        List all analytics modules that are supported by the given VideoAnalyticsConfiguration.
        - requirements ;
            - configuration_token [str]
                Reference to an existing VideoAnalyticsConfiguration. 
                - NOT: This parameters can be found with GetCompatibleVideoAnalyticsConfigurations method by Media Service
        - return [list];
            - SupportedAnalyticsModules [SupportedAnalyticsModules]
        """
        supported_analytics_modules = []
        if self.onvif_service.get_con_status():
            if self.is_analytics_service_supported:
                logger.info(f"Try to GetSupportedAnalyticsModules information..")
                try:
                    zeepAnalyticsClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_analytics = zeepAnalyticsClient.create_service("{" + self.analytics_name_space + "}AnalyticsEngineBinding", self.xAddr)
                    supported_analytics_modules = ws_client_analytics.GetSupportedAnalyticsModules(ConfigurationToken = configuration_token)
                except Exception as emsg:
                    logger.error(f"GetSupportedAnalyticsModules unsuccess.. -> {emsg}")
                else:
                    logger.info(f"GetSupportedAnalyticsModules complete with success..")
            else: logger.error(f"Analytics Service not supported..")
        else: logger.warning(f"No Onvif Connection!")
        return supported_analytics_modules
    # AnalyticsEngineBinding
    def CreateAnalyticsModules(self,request_message : AnalyticsRequestMessages.CreateAnalyticsModulesMessage) -> dict: # Not Tested
        """
        Add one or more analytics modules to an existing VideoAnalyticsConfiguration. 
        The available supported types can be retrieved via GetSupportedAnalyticsModules, where the Name of the supported AnalyticsModules correspond to the type of an AnalyticsModule instance.
        Pass unique module names which can be later used as reference. The Parameters of the analytics module must match those of the corresponding AnalyticsModuleDescription.
        - requirements;
            - request_message : [CreateAnalyticsModulesMessage]
                An Object for CreateAnalyticsModules request message 
        - return [boolean];
            - status : True means OK else False 
        """
        status = False
        if self.onvif_service.get_con_status():
            logger.info(f"Try to CreateAnalyticsModules request..")
            if self.is_analytics_service_supported:
                try:
                    zeepAnalyticsClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_analytics = zeepAnalyticsClient.create_service("{" + self.analytics_name_space + "}AnalyticsEngineBinding", self.xAddr)
                    ws_client_analytics.CreateAnalyticsModules(**request_message.to_dict())
                except Exception as emsg:
                    logger.error(f"CreateAnalyticsModules unsuccess.. -> {emsg}")
                else:
                    status = True
                    logger.info(f"CreateAnalyticsModules complete with success..")
            else:
                logger.error(f"Analytics Service not supported..")
        else: logger.warning(f"No Onvif Connection!")
        return status
    # AnalyticsEngineBinding
    def DeleteAnalyticsModules(self,configuration_token : str,analytics_module_name  : str) -> bool: # Not Tested
        """
        Remove one or more analytics modules from a VideoAnalyticsConfiguration referenced by their names.
        - requirements : 
            - configuration_token : [str] 
                Reference to an existing Video Analytics configuration.
            - analytics_module_name : [str] 
                Name of the AnalyticsModule to be deleted.
        - return [boolean]; 
            - Delete Analytics Modules status
        """
        delete_status = False
        if self.onvif_service.get_con_status():
            if self.is_analytics_service_supported:
                logger.info(f"Try to DeleteAnalyticsModules {analytics_module_name}..")
                try:
                    zeepAnalyticsClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_analytics = zeepAnalyticsClient.create_service("{" + self.analytics_name_space + "}AnalyticsEngineBinding", self.xAddr)
                    ws_client_analytics.DeleteAnalyticsModules(ConfigurationToken  = configuration_token,AnalyticsModuleName = analytics_module_name)
                except Exception as emsg:
                    logger.error(f"DeleteAnalyticsModules unsuccess.. -> {emsg}")
                else:
                    logger.info(f"DeleteAnalyticsModules complete with success..")
                    delete_status = True
            else: logger.warning(f"Analytics is not supported !")
        else: logger.warning(f"No Onvif Connection!")
        return delete_status
    # AnalyticsEngineBinding
    def GetAnalyticsModuleOptions(self,configuration_token : str,analytics_type = None) -> bool: # Not Tested
        """
        Return the options for the supported analytics modules that specify an Option attribute.
        - requirements : 
            - configuration_token : [str] 
                Reference to an existing AnalyticsConfiguration.
            - analytics_type - optional; [QName]
                Reference to an SupportedAnalyticsModule Type returned from GetSupportedAnalyticsModules.
        - return [dict];
            - Options - optional, unbounded; [ConfigOptions]
                List of options for the specified analytics module. The response Options shall not contain any RuleType attribute.
        """
        options = {}
        if self.onvif_service.get_con_status():
            if self.is_analytics_service_supported:
                logger.info(f"Try to GetAnalyticsModuleOptions information..")
                try:
                    zeepAnalyticsClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_analytics = zeepAnalyticsClient.create_service("{" + self.analytics_name_space + "}AnalyticsEngineBinding", self.xAddr)
                    if analytics_type != None:
                        options = ws_client_analytics.GetAnalyticsModuleOptions(ConfigurationToken = configuration_token,Type = analytics_type)
                    else:
                        options = ws_client_analytics.GetAnalyticsModuleOptions(ConfigurationToken = configuration_token)
                except Exception as emsg:
                    logger.error(f"GetAnalyticsModuleOptions unsuccess.. -> {emsg}")
                else:
                    logger.info(f"GetAnalyticsModuleOptions complete with success..")
            else: logger.error(f"Analytics Service not supported..")
        else: logger.warning(f"No Onvif Connection!")
        return options
    # AnalyticsEngineBinding
    def GetAnalyticsModules(self,configuration_token : str) -> list: # Not Tested
        """
        List the currently assigned set of analytics modules of a VideoAnalyticsConfiguration.
        - requirements : 
            - configuration_token : [str] 
                Reference to an existing AnalyticsConfiguration.
        - return [list];
            - AnalyticsModule - optional, unbounded; [Config]
                List of analytics modules 
        """
        analytics_modules = []
        if self.onvif_service.get_con_status():
            if self.is_analytics_service_supported:
                logger.info(f"Try to GetAnalyticsModules information..")
                try:
                    zeepAnalyticsClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_analytics = zeepAnalyticsClient.create_service("{" + self.analytics_name_space + "}AnalyticsEngineBinding", self.xAddr)
                    analytics_modules = ws_client_analytics.GetAnalyticsModules(ConfigurationToken = configuration_token)
                except Exception as emsg:
                    logger.error(f"GetAnalyticsModules unsuccess.. -> {emsg}")
                else:
                    logger.info(f"GetAnalyticsModules complete with success..")
            else: logger.error(f"Analytics Service not supported..")
        else: logger.warning(f"No Onvif Connection!")
        return analytics_modules
    # AnalyticsEngineBinding
    def GetSupportedMetadata(self,type_name = None) -> dict: # Not Tested
        """
        This method provides a computer readable description of the metadata that the selected analytics modules can generate. 
        The type parameter allows to select a single analytics module. 
        By default the output shall relate to all analytics modules that exist in the device.
        - requirements : 
            - type_name - optional; [QName]
                Optional reference to an AnalyticsModule Type returned from GetSupportedAnalyticsModules.
        - return [dict];
            - AnalyticsModule - optional, unbounded; [MetadataInfo]
        """
        supported_metadata = {}
        if self.onvif_service.get_con_status():
            if self.is_analytics_service_supported:
                logger.info(f"Try to GetSupportedMetadata information..")
                try:
                    zeepAnalyticsClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_analytics = zeepAnalyticsClient.create_service("{" + self.analytics_name_space + "}AnalyticsEngineBinding", self.xAddr)
                    if type_name != None:
                        supported_metadata = ws_client_analytics.GetSupportedMetadata(Type = type_name)
                    else:
                        supported_metadata = ws_client_analytics.GetSupportedMetadata()
                except Exception as emsg:
                    logger.error(f"GetSupportedMetadata unsuccess.. -> {emsg}")
                else:
                    logger.info(f"GetSupportedMetadata complete with success..")
            else: logger.error(f"Analytics Service not supported..")
        else: logger.warning(f"No Onvif Connection!")
        return supported_metadata
    # AnalyticsEngineBinding
    def ModifyAnalyticsModules(self,request_message : AnalyticsRequestMessages.ModifyAnalyticsModulesMessage) -> bool: # Not Tested
        """
        Modify the settings of one or more analytics modules of a VideoAnalyticsConfiguration. 
        The modules are referenced by their names. It is allowed to pass only a subset to be modified.
        - requirements;
            - request_message : [ModifyAnalyticsModulesMessage]
                An Object for ModifyAnalyticsModules request message 
        - return [boolean];
            - status : True means OK else False 
        """
        status = False
        if self.onvif_service.get_con_status():
            logger.info(f"Try to ModifyAnalyticsModules request..")
            if self.is_analytics_service_supported:
                try:
                    zeepAnalyticsClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_analytics = zeepAnalyticsClient.create_service("{" + self.analytics_name_space + "}AnalyticsEngineBinding", self.xAddr)
                    ws_client_analytics.ModifyAnalyticsModules(**request_message.to_dict())
                except Exception as emsg:
                    logger.error(f"ModifyAnalyticsModules unsuccess.. -> {emsg}")
                else:
                    status = True
                    logger.info(f"ModifyAnalyticsModules complete with success..")
            else: logger.error(f"Analytics Service not supported..")
        else: logger.warning(f"No Onvif Connection!")
        return status
    # RuleEngineBinding
    def CreateRules(self,request_message : AnalyticsRequestMessages.CreateRulesMessage) -> bool:
        """
        Add one or more analytics modules to an existing VideoAnalyticsConfiguration. 
        The available supported types can be retrieved via GetSupportedAnalyticsModules, \
            where the Name of the supported AnalyticsModules correspond to the type of an AnalyticsModule instance.
        - requirements;
            - request_message : [CreateRulesMessage]
                An Object for CreateRules request message 
        - return [boolean];
            - status : True means OK else False 
        """
        status = False
        if self.onvif_service.get_con_status():
            logger.info(f"Try to CreateRules request..")
            if self.is_analytics_service_supported:
                try:
                    zeepAnalyticsClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_analytics = zeepAnalyticsClient.create_service("{" + self.analytics_name_space + "}RuleEngineBinding", self.xAddr)
                    ws_client_analytics.CreateRules(**request_message.to_dict())
                except Exception as emsg:
                    logger.error(f"CreateRules unsuccess.. -> {emsg}")
                else:
                    status = True
                    logger.info(f"CreateRules complete with success..")
            else: logger.error(f"Analytics Service not supported..")
        else: logger.warning(f"No Onvif Connection!")
        return status
    # RuleEngineBinding
    def DeleteRules(self,configuration_token : str,rule_name : str) -> bool:
        """
        Remove one or more rules from a VideoAnalyticsConfiguration.
        - requirements : 
            - configuration_token : [str] 
                Reference to an existing Video Analytics configuration.
            - rule_name : [str] 
                References the specific rule to be deleted (e.g. "MyLineDetector").
        - return [boolean]; 
            - Delete Rules status
        """
        delete_status = False
        if self.onvif_service.get_con_status():
            if self.is_analytics_service_supported:
                logger.info(f"Try to DeleteRules {rule_name}..")
                try:
                    zeepAnalyticsClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_analytics = zeepAnalyticsClient.create_service("{" + self.analytics_name_space + "}RuleEngineBinding", self.xAddr)
                    ws_client_analytics.DeleteRules(ConfigurationToken = configuration_token,RuleName = rule_name)
                except Exception as emsg:
                    logger.error(f"DeleteRules unsuccess.. -> {emsg}")
                else:
                    logger.info(f"DeleteRules complete with success..")
                    delete_status = True
            else: logger.error(f"Analytics Service not supported..")
        else: logger.warning(f"No Onvif Connection!")
        return delete_status
    # RuleEngineBinding
    def GetRuleOptions(self,configuration_token : str,rule_type = None) -> dict:
        """
        Return the options for the supported rules that specify an Option attribute.
        - requirements : 
            - configuration_token : [str] 
                Reference to an existing analytics configuration.
            - rule_type - optional; [QName]
                Reference to an SupportedRule Type returned from GetSupportedRules.
        - return [dict];
            - RuleOptions - optional, unbounded; [ConfigOptions]
                A device shall provide respective ConfigOptions.
                RuleType for each RuleOption if the request does not specify RuleType. 
                The response Options shall not contain any AnalyticsModule attribute.
        """
        rule_options = {}
        if self.onvif_service.get_con_status():
            if self.is_analytics_service_supported:
                logger.info(f"Try to GetRuleOptions information..")
                try:
                    zeepAnalyticsClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_analytics = zeepAnalyticsClient.create_service("{" + self.analytics_name_space + "}RuleEngineBinding", self.xAddr)
                    if rule_type != None: 
                        rule_options = ws_client_analytics.GetRuleOptions(ConfigurationToken = configuration_token,RuleType = rule_type)
                    else: 
                        rule_options = ws_client_analytics.GetRuleOptions(ConfigurationToken = configuration_token)
                except Exception as emsg:
                    logger.error(f"GetRuleOptions unsuccess.. -> {emsg}")
                else: logger.info(f"GetRuleOptions complete with success..")
            else: logger.error(f"Analytics Service not supported..")
        else: logger.warning(f"No Onvif Connection!")
        return rule_options
    # RuleEngineBinding
    def GetRules(self,configuration_token : str) -> list:
        """
        List the currently assigned set of rules of a VideoAnalyticsConfiguration.
        - requirements : 
            - configuration_token : [str] 
                Reference to an existing VideoAnalyticsConfiguration.
        - return [list];
            - Rule - optional, unbounded; [Config]
                List of Rules 
        """
        rules = []
        if self.onvif_service.get_con_status():
            if self.is_analytics_service_supported:
                logger.info(f"Try to GetRules information..")
                try:
                    zeepAnalyticsClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_analytics = zeepAnalyticsClient.create_service("{" + self.analytics_name_space + "}RuleEngineBinding", self.xAddr)
                    rules = ws_client_analytics.GetRules(ConfigurationToken = configuration_token)
                except Exception as emsg:
                    logger.error(f"GetRules unsuccess.. -> {emsg}")
                else:
                    logger.info(f"GetRules complete with success..")
            else: logger.error(f"Analytics Service not supported..")
        else: logger.warning(f"No Onvif Connection!")
        return rules
    # RuleEngineBinding
    def GetSupportedRules(self,configuration_token : str) -> list:
        """
        List all rules that are supported by the given VideoAnalyticsConfiguration.
        - requirements : 
            - configuration_token : [str] 
                References an existing Video Analytics configuration. 
                The list of available tokens can be obtained via the Media service GetVideoAnalyticsConfigurations method.
        - return [list];
            - SupportedRules [SupportedRules]
        """
        supported_rules = []
        if self.onvif_service.get_con_status():
            if self.is_analytics_service_supported:
                logger.info(f"Try to GetSupportedRules information..")
                try:
                    zeepAnalyticsClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_analytics = zeepAnalyticsClient.create_service("{" + self.analytics_name_space + "}RuleEngineBinding", self.xAddr)
                    supported_rules = ws_client_analytics.GetSupportedRules(ConfigurationToken = configuration_token)
                except Exception as emsg:
                    logger.error(f"GetSupportedRules unsuccess.. -> {emsg}")
                else:
                    logger.info(f"GetSupportedRules complete with success..")
            else: logger.error(f"Analytics Service not supported..")
        else: logger.warning(f"No Onvif Connection!")
        return supported_rules
    # RuleEngineBinding
    def ModifyRules(self,request_message : AnalyticsRequestMessages.ModifyRulesMessage) -> bool:
        """
        Modify one or more rules of a VideoAnalyticsConfiguration. The rules are referenced by their names.
        - requirements;
            - request_message : [ModifyRulesMessage]
                An Object for ModifyRules request message 
        - return [boolean];
            - status : True means OK else False 
        """
        status = False
        if self.onvif_service.get_con_status():
            logger.info(f"Try to ModifyRules request..")
            if self.is_analytics_service_supported:
                try:
                    zeepAnalyticsClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_analytics = zeepAnalyticsClient.create_service("{" + self.analytics_name_space + "}RuleEngineBinding", self.xAddr)
                    ws_client_analytics.ModifyRules(**request_message.to_dict())
                except Exception as emsg:
                    logger.error(f"ModifyRules unsuccess.. -> {emsg}")
                else:
                    status = True
                    logger.info(f"ModifyRules complete with success..")
            else: logger.error(f"Analytics Service not supported..")
        else: logger.warning(f"No Onvif Connection!")
        return status