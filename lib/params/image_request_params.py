from enum import Enum

class ImagesEnumParams:
    class ImageStabilizationMode(Enum):
        """- enum { 'OFF', 'ON', 'AUTO', 'Extended' }"""
        OFF = "OFF"
        ON = "ON"
        AUTO = "AUTO" 
        Extended = "Extended" 
    class WhiteBalanceMode(Enum):
        """- enum { 'AUTO', 'MANUAL' }"""
        MANUAL = "MANUAL"
        AUTO = "AUTO" 
    class WideDynamicMode(Enum):
        """- enum { 'OFF', 'ON' }"""
        OFF = "OFF"
        ON = "ON" 
    class IrCutFilterMode(Enum):
        OFF = "OFF"
        ON = "ON"
        AUTO = "AUTO" 
    class AutoFocusMode(Enum):
        """
        Note: for devices supporting both manual and auto operation at the same time manual operation may be supported even if the Mode parameter is set to Auto.
        - AUTO - The device automatically adjusts focus.
        - MANUAL - The device does not automatically adjust focus.
            - enum { 'AUTO', 'MANUAL' }
        """
        MANUAL = "MANUAL"
        AUTO = "AUTO" 
    class ExposureMode(Enum):
        """
        Auto – Enabled the exposure algorithm on the device. 
        Manual – Disabled exposure algorithm on the device.
            enum { 'AUTO', 'MANUAL' }
        """
        MANUAL = "MANUAL"
        AUTO = "AUTO" 
    class BacklightCompensationMode(Enum):
        OFF = "OFF"
        ON = "ON" 
    class ExposurePriority(Enum):
        """- enum { 'LowNoise', 'FrameRate' }"""
        LowNoise = "LowNoise"
        FrameRate = "FrameRate" 
    class ToneCompensationMode(Enum):
        OFF = "OFF"
        ON = "ON" 
        AUTO = "AUTO" 
    class DefoggingMode(Enum):
        OFF = "OFF"
        ON = "ON" 
        AUTO = "AUTO"

