from lib.params.image_request_params import ImageRequestParams

class ImageRequestMessages:
    # TODO: Create Move request message
    class MoveMessage:
        def __init__(self, focus : ImageRequestParams.FocusMove,vs_token : str) -> None:
            """
            The Move command moves the focus lens in an absolute, a relative or in a continuous manner from its current position. 
            The speed argument is optional for absolute and relative control, but required for continuous. 
            If no speed argument is used, the default speed is used. Focus adjustments through this operation will turn off the autofocus. A device with support for remote focus control should support absolute, relative or continuous control through the Move operation. 
            The supported MoveOpions are signalled via the GetMoveOptions command. 
            At least one focus control capability is required for this operation to be functional.
            - reqirements;
                - focus [FocusMove] 
                    FocusMove
                - vs_token : [string] 
                    Reference to the VideoSource for the requested move (focus) operation.
            """
            self.VideoSourceToken = vs_token
            if type(focus) != dict : self.Focus = focus.to_dict()
            else: self.Focus = focus
        
        def to_dict(self):
            return self.__dict__
        
    # TODO: Create SetImagingSettings request message
    class SetImagingSettingsMessage:
        def __init__(self, imaging_settings : ImageRequestParams.ImagingSettings20,vs_token : str,force_persistence = None) -> None:
            """
            Set the ImagingConfiguration for the requested VideoSource.
            - reqirements;
                - VideoSourceToken [ReferenceToken]
                - ImagingSettings [ImagingSettings20]
                - ForcePersistence - optional; [boolean]
            """
            self.VideoSourceToken = vs_token
            self.ImagingSettings = imaging_settings.to_dict()
            if force_persistence != None : self.ForcePersistence = force_persistence

        def to_dict(self):
            return self.__dict__
        