
from lib.params.analytics_request_params import AnalyticsRequestParams

class AnalyticsRequestMessages:
    class CreateAnalyticsModulesMessage:
        def __init__(self,configuration_token : str,analytics_module : AnalyticsRequestParams.Config) -> None:
            """
            Add one or more analytics modules to an existing VideoAnalyticsConfiguration. 
            The available supported types can be retrieved via GetSupportedAnalyticsModules, where the Name of the supported AnalyticsModules correspond to the type of an AnalyticsModule instance.
            Pass unique module names which can be later used as reference. 
            The Parameters of the analytics module must match those of the corresponding AnalyticsModuleDescription.
            - requirements : 
                - configuration_token [ReferenceToken]
                    Reference to an existing VideoAnalyticsConfiguration.
                - analytics_module [Config]
            """
            self.ConfigurationToken = configuration_token
            self.AnalyticsModule = analytics_module.to_dict()
    
        def to_dict(self) -> dict:
            return self.__dict__
        
    class ModifyAnalyticsModulesMessage:
        def __init__(self,configuration_token : str,analytics_module : AnalyticsRequestParams.Config) -> None:
            """
            Modify the settings of one or more analytics modules of a VideoAnalyticsConfiguration. 
            The modules are referenced by their names. It is allowed to pass only a subset to be modified.
            - requirements : 
                - configuration_token [ReferenceToken]
                    Reference to an existing VideoAnalyticsConfiguration.
                - analytics_module [Config]
            """
            self.ConfigurationToken = configuration_token
            self.AnalyticsModule = analytics_module.to_dict()
    
        def to_dict(self) -> dict:
            return self.__dict__

    class CreateRulesMessage:
        def __init__(self,configuration_token : str,rule : AnalyticsRequestParams.Config) -> None:
            """
            Add one or more rules to an existing VideoAnalyticsConfiguration. 
            The available supported types can be retrieved via GetSupportedRules, \
                where the Name of the supported rule correspond to the type of an rule instance.
            - requirements : 
                - configuration_token [ReferenceToken]
                    Reference to an existing VideoAnalyticsConfiguration.
                - rule [Config]
            """
            self.ConfigurationToken = configuration_token
            self.Rule = rule.to_dict()
    
        def to_dict(self) -> dict:
            return self.__dict__
        
    class ModifyRulesMessage:
        def __init__(self,configuration_token : str,rule : AnalyticsRequestParams.Config) -> None:
            """
            Modify one or more rules of a VideoAnalyticsConfiguration. The rules are referenced by their names.
            - requirements : 
                - configuration_token [ReferenceToken]
                    Reference to an existing VideoAnalyticsConfiguration.
                - rule [Config]
            """
            self.ConfigurationToken = configuration_token
            self.Rule = rule.to_dict()
    
        def to_dict(self) -> dict:
            return self.__dict__