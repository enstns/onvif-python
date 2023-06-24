from lib.params.media_request_params import MediaRequestParams

class MediaRequestMessages:
    # TODO: Create CreateOSD request message
    class CreateOSDMessage:
        def __init__(self, osd : MediaRequestParams.OSDConfiguration) -> None:
            """
            Create the OSD.
            - reqirements;
                - OSD [OSDConfiguration] 
                    Contain the initial OSD configuration for create.
            """
            if type(osd) != dict : self.OSD = osd.to_dict()
            else: self.OSD = osd
        
        def to_dict(self):
            return self.__dict__
        
    # TODO: Create GetStreamUri request message
    class GetStreamUriMessage:
        def __init__(self,stream_setup : MediaRequestParams.StreamSetup,profile_token : str) -> None:
            """
            This operation requests a URI that can be used to initiate a live media stream using RTSP as the control protocol. The returned URI shall remain valid indefinitely even if the profile is changed. The ValidUntilConnect, ValidUntilReboot and Timeout Parameter shall be set accordingly (ValidUntilConnect=false, ValidUntilReboot=false, timeout=PT0S).

            The correct syntax for the StreamSetup element for these media stream setups defined in 5.1.1 of the streaming specification are as follows:
                1 - RTP unicast over UDP: StreamType = "RTP_unicast", TransportProtocol = "UDP"
                2 - RTP over RTSP over HTTP over TCP: StreamType = "RTP_unicast", TransportProtocol = "HTTP"
                3 - RTP over RTSP over TCP: StreamType = "RTP_unicast", TransportProtocol = "RTSP"

            If a multicast stream is requested at least one of VideoEncoderConfiguration, AudioEncoderConfiguration and MetadataConfiguration shall have a valid multicast setting.

            For full compatibility with other ONVIF services a device should not generate Uris longer than 128 octets.
            - reqirements;
                - StreamSetup [StreamSetup]
                    Stream Setup that should be used with the uri
                - ProfileToken [ReferenceToken] : profile_token [str],
                    The ProfileToken element indicates the media profile to use and will define the configuration of the content of the stream.
            """
            self.StreamSetup = stream_setup.to_dict()
            self.ProfileToken = profile_token

        def to_dict(self) -> dict:
            return self.__dict__
   