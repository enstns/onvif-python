from enum import Enum

class MediaEnumParams:
    class OSDType(Enum):
        Text = "Text"
        Image = "Image"
        Extended = "Extended"
    
    class OSDPositionType(Enum):
        UpperLeft = "UpperLeft"
        UpperRight = "UpperRight"
        LowerLeft = "LowerLeft"
        LowerRight = "LowerRight"
    
    class OSDTextStringType(Enum):
        Plain = "Plain"
        Date = "Date"
        Time = "Time"
        DateAndTime = "DateAndTime"

    class StreamType(Enum):
        Unicast = 'RTP-Unicast'
        Multicast = 'RTP-Multicast' 
    
    class TransportProtocol(Enum):
        UDP = 'UDP'
        TCP = 'TCP' 
        RTSP = 'RTSP' 
        HTTP = 'HTTP' 

class MediaRequestParams:
    class Vector:
        pass

    class OSDColor:
        def __init__(self,color : str,transparent = 0) -> None:
            """
            Font color of the text.
            - reqirements;
                - Transparent - optional; [int]
                - Color [Color] - Optional list of supported colors can be found with GetOSDOptions method.
            """
            if transparent != None: self.Transparent = transparent
            self.Color = color
        
        def to_dict(self) -> dict:
            return self.__dict__

    class OSDPosConfiguration:
        def __init__(self,osd_pos_type : MediaEnumParams.OSDPositionType,pos = None,extension = None) -> None:
            """
            Position configuration of OSD.
            - reqirements;
                - Type [string] [OSDPositionType]
                    For OSD position type, following are the pre-defined:
                    - UpperLeft
                    - UpperRight
                    - LowerLeft
                    - LowerRight
                    - Custom
                - Pos - optional; [Vector]
                - Extension - optional; [OSDPosConfigurationExtension]
            """
            self.Type = osd_pos_type.value
            if extension != None : self.Extension = extension
            if pos != None : 
                if type(pos) != dict : self.Pos = pos.to_dict()
                else: self.Pos = pos
            
        def to_dict(self) -> dict:
            return self.__dict__

    class OSDTextConfiguration:
        def __init__(self,osd_text_type : MediaEnumParams.OSDTextStringType,plain_text = None,extension = None,background_color = None,font_size = None,font_color = None,time_format = None,date_format = None,is_persistent_text = None) -> None:
            """
            Text configuration of OSD. It shall be present when the value of Type field is Text.
            - reqirements;
                - IsPersistentText - optional; [boolean]
                    This flag is applicable for Type Plain and defaults to true. When set to false the PlainText content will not be persistent across device reboots.
                - Type [OSDTextStringType]
                    The following OSD Text Type are defined:
                    - Plain - The Plain type means the OSD is shown as a text string which defined in the "PlainText" item.
                    - Date - The Date type means the OSD is shown as a date, format of which should be present in the "DateFormat" item.
                    - Time - The Time type means the OSD is shown as a time, format of which should be present in the "TimeFormat" item.
                    - DateAndTime - The DateAndTime type means the OSD is shown as date and time, format of which should be present in the "DateFormat" and the "TimeFormat" item.
                - DateFormat - optional; [string]
                    List of supported OSD date formats. This element shall be present when the value of Type field has Date or DateAndTime. The following DateFormat are defined:
                    - M/d/yyyy - e.g. 3/6/2013
                    - MM/dd/yyyy - e.g. 03/06/2013
                    - dd/MM/yyyy - e.g. 06/03/2013
                    - yyyy/MM/dd - e.g. 2013/03/06
                    - yyyy-MM-dd - e.g. 2013-06-03
                    - dddd, MMMM dd, yyyy - e.g. Wednesday, March 06, 2013
                    - MMMM dd, yyyy - e.g. March 06, 2013
                    - dd MMMM, yyyy - e.g. 06 March, 2013
                - TimeFormat - optional; [string]
                    List of supported OSD time formats. This element shall be present when the value of Type field has Time or DateAndTime. The following TimeFormat are defined:
                    - h:mm:ss tt - e.g. 2:14:21 PM
                    - hh:mm:ss tt - e.g. 02:14:21 PM
                    - H:mm:ss - e.g. 14:14:21
                    - HH:mm:ss - e.g. 14:14:21
                - FontSize - optional; [int]
                    Font size of the text in pt.
                - FontColor - optional; [OSDColor]
                    Font color of the text.
                - BackgroundColor - optional; [OSDColor]
                    Background color of the text.
                - PlainText - optional; [string]
                    The content of text to be displayed.  
                - Extension - optional; [OSDTextConfigurationExtension]
            """
            self.Type = osd_text_type.value
            if is_persistent_text != None : self.IsPersistentText = is_persistent_text
            if date_format != None : self.DateFormat = date_format
            if time_format != None : self.TimeFormat = time_format
            if font_size != None : self.FontSize = font_size
            if plain_text != None : self.PlainText = plain_text
            if font_color != None : self.FontColor = font_color
            if background_color != None : self.BackgroundColor = background_color
            if extension != None : self.Extension = extension
            
        def to_dict(self) -> dict:
            return self.__dict__
        
    class OSDImgConfiguration:
        def __init__(self,image_path : str,extension = None) -> None:
            """
            Image configuration of OSD. It shall be present when the value of Type field is Image
            - reqirements;
                - ImgPath [anyURI]
                    The URI of the image which to be displayed.
                - Extension - optional; [OSDImgConfigurationExtension]
                
            """
            self.ImgPath = image_path
            if extension != None : self.Extension = extension
            
        def to_dict(self) -> dict:
            return self.__dict__
    
    class OSDConfiguration:
        def __init__(self, token : str, videosource_configuration_token : str,osd_type : MediaEnumParams.OSDType,position : 'MediaRequestParams.OSDPosConfiguration',text_string = None,image = None,extension = None) -> None:
            """
            - reqirements;
                - OSD [OSDConfiguration]
                    Contain the initial OSD configuration for create.
                    - token - required; [ReferenceToken]
                        Unique identifier referencing the physical entity.
                    - VideoSourceConfigurationToken [OSDReference]
                        Reference to the video source configuration.
                    - Type [OSDType]
                        Type of OSD. enum { 'Text', 'Image', 'Extended' }
                    - Position [OSDPosConfiguration]
                        Position configuration of OSD.
                    - TextString - optional; [OSDTextConfiguration]
                        Text configuration of OSD. It shall be present when the value of Type field is Text.
                    - Image - optional; [OSDImgConfiguration]
                        Image configuration of OSD. It shall be present when the value of Type field is Image
                    - Extension - optional; [OSDConfigurationExtension]
            """
            self.token = token
            self.VideoSourceConfigurationToken = videosource_configuration_token
            self.Type = osd_type.value
            if type(position) != dict : self.Position = position.to_dict()
            else: self.Position = position
            if text_string != None : 
                if type(text_string) != dict : self.TextString = text_string.to_dict()
                else: self.TextString = text_string
            if image != None : 
                if type(image) != dict : self.Image = image.to_dict()
                else: self.Image = image
            if extension != None: self.Extension = extension

        def to_dict(self):
            return self.__dict__

    class Transport:
        def __init__(self,protocol : MediaEnumParams.TransportProtocol,tunnel = None) -> None:
            """
            Transport [Transport]
            - reqirements;
                - Protocol [TransportProtocol] : transport_protocol [TransportProtocol],
                    Defines the network protocol for streaming, either UDP=RTP/UDP, RTSP=RTP/RTSP/TCP or HTTP=RTP/RTSP/HTTP/TCP
                    enum { 'UDP', 'TCP', 'RTSP', 'HTTP' }
                - Tunnel - optional; [Transport] :
                    Optional element to describe further tunnel options. This element is normally not needed
                    ... is recursive                 
            """
            self.Protocol = protocol.value
            if tunnel != None : 
                if type(tunnel) != dict: self.Tunnel = tunnel.to_dict()
                else: self.Tunnel = tunnel
            
        def to_dict(self) -> dict:
            return self.__dict__   

    class StreamSetup:
        def __init__(self,stream : MediaEnumParams.StreamType,transport : 'MediaRequestParams.Transport') -> None:
            """
            Stream Setup that should be used with the uri
            - reqirements;
                - Stream [StreamType] : stream [StreamType] ,
                    Defines if a multicast or unicast stream is requested
                    enum { 'RTP-Unicast', 'RTP-Multicast' }
                - Transport [Transport]
            """
            self.Stream = stream.value
            self.Transport = transport.to_dict()
            
        def to_dict(self) -> dict:
            return self.__dict__
    