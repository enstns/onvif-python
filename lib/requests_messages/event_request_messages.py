from lib.params.event_request_params import EventEnumParams,EventRequestParams
 
class EventRequestMessages:
    class AddEventBrokerRequestMessage:
        def __init__(self,event_broker_config : EventRequestParams.EventBrokerConfig) -> None:
            """
            The AddEventBroker command allows an ONVIF client to add an event broker configuration to device to enable ONVIF events to be transferred to an event broker. If an existing event broker configuration already exists with the same Address, the existing configuration shall be modified.
            - requirements:
                - EventBrokerConfig ; [EventBrokerConfig]
            """
            self.EventBrokerConfig = event_broker_config.to_dict()

        def to_dict(self) -> dict:
            return self.__dict__
    
    class CreatePullPointSubscriptionRequestMessage:
        def __init__(self,filter : EventRequestParams.FilterType,initial_termination_time : str,subscription_policy = None) -> None:
            """
            This method returns a PullPointSubscription that can be polled using PullMessages. This message contains the same elements as the SubscriptionRequest of the WS-BaseNotification without the ConsumerReference.
            If no Filter is specified the pullpoint notifies all occurring events to the client.
            This method is mandatory.
            - requirements:
                - Filter - optional; [FilterType]
                    Optional XPATH expression to select specific topics.
                - InitialTerminationTime - optional, nillable; [AbsoluteOrRelativeTimeType]
                    Initial termination time.
                - SubscriptionPolicy - optional;
                    Refer to Web Services Base Notification 1.3 (WS-BaseNotification).
            """
            self.Filter = filter
            self.InitialTerminationTime = initial_termination_time
            if subscription_policy != None: self.SubscriptionPolicy = subscription_policy

        def to_dict(self) -> dict:
            return self.__dict__
     