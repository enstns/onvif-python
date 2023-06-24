"""
Created to control Onvif Event service properties.

craeted by : enstns
created time : 01.04.23
"""
import datetime
import logging
from zeep import CachingClient, Settings, xsd
import xml.etree.ElementTree as ET

from lib.onvif import HISTORY, OnvifService, isfile_exist
from lib.requests_messages.event_request_messages import EventRequestMessages
from lib.params.event_request_params import EventEnumParams, EventRequestParams
from lib.response_messages.event_response_messages import EventResponseMessages
from zeep.wsse.username import UsernameToken

DEBUG = True
LOG = False


SETTINGS = Settings()
SETTINGS.strict = False
SETTINGS.xml_huge_tree = True
# SETTINGS.raw_response = True

logger = logging.getLogger('event_service')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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

def get_event_namespace(services = [],xaddr=""):
    if services and services != None:
        for serv in services:
            ns = str(serv.Namespace)
            if serv.XAddr == xaddr and "event" in ns:
                return serv.Namespace
    else:
        return None
        
def get_caching_client(isAuth : bool,wsdl_URL : str,username_token : UsernameToken,settings = SETTINGS):
    caching_client = None
    if isfile_exist(wsdl_URL) or wsdl_URL.find("http://www.onvif.org") != -1:
        try:
            if isAuth: 
                caching_client = CachingClient(wsdl=wsdl_URL, wsse=username_token, settings=settings,plugins=[HISTORY])
            else: 
                caching_client = CachingClient(wsdl=wsdl_URL, settings=settings,plugins=[HISTORY])
        except Exception as emsg:
            logger.error(f"create caching client exception : -> {emsg}")
    else:
        logger.error(f"no such a file directory : {str(wsdl_URL)}")
    return caching_client

def pull_response_parser(pull_response_xml : str) -> EventResponseMessages.PullMessagesResponse:
    """
        TODO: Parse PullMessages xml response message
        - parameters : [str] xml response string
        - return : [dict] PullMessages
    """
    pull_response = EventResponseMessages.PullMessagesResponse()
    try:
        tree = ET.fromstring(pull_response_xml)  
        current_time = tree.find('.//{http://www.onvif.org/ver10/events/wsdl}CurrentTime').text
        termination_time = tree.find('.//{http://www.onvif.org/ver10/events/wsdl}TerminationTime').text
        try:
            pull_response.CurrentTime = datetime.datetime.strptime(current_time, '%Y-%m-%dT%H:%M:%SZ') #2000-01-01T00:00:00Z
            pull_response.TerminationTime = datetime.datetime.strptime(termination_time, '%Y-%m-%dT%H:%M:%SZ') #2000-01-01T00:00:00Z
        except Exception as emsg:
            logger.error(f"pull_response_parser - {emsg}")
        else:
            notification_messages = tree.findall('.//{http://docs.oasis-open.org/wsn/b-2}NotificationMessage')
            messages = []
            for notif_mes in notification_messages:
                message = EventRequestParams.NotificationMessage(source=EventRequestParams.SimpleItem,data=EventRequestParams.SimpleItem)
                message.Topic = notif_mes.find('.//{http://docs.oasis-open.org/wsn/b-2}Topic').text
                mes = notif_mes.find('.//{http://docs.oasis-open.org/wsn/b-2}Message').find('.//{http://www.onvif.org/ver10/schema}Message')
                message.Message = mes.attrib
                # message.Source = mes.find('.//{http://www.onvif.org/ver10/schema}Source').find(".//{http://www.onvif.org/ver10/schema}SimpleItem").attrib
                source = mes.find('.//{http://www.onvif.org/ver10/schema}Source').find(".//{http://www.onvif.org/ver10/schema}SimpleItem").attrib
                message.Source = EventRequestParams.SimpleItem(name = source["Name"],value=source["Value"])
                # message.Data = mes.find('.//{http://www.onvif.org/ver10/schema}Data').find(".//{http://www.onvif.org/ver10/schema}SimpleItem").attrib
                data = mes.find('.//{http://www.onvif.org/ver10/schema}Data').find(".//{http://www.onvif.org/ver10/schema}SimpleItem").attrib
                message.Data = EventRequestParams.SimpleItem(name = data["Name"],value=data["Value"])
                messages.append(message)
            pull_response.NotificationMessage = messages
    except Exception as emsg:
        logger.error(f"pull_response_parser - PullMessages Unsuccess, XML parse Error! - {emsg}")
    else:
        logger.info(f"PullMessages, XML parsing complete with success..")
    return pull_response

