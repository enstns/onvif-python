from lib.params.ptz_request_params import PTZRequestParams
 
class PTZRequestMessages:
    class ModifyPresetTourRequestMessage:
        def __init__(self,profile_token : str,preset_tour : PTZRequestParams.PresetTour,auto_start : bool,starting_condition : PTZRequestParams.PTZPresetTourStartingCondition,tour_spot = None) -> None:
            """
            Operation to modify a preset tour for the selected media profile.
            - reqirements;
                - ProfileToken [ReferenceToken]
                - PresetTour [PresetTour]
                - AutoStart [boolean]
                    Auto Start flag of the preset tour. True allows the preset tour to be activated always.
                - StartingCondition [PTZPresetTourStartingCondition]
                    Parameters to specify the detail behavior of the preset tour.
                - TourSpot - optional, unbounded; [PTZPresetTourSpot]
                    A list of detail of touring spots including preset positions.
                - Extension - optional; [PTZPresetTourExtension]
            """
            self.ProfileToken = profile_token
            self.PresetTour = preset_tour.to_dict()
            self.AutoStart = auto_start
            self.StartingCondition = starting_condition.to_dict()
            if tour_spot != None: 
                if type(tour_spot) != dict : self.TourSpot = tour_spot.to_dict()
                else: self.TourSpot = tour_spot

        def to_dict(self) -> dict:
            return self.__dict__
        
    class AbsoluteMoveRequestMessage:
        def __init__(self,profile_token : str,position : PTZRequestParams.PTZVector,speed = None) -> None:
            """
            Operation to move pan,tilt or zoom to a absolute destination.
            The speed argument is optional. If an x/y speed value is given it is up to the device to either use the x value as absolute resoluting speed vector or to map x and y to the component speed. If the speed argument is omitted, the default speed set by the PTZConfiguration will be used.
            - reqirements;
                - ProfileToken [ReferenceToken]
                    A reference to the MediaProfile.
                - Position [PTZVector]
                    A Position vector specifying the absolute target position.
                - Speed - optional; [PTZSpeed]
                    An optional Speed.
            """
            self.ProfileToken = profile_token
            self.Position = position.to_dict()
            if speed != None :
                if type(speed) != dict: self.Speed = speed.to_dict()
                else: self.Speed = speed

        def to_dict(self) -> dict:
            return self.__dict__
        
    class ContinuousMoveRequestMessage:
        def __init__(self,profile_token : str,velocity : PTZRequestParams.PTZSpeed,timeout = None) -> None:
            """
            Operation for continuous Pan/Tilt and Zoom movements. The operation is supported if the PTZNode supports at least one continuous Pan/Tilt or Zoom space. If the space argument is omitted, the default space set by the PTZConfiguration will be used.
            - requirements;
                - ProfileToken [ReferenceToken]
                    A reference to the MediaProfile.
                - Velocity [PTZSpeed]
                    A Velocity vector specifying the velocity of pan, tilt and zoom.
                - Timeout - optional; [duration]
                    An optional Timeout parameter.
            """
            self.ProfileToken = profile_token
            self.Velocity = velocity.to_dict()
            if timeout != None : self.Timeout = timeout

        def to_dict(self) -> dict:
            return self.__dict__

    class RelativeMoveRequestMessage:
        def __init__(self,profile_token : str,translation : PTZRequestParams.PTZVector,speed = None) -> None:
            """
            Operation for Relative Pan/Tilt and Zoom Move. The operation is supported if the PTZNode supports at least one relative Pan/Tilt or Zoom space.
            - requirements;
                - ProfileToken [ReferenceToken]
                    A reference to the MediaProfile.
                - Translation [PTZVector]
                    A positional Translation relative to the current position
                - Speed - optional; [PTZSpeed]
                    An optional Speed parameter.
            """
            self.ProfileToken = profile_token
            self.Translation = translation.to_dict()
            if speed != None : 
                if type(speed) != dict : self.Speed = speed.to_dict()
                else: self.Speed = speed

        def to_dict(self) -> dict:
            return self.__dict__

    class GeoMoveRequestMessage:
        def __init__(self,profile_token : str,target : PTZRequestParams.PTZGeoLocation,speed = None,area_height = None,area_width = None) -> None:
            """
            Operation to move pan,tilt or zoom to point to a destination based on the geolocation of the target.
            - requirements;
                - ProfileToken [ReferenceToken]
                    A reference to the MediaProfile.
                - Target [GeoLocation]
                    The geolocation of the target position. 
                - Speed - optional; [PTZSpeed]
                    An optional Speed parameter.
                - AreaHeight - optional; [float]
                    An optional indication of the height of the target/area.
                - AreaWidth - optional; [float]
                    An optional indication of the width of the target/area.
            """
            self.ProfileToken = profile_token
            self.Target = target.to_dict()
            if speed != None : 
                if type(speed) != dict : self.Speed = speed.to_dict()
                else: self.Speed = speed
            if area_height != None : self.AreaHeight = area_height
            if area_width != None : self.AreaWidth = area_width

        def to_dict(self) -> dict:
            return self.__dict__
        
    class MoveAndStartTrackingRequestMessage:
        def __init__(self,profile_token : str,preset_token = None ,geo_location = None, target_position = None,speed = None,object_id = None) -> None:
            """
            Operation to move pan,tilt or zoom to point to a destination based on the geolocation of the target.
            - requirements;
                - ProfileToken [ReferenceToken]
                    A reference to the MediaProfile where the operation should take place.
                - PresetToken - optional; [ReferenceToken]
                    A preset token.
                - GeoLocation - optional; [GeoLocation]
                    The geolocation of the target position.
                - TargetPosition - optional; [PTZVector]
                    A Position vector specifying the absolute target position.
                - Speed - optional; [PTZSpeed]
                    Speed vector specifying the velocity of pan, tilt and zoom.
                - ObjectID - optional; [integer]
                    Object ID of the object to track. 
            """
            self.ProfileToken = profile_token
            if preset_token != None : self.PresetToken = preset_token
            if geo_location != None : 
                if type(geo_location) != dict : self.GeoLocation = geo_location.to_dict()
                else: self.GeoLocation = geo_location
            if target_position != None : 
                if type(target_position) != dict : self.TargetPosition = target_position.to_dict()
                else: self.TargetPosition = target_position
            if speed != None : 
                if type(speed) != dict : self.Speed = speed.to_dict()
                else: self.Speed = speed
            if object_id != None : self.ObjectID = object_id

        def to_dict(self) -> dict:
            return self.__dict__

    class SetConfigurationRequestMessage:
        def __init__(self,ptz_configuration : PTZRequestParams.PTZConfiguration,force_persistence : bool) -> None:
            """
             Set/update a existing PTZConfiguration on the device. 
            - requirements;
                - PTZConfiguration [PTZConfiguration]
                - ForcePersistence [boolean]
                    Flag that makes configuration persistent. Example: User wants the configuration to exist after reboot. 
            """
            self.PTZConfiguration = ptz_configuration.to_dict()
            self.ForcePersistence = force_persistence

        def to_dict(self) -> dict:
            return self.__dict__
