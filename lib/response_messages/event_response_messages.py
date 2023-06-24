import datetime
import json
from lib.params.event_request_params import PullMessageEncoder,EventEnumParams

class EventResponseMessages:
    class PullMessagesResponse:
        def __init__(self,current_time = datetime.datetime.strptime("2000-01-01T00:00:00Z",'%Y-%m-%dT%H:%M:%SZ'),termination_time = datetime.datetime.strptime("2000-01-01T00:00:00Z",'%Y-%m-%dT%H:%M:%SZ'),notification_messages = []) -> None:
            self.CurrentTime = current_time
            self.TerminationTime = termination_time
            self.NotificationMessage = notification_messages

        def __repr__(self) -> str:
            return json.dumps(self.__dict__,cls=PullMessageEncoder,indent=4) # json.dumps(self.__dict__, indent=4)
        
        def __str__(self) -> str:
            return json.dumps(self.__dict__,cls=PullMessageEncoder,indent=4) # json.dumps(self.__dict__, indent=4)