class ImageRequestParams:
    class AbsoluteFocus:
        def __init__(self,position : float,speed = None) -> None:
            """
            Parameters for the absolute focus control.
            - reqirements;
                - Position [float]
                    Position parameter for the absolute focus control.
                - Speed - optional; [float]
                    Speed parameter for the absolute focus control.
            """
            self.Position = position
            if speed != None: self.Speed = speed

        def to_dict(self) -> dict:
            return self.__dict__

    class RelativeFocus:
        def __init__(self,distance : float,speed = None) -> None:
            """
            Parameters for the relative focus control.
            - reqirements;
                - Distance [float]
                    Distance parameter for the relative focus control.
                - Speed - optional; [float]
                    Speed parameter for the relative focus control.
            """
            self.Distance = distance
            if speed != None: self.Speed = speed

        def to_dict(self) -> dict:
            return self.__dict__

    class ContinuousFocus:
        def __init__(self,speed : float) -> None:
            """
            Parameter for the continuous focus control.
            - reqirements;
                - Speed [float]
                    Speed parameter for the Continuous focus control.
            """
            self.Speed = speed

        def to_dict(self) -> dict:
            return self.__dict__

    class FocusMove:
        def __init__(self,absolute = None,relative = None,continuous = None) -> None:
            """
            Content of the requested move (focus) operation.
            - reqirements;
                - Absolute - optional; [AbsoluteFocus]
                - Relative - optional; [RelativeFocus]
                - Continuous - optional; [ContinuousFocus]
            """
            if absolute != None:
                if type(absolute) != dict: self.Absolute = absolute.to_dict()
                else: self.Absolute = absolute
            if relative != None:
                if type(relative) != dict: self.Relative = relative.to_dict()
                else: self.Relative = relative
            if continuous != None:
                if type(continuous) != dict: self.Continuous = continuous.to_dict()
                else: self.Continuous = continuous
        
        def to_dict(self) -> dict:
            return self.__dict__
        
    class BacklightCompensation20:
        def __init__(self,mode : ImagesEnumParams.BacklightCompensationMode,level = None) -> None:
            """
            Enabled/disabled BLC mode (on/off).
            - reqirements;
                - Mode [BacklightCompensationMode]
                    Backlight compensation mode (on/off).
                    OFF: Backlight compensation is disabled.
                    ON: Backlight compensation is enabled.
                - Level - optional; [float]
                    Optional level parameter (unit unspecified).
            """
            self.Mode = mode.value
            if level != None : self.Level = level
        
        def to_dict(self) -> dict:
            return self.__dict__

    class Exposure20:
        def __init__(self,mode : ImagesEnumParams.ExposureMode,priority = None,window = None,\
                    min_exposure_time = None,max_exposure_time = None,min_gain = None,max_gain = None,\
                        min_iris = None,max_iris = None,exposure_time = None,iris = None,gain = None) -> None:
            """
            Exposure mode of the device.
            - reqirements;
                - Mode [ExposureMode] 
                    Exposure Mode - enum { 'AUTO', 'MANUAL' }
                - Priority - optional; [ExposurePriority]
                    The exposure priority mode (low noise/framerate). - enum { 'LowNoise', 'FrameRate' }
                - Window - optional; [Rectangle]
                    Rectangular exposure mask.
                - MinExposureTime - optional; [float]
                    Minimum value of exposure time range allowed to be used by the algorithm.
                - MaxExposureTime - optional; [float]
                    Maximum value of exposure time range allowed to be used by the algorithm.
                - MinGain - optional; [float]
                    Minimum value of the sensor gain range that is allowed to be used by the algorithm.
                - MaxGain - optional; [float]
                    Maximum value of the sensor gain range that is allowed to be used by the algorithm.
                - MinIris - optional; [float]
                    Minimum value of the iris range allowed to be used by the algorithm. 0dB maps to a fully opened iris and positive values map to higher attenuation.
                - MaxIris - optional; [float]
                    Maximum value of the iris range allowed to be used by the algorithm. 0dB maps to a fully opened iris and positive values map to higher attenuation.
                - ExposureTime - optional; [float]
                    The fixed exposure time used by the image sensor (μs).
                - Gain - optional; [float]
                    The fixed gain used by the image sensor (dB).
                - Iris - optional; [float]
                    The fixed attenuation of input light affected by the iris (dB). 0dB maps to a fully opened iris and positive values map to higher attenuation.
            """
            self.Mode = mode.value
            if priority != None : self.Priority = priority.value
            if window != None : self.Window = window
            if min_exposure_time != None : self.MinExposureTime = min_exposure_time
            if max_exposure_time != None : self.MaxExposureTime = max_exposure_time
            if min_gain != None : self.MinGain = min_gain
            if max_gain != None : self.MaxGain = max_gain
            if min_iris != None : self.MinIris = min_iris
            if max_iris != None : self.MaxIris = max_iris
            if exposure_time != None : self.ExposureTime = exposure_time
            if gain != None : self.Gain = gain
            if iris != None : self.Iris = iris

        def to_dict(self) -> dict:
            return self.__dict__

    class FocusConfiguration20:
        def __init__(self,auto_focus_mode : ImagesEnumParams.AutoFocusMode,af_mode = None,\
                    default_speed = None,near_limit = None,far_limit = None,extension = None) -> None:
            """
            Focus configuration.
            - reqirements;
                - AFMode - optional; [StringAttrList] 
                    Zero or more modes as defined in enumeration tt:AFModes.
                - AutoFocusMode [AutoFocusMode]
                    Mode of auto focus.
                - DefaultSpeed - optional; [float]
                - NearLimit - optional; [float]
                    Parameter to set autofocus near limit (unit: meter).
                - FarLimit - optional; [float]
                        Parameter to set autofocus far limit (unit: meter).
                - Extension - optional; [FocusConfiguration20Extension]
            """
            self.AFMode = af_mode
            self.AutoFocusMode = auto_focus_mode.value
            if default_speed != None : self.DefaultSpeed = default_speed
            if near_limit != None : self.NearLimit = near_limit
            if far_limit != None : self.FarLimit = far_limit
            if extension != None : self.Extension = extension

        def to_dict(self) -> dict:
            return self.__dict__

    class WideDynamicRange20:
        def __init__(self,mode : ImagesEnumParams.WideDynamicMode,level = None) -> None:
            """
            WDR settings.
            - reqirements;
                - Mode [WideDynamicMode]
                    Wide dynamic range mode (on/off).
                    - enum { 'OFF', 'ON' }
                - Level - optional; [float]
                    Optional level parameter (unit unspecified).
            """
            self.Mode = mode.value
            if level != None: self.Level = level

        def to_dict(self) -> dict:
            return self.__dict__

    class WhiteBalance20:
        def __init__(self,mode : ImagesEnumParams.WhiteBalanceMode,cr_gain = None,cb_gain = None,extension = None) -> None:
            """
            White balance settings.
            - reqirements;
                - Mode [WhiteBalanceMode]
                    'AUTO' or 'MANUAL'
                - CrGain - optional; [float]
                    Rgain (unitless).
                - CbGain - optional; [float]
                    Bgain (unitless).
                - Extension - optional; [WhiteBalance20Extension]
            """
            self.Mode = mode.value
            if cr_gain != None: self.CrGain = cr_gain
            if cb_gain != None: self.CbGain = cb_gain
            if extension != None: self.Extension = extension

        def to_dict(self) -> dict:
            return self.__dict__

    class ImagingSettings20:
        def __init__(self,backlight_compensation = None,brightness = None,color_saturation = None,\
                    contrast = None,exposure = None,focus = None,ir_cut_filter = None,\
                        sharpness = None,wide_dynamic_range = None,white_balance = None,extension = None) -> None:
            """
            Imaging Settings of the device.
            - reqirements;
                - BacklightCompensation - optional; [BacklightCompensation20]
                - Brightness - optional; [float]
                    Image brightness (unit unspecified).
                - ColorSaturation - optional; [float]
                    Color saturation of the image (unit unspecified).
                - Contrast - optional; [float]
                    Contrast of the image (unit unspecified).
                - Exposure - optional; [Exposure20]
                - Focus - optional; [FocusConfiguration20]
                    Focus configuration.
                - IrCutFilter - optional; [IrCutFilterMode]
                    Infrared Cutoff Filter settings.
                - Sharpness - optional; [float]
                    Sharpness of the Video image.
                - WideDynamicRange - optional; [WideDynamicRange20]
                    WDR settings.
                - WhiteBalance - optional; [WhiteBalance20]
                    White balance settings.
                - Extension - optional; [ImagingSettingsExtension20]    
            """
            if backlight_compensation != None:
                if type(backlight_compensation) != dict: self.BacklightCompensation = backlight_compensation.to_dict()
                else: self.BacklightCompensation = backlight_compensation
            if brightness != None: self.Brightness = brightness
            if color_saturation != None: self.ColorSaturation = color_saturation
            if contrast != None: self.Contrast = contrast
            if exposure != None:
                if type(exposure) != dict: self.Exposure = exposure.to_dict()
                else: self.Exposure = exposure
            if focus != None:
                if type(focus) != dict: self.Focus = focus.to_dict()
                else: self.Focus = focus
            if ir_cut_filter != None: self.IrCutFilter = ir_cut_filter
            if sharpness != None: self.Sharpness = sharpness
            if wide_dynamic_range != None:
                if type(wide_dynamic_range) != dict: self.WideDynamicRange = wide_dynamic_range.to_dict()
                else: self.WideDynamicRange = wide_dynamic_range
            if white_balance != None:
                if type(white_balance) != dict: self.WhiteBalance = white_balance.to_dict()
                else: self.WhiteBalance = white_balance
            if extension != None:
                if type(extension) != dict: self.Extension = extension.to_dict()
                else: self.Extension = extension

        def to_dict(self) -> dict:
            return self.__dict__

    class ImagingSettingsExtension20:
        def __init__(self,image_stabilization = None,extension = None) -> None:
            """
            - reqirements;
                - ImageStabilization - optional; [ImageStabilization]
                    Optional element to configure Image Stabilization feature.
                - Extension - optional; [ImagingSettingsExtension202]
            """
            if image_stabilization != None:
                if type(image_stabilization) != dict: self.ImageStabilization = image_stabilization.to_dict()
                else: self.ImageStabilization = image_stabilization
            if extension != None:
                self.Extension = extension
        
        def to_dict(self) -> dict:
            return self.__dict__

    class ImagingSettingsExtension202:
        def __init__(self,ir_cut_filter_auto_adjustment = None,extension = None) -> None:
            """
            - reqirements;
                - IrCutFilterAutoAdjustment - optional, unbounded; [IrCutFilterAutoAdjustment]
                    An optional parameter applied to only auto mode to adjust timing of toggling Ir cut filter.
                - Extension - optional; [ImagingSettingsExtension203]
            """
            if ir_cut_filter_auto_adjustment != None:
                if type(ir_cut_filter_auto_adjustment) != dict: self.IrCutFilterAutoAdjustment = ir_cut_filter_auto_adjustment.to_dict()
                else: self.IrCutFilterAutoAdjustment = ir_cut_filter_auto_adjustment
            if extension != None:
                self.Extension = extension
        
        def to_dict(self) -> dict:
            return self.__dict__

    class ImagingSettingsExtension203:
        def __init__(self,tone_compensation = None,defogging = None,noise_reduction = None,extension = None) -> None:
            """
            - reqirements;
                - ToneCompensation - optional; [ToneCompensation]
                    Optional element to configure Image Contrast Compensation.
                - Defogging - optional; [Defogging]
                    Optional element to configure Image Defogging.
                - NoiseReduction - optional; [NoiseReduction]
                    Optional element to configure Image Noise Reduction.
                - Extension - optional; [ImagingSettingsExtension204]
            """
            if tone_compensation != None:
                if type(tone_compensation) != dict: self.ToneCompensation = tone_compensation.to_dict()
                else: self.ToneCompensation = tone_compensation
            if defogging != None:
                if type(defogging) != dict: self.Defogging = defogging.to_dict()
                else: self.Defogging = defogging
            if noise_reduction != None:
                if type(noise_reduction) != dict: self.NoiseReduction = noise_reduction.to_dict()
                else: self.NoiseReduction = noise_reduction
            if extension != None:
                self.Extension = extension
        
        def to_dict(self) -> dict:
            return self.__dict__

    class ImageStabilization:
        def __init__(self,mode : ImagesEnumParams.WideDynamicMode,level = None,extension = None) -> None:
            """
            Optional element to configure Image Stabilization feature.
            - reqirements;
                - Mode [ImageStabilizationMode]
                    Parameter to enable/disable Image Stabilization feature.
                    - enum { 'OFF', 'ON' }
                - Level - optional; [float]
                    Optional level parameter (unit unspecified)
                - Extension - optional; [ImageStabilizationExtension]
            """
            self.Mode = mode.value
            if level != None: self.Level = level
            if extension != None: self.Extension = extension

        def to_dict(self) -> dict:
            return self.__dict__

    class IrCutFilterAutoAdjustment:
        def __init__(self,boundary_type : str,boundary_offset = None,response_time = None,extension = None) -> None:
            """
            An optional parameter applied to only auto mode to adjust timing of toggling Ir cut filter.
            - reqirements;
                - BoundaryType [string]
                    Specifies which boundaries to automatically toggle Ir cut filter following parameters are applied to. 
                    Its options shall be chosen from tt:IrCutFilterAutoBoundaryType.  
                - BoundaryOffset - optional; [float]
                    Adjusts boundary exposure level for toggling Ir cut filter to on/off specified with unitless normalized value from +1.0 to -1.0. 
                    Zero is default and -1.0 is the darkest adjustment (Unitless).   
                - ResponseTime - optional; [duration]
                    Delay time of toggling Ir cut filter to on/off after crossing of the boundary exposure levels.     
                - Extension - optional; [IrCutFilterAutoAdjustmentExtension]
            """
            self.BoundaryType = boundary_type
            if boundary_offset != None: self.BoundaryOffset = boundary_offset
            if response_time != None: self.ResponseTime = response_time
            if extension != None: self.Extension = extension

        def to_dict(self) -> dict:
            return self.__dict__
        
    class ToneCompensation:
        def __init__(self,mode : ImagesEnumParams.ToneCompensationMode,level = None,extension = None) -> None:
            """
            Optional element to configure Image Contrast Compensation.
            - reqirements;
                - Mode [ToneCompensationMode]
                    Parameter to enable/disable or automatic ToneCompensation feature. Its options shall be chosen from tt:ToneCompensationMode Type.
                - Level - optional; [float]
                    Optional level parameter specified with unitless normalized value from 0.0 to +1.0.
                - Extension - optional; [ToneCompensationExtension]
            """
            self.Mode = mode.value
            if level != None: self.Level = level
            if extension != None: self.Extension = extension

        def to_dict(self) -> dict:
            return self.__dict__
        
    class Defogging:
        def __init__(self,mode : ImagesEnumParams.DefoggingMode,level = None,extension = None) -> None:
            """
            Optional element to configure Image Defogging.
            - reqirements;
                - Mode [DefoggingMode]
                    Parameter to enable/disable or automatic Defogging feature. Its options shall be chosen from tt:DefoggingMode Type.
                - Level - optional; [float]
                    Optional level parameter specified with unitless normalized value from 0.0 to +1.0.
                - Extension - optional; [DefoggingExtension]
            """
            self.Mode = mode.value
            if level != None: self.Level = level
            if extension != None: self.Extension = extension
            
        def to_dict(self) -> dict:
            return self.__dict__

    class NoiseReduction:
        def __init__(self,level : float) -> None:
            """
            Optional element to configure Image Noise Reduction.
            - reqirements;
                - Level [float]
                    Level parameter specified with unitless normalized value from 0.0 to +1.0. 
                    Level=0 means no noise reduction or minimal noise reduction.
            """
            self.Level = level
            
        def to_dict(self) -> dict:
            return self.__dict__
    

