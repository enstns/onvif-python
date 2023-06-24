from enum import Enum

class PTZEnumParams:
    class PTZPresetTourOperation(Enum):
        Start = "Start"
        Stop = "Stop"
        Pause = "Pause"
        Extended = "Extended"
    class PTZPresetTourState(Enum):
        Idle = "Idle"
        Touring = "Touring"
        Paused = "Paused"
        Extended = "Extended"
    class PTZPresetTourDirection(Enum):
        forward = "Forward"
        backward = "Backward"
        extended = "Extended"
    class EFlipMode(Enum):
        off = "OFF"
        on = "ON"
        extended = "Extended"
    class ReverseMode(Enum):
        off = "OFF"
        on = "ON"
        auto = "AUTO"
        extended = "Extended"

class PTZRequestParams:
    class PTZPresetTourStatus:
        def __init__(self,state : PTZEnumParams.PTZPresetTourState,current_tour_spot = None,preset_detail = None,speed = None,stay_time = None,extension = None) -> None:
            """
            Read only parameters to indicate the status of the preset tour.
            - parameters ; 
                - State [PTZPresetTourState]
                    Indicates state of this preset tour by Idle/Touring/Paused.
                    - enum { 'Idle', 'Touring', 'Paused', 'Extended' }
                - CurrentTourSpot - optional; [PTZPresetTourSpot]
                    Indicates a tour spot currently staying.
                - PresetDetail [PTZPresetTourPresetDetail]
                    Detail definition of preset position of the tour spot.
                - Speed - optional; [PTZSpeed]
                    Optional parameter to specify Pan/Tilt and Zoom speed on moving toward this tour spot.
                - StayTime - optional; [duration]
                    Optional parameter to specify time duration of staying on this tour sport.
                - Extension - optional; [PTZPresetTourSpotExtension]
            """
            self.State = state.value
            if current_tour_spot != None : self.CurrentTourSpot = current_tour_spot
            if speed != None : self.PresetDetail = preset_detail
            if speed != None : 
                if type(speed) != dict : self.Speed = speed.to_dict()
                else : self.Speed = speed
            if stay_time != None : self.StayTime = stay_time
            if extension != None : self.Extension = extension
            
        def to_dict(self) -> dict:
            return self.__dict__

    class Vector2D:
        def __init__(self,nspace_url : str,x : float,y : float) -> None:
            self.x = x
            self.y = y 
            self.space = nspace_url

        def to_dict(self):
            return self.__dict__

    class Vector1D:
        def __init__(self,nspace_url : str,x : float) -> None:
            self.x = x
            self.space = nspace_url
            
        def to_dict(self):
            return self.__dict__

    class FloatRange:
        def __init__(self,min : float,max : float) -> None:
            """
            A range of min-max
            - requirements;
            - Min [float]
            - Max [float]
            """
            self.Min = min
            self.Max = max

        def to_dict(self):
            return self.__dict__

    class PTZSpeed:
        def __init__(self,pantilt = None,zoom = None) -> None:
            """
            Optional parameter to specify Pan/Tilt and Zoom speed on moving.
            parameters;
                - PanTilt - optional; [Vector2D]
                    Pan and tilt speed. The x component corresponds to pan and the y component to tilt. If omitted in a request, the current (if any) PanTilt movement should not be affected.
                - Zoom - optional; [Vector1D]
                    A zoom speed. If omitted in a request, the current (if any) Zoom movement should not be affected.
            """
            if pantilt != None : 
                if type(pantilt) != dict : self.PanTilt = pantilt.to_dict()
                else: self.PanTilt = pantilt
            if zoom != None : 
                if type(zoom) != dict : self.Zoom = zoom.to_dict()
                else: self.Zoom = zoom
        
        def to_dict(self) -> dict:
            return self.__dict__

    class PTZVector:
        def __init__(self,pantilt = None,zoom = None) -> None:
            """
            Optional parameter to specify Pan/Tilt and Zoom position vector.
            parameters;
                - PanTilt - optional; [Vector2D]
                    Pan and tilt position. The x component corresponds to pan and the y component to tilt. If omitted in a request, the current (if any) PanTilt movement should not be affected.
                - Zoom - optional; [Vector1D]
                    A zoom position. If omitted in a request, the current (if any) Zoom movement should not be affected.
            """
            if pantilt != None : 
                if type(pantilt) != dict: self.PanTilt = pantilt.to_dict()
                else: self.PanTilt = pantilt
            if zoom != None : 
                if type(zoom) != dict: self.Zoom = zoom.to_dict()
                else: self.Zoom = zoom

        def to_dict(self) -> dict:
            return self.__dict__

    class PresetTour:
        def __init__(self,token : str,status : 'PTZRequestParams.PTZPresetTourStatus',name = None,extension = None) -> None:
            """
            Definition a preset tour.
            - parameters ;
                - token [ReferenceToken]
                    Unique identifier of this preset tour.
                - Name - optional; [Name]
                    Readable name of the preset tour.
                - Status [PTZPresetTourStatus]
                    Read only parameters to indicate the status of the preset tour.
                - Extension - optional; [PTZPresetTourStatusExtension]
            """
            self.token = token
            if name != None : self.Name = name
            self.Status = status.to_dict()
            if extension != None : self.Extension = extension

        def to_dict(self) -> dict:
            return self.__dict__
        
    class PTZPresetTourStartingCondition:
        def __init__(self,random_preset_order : bool,recurring_time = None,recurring_duration = None,direction = None,extension = None) -> None:
            """
            Parameters to specify the detail behavior of the preset tour.
            - parameters ; 
                - RandomPresetOrder [boolean]
                    Execute presets in random order. If set to true and Direction is also present, Direction will be ignored and presets of the Tour will be recalled randomly.
                - RecurringTime - optional; [int]
                    Optional parameter to specify how many times the preset tour is recurred.
                - RecurringDuration - optional; [duration]
                    Optional parameter to specify how long time duration the preset tour is recurred.
                - Direction - optional; [PTZPresetTourDirection]
                    Optional parameter to choose which direction the preset tour goes. Forward shall be chosen in case it is omitted.
                    - enum { 'Forward', 'Backward', 'Extended' }
                - Extension - optional; [PTZPresetTourStartingConditionExtension]
            """
            self.RandomPresetOrder = random_preset_order
            if recurring_time != None: self.RecurringTime = recurring_time
            if recurring_duration != None: self.RecurringDuration = recurring_duration
            if direction != None: self.Direction = direction.value
            if extension != None: self.Extension = extension       

        def to_dict(self) -> dict:
            return self.__dict__

    class PTZPresetTourSpot:
        def __init__(self,preset_detail : str,stay_time = None,extension = None,speed = None) -> None:
            """
            A list of detail of touring spots including preset positions.
            - parameters ;
                - PresetDetail [PTZPresetTourPresetDetail]
                    Detail definition of preset position of the tour spot.
                - Speed - optional; [PTZSpeed]
                    Optional parameter to specify Pan/Tilt and Zoom speed on moving toward this tour spot.
                    - PanTilt - optional; [Vector2D]
                        Pan and tilt speed. The x component corresponds to pan and the y component to tilt. If omitted in a request, the current (if any) PanTilt movement should not be affected.
                    - Zoom - optional; [Vector1D]
                        A zoom speed. If omitted in a request, the current (if any) Zoom movement should not be affected.
                - StayTime - optional; [duration]
                    Optional parameter to specify time duration of staying on this tour sport.
                - Extension - optional; [PTZPresetTourSpotExtension]
            """
            self.PresetDetail = preset_detail
            if speed != None : self.Speed = speed.to_dict()
            if stay_time != None : self.StayTime = stay_time
            if extension != None : self.Extension = extension

        def to_dict(self) -> dict:
            return self.__dict__

    class PTZGeoLocation:
        def __init__(self,elevation : float,lat : float,lon : float) -> None:
            """
            The geolocation of the target position.
            - requirements;
                - lat
                - lon
                - elevation
            """
            self.lat = lat
            self.lon = lon 
            self.elevation = elevation

        def to_dict(self):
            return self.__dict__

    class EFlipMode:
        def __init__(self,eflip_mode = PTZEnumParams.EFlipMode) -> None:
            """
            Optional element to configure related parameters for E-Flip.
            - requirements;
                - Mode [EFlipMode]
                    Parameter to enable/disable E-Flip feature.
                    - enum { 'OFF', 'ON', 'Extended' }
            """
            self.EFlipMode = eflip_mode.value
            
        def to_dict(self):
            return self.__dict__

    class Reverse:
        def __init__(self,reverse_mode = PTZEnumParams.ReverseMode) -> None:
            """
            Optional element to configure related parameters for reversing of PT Control Direction.
            - requirements;
                - Mode [ReverseMode]
                    Parameter to enable/disable Reverse feature.
                    - enum { 'OFF', 'ON', 'AUTO', 'Extended' }
            """
            self.Mode = reverse_mode.value
            
        def to_dict(self):
            return self.__dict__

    class PTControlDirection:
        def __init__(self,eflip = None,reverse = None,extension = None) -> None:
            """
            Optional element to configure PT Control Direction related features.
            - requirements;
                - EFlip - optional; [EFlip]
                    Optional element to configure related parameters for E-Flip.
                - Reverse - optional; [Reverse]
                    Optional element to configure related parameters for reversing of PT Control Direction.
                - Extension - optional; [PTControlDirectionExtension]
            """
            if eflip != None: 
                if type(eflip) != dict: self.EFlip = eflip.to_dict()
                else: self.EFlip = eflip
            if reverse != None: 
                if type(reverse) != dict: self.Reverse = reverse.to_dict()
                else: self.Reverse = reverse
            if extension != None: self.Extension = extension
            
        def to_dict(self):
            return self.__dict__

    class PTZConfigurationExtension:
        def __init__(self,ptz_contol_direction = None,extension = None) -> None:
            """
            - requirements;
                - PTControlDirection - optional; [PTControlDirection]
                    Optional element to configure PT Control Direction related features.
                - Extension - optional; [PTZConfigurationExtension2]
            """
            if ptz_contol_direction != None: 
                if type(ptz_contol_direction) != dict: self.PTControlDirection = ptz_contol_direction.to_dict()
                else: self.PTControlDirection = ptz_contol_direction
            if extension != None: 
                if type(extension) != dict: self.Extension = extension.to_dict()
                else: self.Extension = extension

        def to_dict(self):
            return self.__dict__

    class Space2DDescription:
        def __init__(self,uri : str,xrange : 'PTZRequestParams.FloatRange',yrange : 'PTZRequestParams.FloatRange') -> None:
            """
            A range of x-y limits.
            - requirements:
                - URI [anyURI]
                    A URI of coordinate systems.
                - XRange [FloatRange]
                    A range of x-axis.
                - YRange [FloatRange]
                    A range of y-axis.
            """
            self.URI = uri
            self.XRange = xrange.to_dict()
            self.YRange = yrange.to_dict()

        def to_dict(self):
            return self.__dict__

    class Space1DDescription:
        def __init__(self,uri : str,xrange : 'PTZRequestParams.FloatRange') -> None:
            """
            A range of x-y limits.
            - requirements:
                - URI [anyURI]
                    A URI of coordinate systems.
                - XRange [FloatRange]
                    A range of x-axis.
            """
            self.URI = uri
            self.XRange = xrange.to_dict()

        def to_dict(self):
            return self.__dict__

    class PanTiltLimits:
        def __init__(self,range : 'PTZRequestParams.Space2DDescription') -> None:
            """
            - requirements;
                - Range [Space2DDescription]
            """
            self.Range = range.to_dict()

        def to_dict(self):
            return self.__dict__

    class ZoomLimits:
        def __init__(self,range : 'PTZRequestParams.Space1DDescription') -> None:
            """
            The Zoom limits element should be present for a PTZ Node that supports absolute zoom. If the element is present it signals the supports for configurable Zoom limits. If limits are enabled the zoom movements shall always stay within the specified range. The Zoom limits are disabled by settings the limits to -INF and +INF. 
            - requirements;
                - Range [Space2DDescription]
            """
            self.Range = range.to_dict()

        def to_dict(self):
            return self.__dict__

    class PTZConfiguration:
        def __init__(self,token : str,name : str,usecount : int,node_token : str,move_ramp = None,preset_ramp = None,preset_tour_ramp = None,\
                default_absolute_panttilt_position_space = None,default_absolute_zoom_position_space = None,\
                default_relative_panttilt_translation_space = None,default_relative_zoom_translation_space = None,\
                default_continuous_panttilt_velocity_space = None,default_continuous_zoom_velocity_space = None,\
                default_ptz_speed = None,default_ptz_timeout = None,pantilt_limits = None,zoom_limits = None,extension = None) -> None:
            """
            - requirements;
                - token - required; [ReferenceToken]
                    Token that uniquely references this configuration. Length up to 64 characters.
                - Name [Name]
                    User readable name. Length up to 64 characters.
                - UseCount [int]
                    Number of internal references currently using this configuration.
                    This informational parameter is read-only. Deprecated for Media2 Service.
                - MoveRamp [int]
                    The optional acceleration ramp used by the device when moving.
                - PresetRamp [int]
                    The optional acceleration ramp used by the device when recalling presets.
                - PresetTourRamp [int]
                    The optional acceleration ramp used by the device when executing PresetTours.
                - NodeToken [ReferenceToken]
                    A mandatory reference to the PTZ Node that the PTZ Configuration belongs to.
                - DefaultAbsolutePantTiltPositionSpace - optional; [anyURI]
                    If the PTZ Node supports absolute Pan/Tilt movements, it shall specify one Absolute Pan/Tilt Position Space as default.
                - DefaultAbsoluteZoomPositionSpace - optional; [anyURI]
                    If the PTZ Node supports absolute zoom movements, it shall specify one Absolute Zoom Position Space as default.
                - DefaultRelativePanTiltTranslationSpace - optional; [anyURI]
                    If the PTZ Node supports relative Pan/Tilt movements, it shall specify one RelativePan/Tilt Translation Space as default.
                - DefaultRelativeZoomTranslationSpace - optional; [anyURI]
                    If the PTZ Node supports relative zoom movements, it shall specify one Relative Zoom Translation Space as default.
                - DefaultContinuousPanTiltVelocitySpace - optional; [anyURI]
                    If the PTZ Node supports continuous Pan/Tilt movements, it shall specify one Continuous Pan/Tilt Velocity Space as default.
                - DefaultContinuousZoomVelocitySpace - optional; [anyURI]
                    If the PTZ Node supports continuous zoom movements, it shall specify one Continuous Zoom Velocity Space as default.
                - DefaultPTZSpeed - optional; [PTZSpeed]
                    If the PTZ Node supports absolute or relative PTZ movements, it shall specify corresponding default Pan/Tilt and Zoom speeds. 
                - DefaultPTZTimeout - optional; [duration]
                    If the PTZ Node supports continuous movements, it shall specify a default timeout, after which the movement stops.
                - PanTiltLimits - optional; [PanTiltLimits]
                    The Pan/Tilt limits element should be present for a PTZ Node that supports an absolute Pan/Tilt. If the element is present it signals the support for configurable Pan/Tilt limits. If limits are enabled, the Pan/Tilt movements shall always stay within the specified range. The Pan/Tilt limits are disabled by setting the limits to –INF or +INF.
                - ZoomLimits - optional; [ZoomLimits]
                    The Zoom limits element should be present for a PTZ Node that supports absolute zoom. If the element is present it signals the supports for configurable Zoom limits. If limits are enabled the zoom movements shall always stay within the specified range. The Zoom limits are disabled by settings the limits to -INF and +INF.
                - Extension - optional; [PTZConfigurationExtension]
            """
            self.token = token
            self.Name = name
            self.UseCount = usecount
            if move_ramp != None: self.MoveRamp = move_ramp
            if preset_ramp != None:self.PresetRamp = preset_ramp
            if preset_tour_ramp != None:self.PresetTourRamp = preset_tour_ramp
            self.NodeToken = node_token
            if default_absolute_panttilt_position_space != None: self.DefaultAbsolutePantTiltPositionSpace = default_absolute_panttilt_position_space
            if default_absolute_zoom_position_space != None: self.DefaultAbsoluteZoomPositionSpace = default_absolute_zoom_position_space
            if default_relative_panttilt_translation_space != None: self.DefaultRelativePanTiltTranslationSpace = default_relative_panttilt_translation_space
            if default_relative_zoom_translation_space != None: self.DefaultRelativeZoomTranslationSpace = default_relative_zoom_translation_space
            if default_continuous_panttilt_velocity_space != None: self.DefaultContinuousPanTiltVelocitySpace = default_continuous_panttilt_velocity_space
            if default_continuous_zoom_velocity_space != None: self.DefaultContinuousZoomVelocitySpace = default_continuous_zoom_velocity_space
            if default_ptz_speed != None:
                if type(default_ptz_speed) != dict: self.DefaultPTZSpeed = default_ptz_speed.to_dict()
                else: self.DefaultPTZSpeed = default_ptz_speed
            if default_ptz_timeout != None: self.DefaultPTZTimeout = default_ptz_timeout
            if pantilt_limits != None:
                if type(pantilt_limits) != dict: self.PanTiltLimits = pantilt_limits.to_dict()
                else: self.PanTiltLimits = pantilt_limits
            if zoom_limits != None:
                if type(zoom_limits) != dict: self.ZoomLimits = zoom_limits.to_dict()
                else: self.ZoomLimits = zoom_limits
            if extension != None: 
                if type(extension) != dict: self.Extension = extension.to_dict()
                else: self.Extension = extension

        def to_dict(self):
            return self.__dict__
