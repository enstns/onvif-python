import datetime
from enum import Enum
import json

class PullMessageEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, EventRequestParams.NotificationMessage):
            return obj.__dict__
        elif isinstance(obj, EventRequestParams.SimpleItem):
            return obj.__dict__
        else:
            return super().default(obj)

class EventEnumParams:
    pass

class EventRequestParams:
    class FilterType:
        pass

    class SimpleItem:
        def __init__(self,name = None,value = None) -> None:
            self.Name = name
            self.Value = value

        def __str__(self) -> str:
            return str(self.__dict__)

        def __repr__(self) -> str:
            return str(self.__dict__)

    class NotificationMessage:
        def __init__(self,source : 'EventRequestParams.SimpleItem',data : 'EventRequestParams.SimpleItem',topic = "",message = {}) -> None:
            self.Topic = topic
            self.Message = message
            self.Source = source
            self.Data = data

        def __repr__(self) -> str:
            return json.dumps(self.__dict__,cls=PullMessageEncoder,indent=4) # json.dumps(self.__dict__, indent=4)
        
        def __str__(self) -> str:
            return json.dumps(self.__dict__,cls=PullMessageEncoder,indent=4)

    class EventBrokerConfig:
        def __init__(self,address : str,topic_perifix : str,username = None,password = None,certificate_id = None,\
                    publish_filter = None,qos = None,status = None,cert_path_validation_policy_id = None,metadata_filter = None) -> None:
            """
            - requirements;
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
            self.Address = address
            self.TopicPrefix = topic_perifix
            if username != None: self.UserName = username
            if password != None: self.Password = password
            if certificate_id != None: self.CertificateID = certificate_id
            if publish_filter != None:
                if type(publish_filter) != dict: self.PublishFilter = publish_filter.to_dict()
                else: self.PublishFilter = publish_filter
            if qos != None: self.Qos = qos
            if status != None: self.Status = status
            if cert_path_validation_policy_id != None: self.CertPathValidationPolicyID = cert_path_validation_policy_id
            if metadata_filter != None:
                if type(metadata_filter) != dict: self.MetadataFilter = metadata_filter.to_dict()
                else: self.MetadataFilter = metadata_filter
    
        def to_dict(self) -> dict:
            return self.__dict__