from enum import Enum

class DeviceEnumParams:
    class UserLevel(Enum):
        """UserLevel
        - enum { 'Administrator', 'Operator', 'User', 'Anonymous', 'Extended' }
        """
        Administrator = "Administrator"
        Operator = "Operator"
        User = "User"
        Anonymous = "Anonymous"
        Extended = "Extended"
    class DiscoveryMode(Enum):
        """DiscoveryMode
        - enum { 'Discoverable', 'NonDiscoverable' }
        """
        Discoverable = "Discoverable"
        NonDiscoverable = "NonDiscoverable"
    class SetDateTimeType(Enum):
        """SetDateTimeType
        - enum { 'Manual', 'NTP' }
        """
        Manual = "Manual"
        NTP = "NTP"
    class NetworkHostType(Enum):
        """Network host type: IPv4, IPv6 or DNS.
        - enum { 'IPv4', 'IPv6', 'DNS' }
        """
        IPv4 = "IPv4"
        IPv6 = "IPv6"
        DNS = "DNS"

class DeviceRequestParams:
    class User:
        def __init__(self,username : str,userlevel : DeviceEnumParams.UserLevel,password = None,extension = None) -> None:
            """
            Creates new device users and corresponding credentials. Each user entry includes: username, password and user level. Either all users are created successfully or a fault message MUST be returned without creating any user. If trying to create several users with exactly the same username the request is rejected and no users are created. If password is missing, then fault message Too weak password is returned.
            - reqirements;
                - Username [string]
                    Username string.
                - Password - optional; [string]
                    Password string.
                - UserLevel [UserLevel]
                    User level string. - enum { 'Administrator', 'Operator', 'User', 'Anonymous', 'Extended' }  
                - Extension - optional; [UserExtension]
            """
            self.Username = username
            if password != None: self.Password = password
            self.UserLevel = userlevel.value
            if extension != None: self.Extension = extension
        
        def to_dict(self) -> dict:
            return self.__dict__
        
    class TimeZone:
        def __init__(self,tz : str) -> None:
            """
            The time zone in POSIX 1003.1 format
            - reqirements;
                - TZ [token]
                    "Posix timezone string."
            """
            self.TZ = tz
        
        def to_dict(self) -> dict:
            return self.__dict__ 

    class Time:
        def __init__(self,hour : int,minute : int,second :int) -> None:
            """
            Time [Time]
            - reqirements;
                - Hour [int]
                    Range is 0 to 23.
                - Minute [int]
                    Range is 0 to 59.
                - Second [int]
                    Range is 0 to 61 (typically 59).
            """
            self.Hour = hour
            self.Minute = minute
            self.Second = second
        
        def to_dict(self) -> dict:
            return self.__dict__ 

    class Date:
        def __init__(self,year : int,month : int,day :int) -> None:
            """
            Date [Date]
            - reqirements;
                - Year [int]
                - Month [int]
                    Range is 1 to 12.
                - Day [int]
                    Range is 1 to 31.
            """
            self.Year = year
            self.Month = month
            self.Day = day
        
        def to_dict(self) -> dict:
            return self.__dict__ 

    class DateTime:
        def __init__(self,time : 'DeviceRequestParams.Time',date : 'DeviceRequestParams.Date') -> None:
            """
            Date and time in UTC. If time is obtained via NTP, UTCDateTime has no meaning
            - reqirements;
                - Time [Time]
                - Date [Date]
            """
            if type(time) != dict: self.Time = time.to_dict()
            else: self.Time = time
            if type(date) != dict: self.Date = date.to_dict()
            else: self.Date = date
        
        def to_dict(self) -> dict:
            return self.__dict__ 

    class NetworkHost:
        def __init__(self,network_host_type : DeviceEnumParams.NetworkHostType,IPv4Address = None, IPv6Address = None,DNSname = None,extension = None) -> None:
            """
            Manual NTP settings.
            - reqirements;
                - network_host_type [NetworkHostType]
                    Network host type: IPv4, IPv6 or DNS.
                - IPv4Address - optional; [IPv4Address]
                    IPv4 address.
                - IPv6Address - optional; [IPv6Address]
                    IPv6 address.
                - DNSname - optional; [DNSName]
                    DNS name.
                - extension - optional; [NetworkHostExtension]
            """
            self.Type = network_host_type.value
            if IPv4Address != None: self.IPv4Address = IPv4Address
            if IPv6Address != None: self.IPv6Address = IPv6Address
            if DNSname != None: self.DNSname = DNSname
            if extension != None: self.Extension = extension
        
        def to_dict(self) -> dict:
            return self.__dict__ 