class EventService:
    def __init__(self,onvif_service = OnvifService()) -> None:
        self.is_event_service_supported = False
        self.onvif_service = onvif_service
        self.event_name_space = ""
        self.wsdlUrl = self.onvif_service.wsdl_directory + "/events.wsdl"
        self.xAddr = "" 
        self.event_service_capabilities = {}
        self.set_event_service_variables()

    def set_event_service_variables(self) -> None:
        if self.onvif_service.get_con_status() and self.onvif_service.capabilities.Events != None:
            self.is_event_service_supported = True
            self.xAddr = self.onvif_service.capabilities.Events.XAddr
            self.event_name_space = get_event_namespace(services = self.onvif_service.services,xaddr = self.xAddr)
            self.event_service_capabilities = self.GetServiceCapabilities()
        else:
            logger.error(f"Event service not sported from {self.onvif_service.ip}")

    # EventBinding & NOT Tested
    def GetServiceCapabilities(self) -> dict:
        """
        Returns the capabilities of the event service. The result is returned in a typed answer.
        - return [dict];
            - Capabilities [Capabilities]
                The capabilities for the event service is returned in the Capabilities element.
        """
        service_cap = {}
        if self.is_event_service_supported:
            logger.info(f"Try to GetServiceCapabilities information..")
            try:
                zeepEventClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                ws_client_event = zeepEventClient.create_service("{" + self.event_name_space + "}EventBinding", self.xAddr)
                service_cap = ws_client_event.GetServiceCapabilities()
            except Exception as emsg:
                logger.error(f"GetServiceCapabilities unsuccess.. -> {emsg}")
            else:
                logger.info(f"GetServiceCapabilities complete with success..")
        return service_cap

    # EventBinding & NOT Tested  
    def AddEventBroker(self, request_message : EventRequestMessages.AddEventBrokerRequestMessage) -> bool:
        """
        The AddEventBroker command allows an ONVIF client to add an event broker configuration to device to enable ONVIF events to be transferred to an event broker. If an existing event broker configuration already exists with the same Address, the existing configuration shall be modified.
        - requirements:
            - request_message : [AddEventBrokerRequestMessage]   
        - return:
            - status : [boolean] True means OK else False 
        """
        status = False
        if self.onvif_service.get_con_status():
            logger.info(f"Try to AddEventBroker request..")
            if self.is_event_service_supported and self.event_service_capabilities.EventBrokerProtocols:
                try:
                    zeep_event_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_event = zeep_event_client.create_service("{" + self.event_name_space + "}EventBinding", self.xAddr)
                    ws_client_event.AddEventBroker(**request_message.to_dict())
                except Exception as emsg:
                    logger.error(f"AddEventBroker unsuccess.. -> {emsg}")
                else:
                    logger.info(f"AddEventBroker complete with success..")
                    status = True
            else:
                logger.error(f"Event Service not supported..")
        return status

    # EventBinding & NOT Tested  
    def DeleteEventBroker(self,address : str) -> bool:
        """
        The DeleteEventBroker allows an ONVIF client to delete an event broker configuration from an ONVIF device.
        - requirements;
            - Address : [anyURI]
        - return; 
            status : [boolean] True means OK else False 
        """
        status = False
        if self.onvif_service.get_con_status():
            logger.info(f"Try to DeleteEventBroker request..")
            if self.is_event_service_supported and self.event_service_capabilities.EventBrokerProtocols:
                try:
                    zeepEventClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_event = zeepEventClient.create_service("{" + self.event_name_space + "}EventBinding", self.xAddr)
                    ws_client_event.DeleteEventBroker(Address = address)
                except Exception as emsg:
                    logger.error(f"DeleteEventBroker unsuccess.. -> {emsg}")
                else:
                    status = True
                    logger.info(f"DeleteEventBroker complete with success..")
            else:
                logger.error(f"Event Service not supported..")
        return status

    # EventBinding & NOT Tested  
    def GetEventBrokers(self,address : str) -> list:
        """
        The GetEventBrokers command lets a client retrieve event broker configurations from the device.
        - requirements;
            - Address : [anyURI]
        - return; 
            - brokers : [list]
                - EventBroker - optional, unbounded; [EventBrokerConfig]
                    - Address [anyURI]
                        Event broker address in the format "scheme://host:port[/resource]". The supported schemes shall be returned by the EventBrokerProtocols capability. The resource part of the URL is only valid when using websocket. The Address must be unique.
                    - TopicPrefix [string]
                        Prefix that will be prepended to all topics before they are published. This is used to make published topics unique for each device. TopicPrefix is not allowed to be empty.
                    - UserName - optional; [string]
                        User name for the event broker.
                    - Password - optional; [string]
                        Password for the event broker. Password shall not be included when returned with GetEventBrokers.
                    - CertificateID - optional; [token]
                        Optional certificate ID in the key store pointing to a client certificate to be used for authenticating the device at the message broker.
                    - PublishFilter - optional; [FilterType]
                        Concrete Topic Expression to select specific event topics to publish.
                    - QoS - optional; [int]
                        Quality of service level to use when publishing. This defines the guarantee of delivery for a specific message: 0 = At most once, 1 = At least once, 2 = Exactly once.
                    - Status - optional; [string]
                        Current connection status (see tev:ConnectionStatus for possible values).
                    - CertPathValidationPolicyID - optional; [string]
                        The ID of the certification path validation policy used to validate the broker certificate. In case encryption is used but no validation policy is specified, the device shall not validate the broker certificate.
                    - MetadataFilter - optional; [FilterType]
                        Concrete Topic Expression to select specific metadata topics to publish.
        """
        brokers = []
        if self.onvif_service.get_con_status():
            logger.info(f"Try to GetEventBrokers request..")
            if self.is_event_service_supported and self.event_service_capabilities.EventBrokerProtocols:
                try:
                    zeepEventClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_event = zeepEventClient.create_service("{" + self.event_name_space + "}EventBinding", self.xAddr)
                    brokers = ws_client_event.GetEventBrokers(Address = address)
                except Exception as emsg:
                    logger.error(f"GetEventBrokers unsuccess.. -> {emsg}")
                else:
                    logger.info(f"GetEventBrokers complete with success..")
            else:
                logger.error(f"Event Service not supported..")
        return brokers

    # EventBinding  
    def GetEventProperties(self) -> dict:
        """
        The GetEventBrokers command lets a client retrieve event broker configurations from the device.
        - requirements;
            None
        - return; 
            - [dict] :
                - TopicNamespaceLocation - unbounded; [anyURI]
                    List of topic namespaces supported.
                - FixedTopicSet [FixedTopicSet]
                    True when topicset is fixed for all times.
                - TopicSet [TopicSet]
                    Set of topics supported.
                - TopicExpressionDialect - unbounded; [TopicExpressionDialect]
                    Defines the XPath expression syntax supported for matching topic expressions.
                    The following TopicExpressionDialects are mandatory for an ONVIF compliant device :
                        - http://docs.oasis-open.org/wsn/t-1/TopicExpression/Concrete
                        - http://www.onvif.org/ver10/tev/topicExpression/ConcreteSet.
                - MessageContentFilterDialect - unbounded; [anyURI]
                    Defines the XPath function set supported for message content filtering.
                    The following MessageContentFilterDialects should be returned if a device supports the message content filtering:
                        - http://www.onvif.org/ver10/tev/messageContentFilter/ItemFilter.
                    A device that does not support any MessageContentFilterDialect returns a single empty url.
                - ProducerPropertiesFilterDialect - optional, unbounded; [anyURI]
                    Optional ProducerPropertiesDialects. Refer to Web Services Base Notification 1.3 (WS-BaseNotification) for advanced filtering.
                - MessageContentSchemaLocation - unbounded; [anyURI]
                    The Message Content Description Language allows referencing of vendor-specific types. In order to ease the integration of such types into a client application, the GetEventPropertiesResponse shall list all URI locations to schema files whose types are used in the description of notifications, with MessageContentSchemaLocation elements.
                    This list shall at least contain the URI of the ONVIF schema file. 
        """
        event_properties = {}
        if self.onvif_service.get_con_status():
            logger.info(f"Try to GetEventProperties request..")
            if self.is_event_service_supported:
                try:
                    zeepEventClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_event = zeepEventClient.create_service("{" + self.event_name_space + "}EventBinding", self.xAddr)
                    event_properties = ws_client_event.GetEventProperties()
                except Exception as emsg:
                    logger.error(f"GetEventProperties unsuccess.. -> {emsg}")
                else:
                    logger.info(f"GetEventProperties complete with success..")
            else:
                logger.error(f"Event Service not supported..")
        return event_properties

    # EventBinding
    def CreatePullPointSubscription(self,request_message = None) -> dict:
        """
        This method returns a PullPointSubscription that can be polled using PullMessages. This message contains the same elements as the SubscriptionRequest of the WS-BaseNotification without the ConsumerReference.
        If no Filter is specified the pullpoint notifies all occurring events to the client.
        This method is mandatory.
        - requirements:
            - request_message : [CreatePullPointSubscriptionRequestMessage]   
        - return: [dict]
            - SubscriptionReference [EndpointReferenceType]
                Endpoint reference of the subscription to be used for pulling the messages.
            - CurrentTime [CurrentTime]
                Current time of the server for synchronization purposes.
            - TerminationTime [TerminationTime]
                Date time when the PullPoint will be shut down without further pull requests.
        """
        response = {}
        if self.onvif_service.get_con_status():
            logger.info(f"Try to CreatePullPointSubscription request..")
            if self.is_event_service_supported:
                try:
                    zeep_event_client = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_event = zeep_event_client.create_service("{" + self.event_name_space + "}EventBinding", self.xAddr)
                    if request_message != None: response = ws_client_event.CreatePullPointSubscription(**request_message.to_dict())
                    else: response = ws_client_event.CreatePullPointSubscription()
                except Exception as emsg:
                    logger.error(f"CreatePullPointSubscription unsuccess.. -> {emsg}")
                else:
                    logger.info(f"CreatePullPointSubscription complete with success..")
            else:
                logger.error(f"Event Service not supported..")
        return response
    
    # PullPointSubscription
    def PullMessages(self,address : str,timeout : str, message_limit : int) -> dict:
        """
        This method pulls one or more messages from a PullPoint. The device shall provide the following PullMessages command for all SubscriptionManager endpoints returned by the CreatePullPointSubscription command. This method shall not wait until the requested number of messages is available but return as soon as at least one message is available.

        The command shall at least support a Timeout of one minute. In case a device supports retrieval of less messages than requested it shall return these without generating a fault.
        - requirements:
            - Timeout [duration]
                Maximum time to block until this method returns.
            - MessageLimit [int]
                Upper limit for the number of messages to return at once. A server implementation may decide to return less messages.
        - return: [dict]
            - CurrentTime [dateTime]
                The date and time when the messages have been delivered by the web server to the client.
            - TerminationTime [dateTime] -> (PT1M)
                Date time when the PullPoint will be shut down without further pull requests.
            - NotificationMessage - optional, unbounded; [NotificationMessage]
                List of messages. This list shall be empty in case of a timeout.
        """
        pull_response = {}
        if self.onvif_service.get_con_status():
            logger.info(f"Try to PullMessages request..")
            if self.is_event_service_supported:
                try:
                    # <a:ReplyTo>
                    #    <a:Address>
                    #      http://www.w3.org/2005/08/addressing/anonymous                 
                    #    </a:Address>
                    # </a:ReplyTo>
                    header = xsd.ComplexType(
                        xsd.Sequence([
                            xsd.Element('{http://www.w3.org/2005/08/addressing}Address', xsd.String()),
                        ])
                    )
                    header_value = header(Address="http://www.w3.org/2005/08/addressing/anonymous")
                    # TODO: get message raw xml
                    zeepEventClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token(),settings=Settings(strict = False,xml_huge_tree = True,raw_response = True))
                    ws_client_event = zeepEventClient.create_service("{" + self.event_name_space + "}PullPointSubscriptionBinding", address = address)
                    pull_response_xml = ws_client_event.PullMessages(_soapheaders=[header_value],Timeout = timeout,MessageLimit = message_limit).text
                    pull_response = pull_response_parser(pull_response_xml)            
                except Exception as emsg:
                    logger.error(f"PullMessages unsuccess.. -> {emsg}")
                else:
                    logger.info(f"PullMessages complete with success..")
            else:
                logger.error(f"Event Service not supported..")
        return pull_response

    # SubscriptionManagerBinding
    def Renew(self,address : str,termination_time : str) -> dict:
        """
        This method update timeout value with termination time, for each PullPoint method this method should be used.
        The command shall at least support a Timeout of one minute. In case a device supports retrieval of less messages than requested it shall return these without generating a fault.
        The device shall provide the following Renew command for all SubscriptionManager endpoints returned by the CreatePullPointSubscription command. 
        
        - requirements:
            - TerminationTime [duration]
                Terminate time which blocked by PullMessage method.
        - return: [dict]
            - CurrentTime [dateTime]
                The date and time when the messages have been delivered by the web server to the client.
            - TerminationTime [dateTime] -> (PT1M)
                Date time to shut down the PullPoint.
        """
        renew_response = {}
        if self.onvif_service.get_con_status():
            logger.info(f"Try to Renew request..")
            if self.is_event_service_supported:
                try:
                    # TODO: get message raw xml
                    zeepEventClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token(),settings=SETTINGS)
                    ws_client_event = zeepEventClient.create_service("{" + self.event_name_space + "}SubscriptionManagerBinding", address = address)
                    renew_response = ws_client_event.Renew(TerminationTime = termination_time)
                except Exception as emsg:
                    logger.error(f"Renew unsuccess.. -> {emsg}")
                else:
                    logger.info(f"Renew complete with success..")
            else:
                logger.error(f"Event Service not supported..")
        return renew_response
    
    # PullPointSubscription & NOT Tested  
    def Seek(self,utctime : datetime, reverse : bool) -> dict:
        """
        This method readjusts the pull pointer into the past. A device supporting persistent notification storage shall provide the following Seek command for all SubscriptionManager endpoints returned by the CreatePullPointSubscription command. The optional Reverse argument can be used to reverse the pull direction of the PullMessages command.
        - requirements;
            - UtcTime : [dateTime] The date and time to match against stored messages.
            - Reverse : optional; [boolean] Reverse the pull direction of PullMessages.
        - return; 
            - status : [boolean] True means OK else False 
        """
        status = False
        if self.onvif_service.get_con_status():
            logger.info(f"Try to Seek request..")
            if self.is_event_service_supported:
                try:
                    zeepEventClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_event = zeepEventClient.create_service("{" + self.event_name_space + "}PullPointSubscriptionBinding", self.xAddr)
                    ws_client_event.Seek(UtcTime = utctime,Reverse = reverse)
                except Exception as emsg:
                    logger.error(f"Seek unsuccess.. -> {emsg}")
                else:
                    status = True
                    logger.info(f"Seek complete with success..")
            else:
                logger.error(f"Event Service not supported..")
        return status

    # PullPointSubscription & NOT Tested  
    def SetSynchronizationPoint(self) -> bool:
        """
        Properties inform a client about property creation, changes and deletion in a uniform way. \
            When a client wants to synchronize its properties with the properties of the device, \
                it can request a synchronization point which repeats the current status of all properties to which a client has subscribed. \
                    The PropertyOperation of all produced notifications is set to “Initialized”. \
                        The Synchronization Point is requested directly from the SubscriptionManager which was returned in either the SubscriptionResponse or in the CreatePullPointSubscriptionResponse. \
                            The property update is transmitted via the notification transportation of the notification interface. \
                                This method is mandatory.
        - return; 
            status : [boolean] True means OK else False 
        """
        status = False
        if self.onvif_service.get_con_status():
            logger.info(f"Try to SetSynchronizationPoint request..")
            if self.is_event_service_supported:
                try:
                    zeepEventClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_event = zeepEventClient.create_service("{" + self.event_name_space + "}PullPointSubscriptionBinding", self.xAddr)
                    ws_client_event.SetSynchronizationPoint()
                except Exception as emsg:
                    logger.error(f"SetSynchronizationPoint unsuccess.. -> {emsg}")
                else:
                    status = True
                    logger.info(f"SetSynchronizationPoint complete with success..")
            else:
                logger.error(f"Event Service not supported..")
        return status

    # PullPointSubscription  
    def Unsubscribe(self,address : str) -> bool:
        """
        The device shall provide the following Unsubscribe command for all SubscriptionManager endpoints returned by the CreatePullPointSubscription command.  
        This command shall terminate the lifetime of a pull point.
        - return; 
            status : [boolean] True means OK else False 
        """
        status = False
        if self.onvif_service.get_con_status():
            logger.info(f"Try to Unsubscribe request..")
            if self.is_event_service_supported and self.event_service_capabilities.WSPullPointSupport:
                try:
                    zeepEventClient = get_caching_client(isAuth=True,wsdl_URL=self.wsdlUrl,username_token=self.onvif_service.get_username_token())
                    ws_client_event = zeepEventClient.create_service("{" + self.event_name_space + "}PullPointSubscriptionBinding", address=address)
                    ws_client_event.Unsubscribe()
                except Exception as emsg:
                    logger.error(f"Unsubscribe unsuccess.. -> {emsg}")
                else:
                    status = True
                    logger.info(f"Unsubscribe complete with success..")
            else:
                logger.error(f"Event Service not supported..")
        return status
    