from enum import Enum

def generate_active_cells():
    pass

class AnalyticsEnumParams:
    pass

class AnalyticsRequestParams:
    class ElementItem:
        def __init__(self,name = None) -> None:
            """
            Complex value structure.
            - requirements; 
                - Name - required; [string]
                    Item name.
            """
            self.Name = name

        def to_dict(self) -> dict:
            return self.__dict__
        
    class SimpleItem:
        def __init__(self,name = None,value = None) -> None:
            """
            Value name pair as defined by the corresponding description.
            - requirements; 
                - Name - required; [string]
                    Item name.
                - Value - required; [anySimpleType]
                    Item value. The type is defined in the corresponding description.
            """
            self.Name = name
            self.Value = value

        def to_dict(self) -> dict:
            return self.__dict__
    
    class ItemList:
        def __init__(self,simple_item = None,element_item = None,extension = None) -> None:
            """
            List of configuration parameters as defined in the corresponding description.
            - requirements; 
                - SimpleItem - optional, unbounded [list of SimpleItem [it has to be dict type]];
                    Value name pair as defined by the corresponding description.
                    - For Example:
                        -   [
                                {
                                    'Name': 'MinCount',
                                    'Value': '5'
                                },
                                {
                                    'Name': 'AlarmOnDelay',
                                    'Value': '1000'
                                }
                            ]
                - ElementItem - optional, unbounded [list of ElementItem];
                    Complex value structure.
                - Extension - optional; [ItemListExtension]
            """
            if simple_item != None : self.SimpleItem = simple_item
            if element_item != None : self.ElementItem = element_item
            if extension != None : self.Extension = extension

        def to_dict(self) -> dict:
            return self.__dict__

    class Config:
        def __init__(self,name : str,parameters : 'AnalyticsRequestParams.ItemList',type_name : str) -> None:
            """
            AnalyticsModule - unbounded
            - requirements; 
                - Name - required; [string]
                    Name of the configuration.
                - Type - required; [QName]
                    The Type attribute specifies the type of rule and shall be equal to value of one of Name attributes of ConfigDescription elements returned by GetSupportedRules and GetSupportedAnalyticsModules command.
                - Parameters [ItemList]
                    List of configuration parameters as defined in the corresponding description.
            """
            self.Name = name
            self.Type = type_name
            if type(parameters) != dict: self.Parameters = parameters.to_dict()
            else: self.Parameters = parameters
            
        def to_dict(self) -> dict:
            return self.__dict__


