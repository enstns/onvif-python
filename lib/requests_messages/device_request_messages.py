from lib.params.device_request_params import DeviceEnumParams, DeviceRequestParams

class DeviceRequestMessages:
    class CreateUsersMessage:
        def __init__(self,user : DeviceRequestParams.User) -> None:
            """
            Creates new device users and corresponding credentials. Each user entry includes: username, password and user level. Either all users are created successfully or a fault message MUST be returned without creating any user. If trying to create several users with exactly the same username the request is rejected and no users are created. If password is missing, then fault message Too weak password is returned.
            - requirements : 
                - user - unbounded; [User] 
                    Creates new device users and corresponding credentials. 
            """
            if type(user) != dict: self.User = user.to_dict()
            else: self.User = user
    
        def to_dict(self) -> dict:
            return self.__dict__
        
    class SetSystemDateAndTimeMessage:
        def __init__(self,date_time_type : DeviceEnumParams.SetDateTimeType,daylight_savings : bool,time_zone = None,UTC_datetime = None) -> None:
            """
            This operation sets the device system date and time. 
            The device shall support the configuration of the daylight saving setting and of the manual system date and time (if applicable) or indication of NTP time (if applicable) through the SetSystemDateAndTime command.
            - requirements : 
                - date_time_type [SetDateTimeType]
                    Defines if the date and time is set via NTP or manually.
                - daylight_savings [boolean]
                    Automatically adjust Daylight savings if defined in TimeZone.
                - time_zone - optional; [TimeZone]
                    The time zone in POSIX 1003.1 format
                - UTC_datetime - optional; [DateTime]
                    Date and time in UTC. If time is obtained via NTP, UTCDateTime has no meaning
            """
            self.DateTimeType = date_time_type.value
            self.DaylightSavings = daylight_savings
            if time_zone != None:
                if type(time_zone) != dict: self.TimeZone = time_zone.to_dict()
                else: self.TimeZone = time_zone
            if UTC_datetime != None:
                if type(UTC_datetime) != dict: self.UTCDateTime = UTC_datetime.to_dict()
                else: self.UTCDateTime  = UTC_datetime
    
        def to_dict(self) -> dict:
            return self.__dict__
        
    class SetNTPMessage:
        def __init__(self,from_DHCP : bool,NTP_manual = None) -> None:
            """
            SetNTP
            - requirements : 
                - from_DHCP [boolean]
                    Indicate if NTP address information is to be retrieved using DHCP.
                - NTP_manual - optional, unbounded; [NetworkHost]
                    Manual NTP settings.        
                """
            self.FromDHCP = from_DHCP
            if NTP_manual != None:
                if type(NTP_manual) != dict: self.NTPManual = NTP_manual.to_dict()
                else: self.NTPManual = NTP_manual
    
        def to_dict(self) -> dict:
            return self.__dict__