import json, os

class DownloaderConfig:
    def __init__(self, configFile):
        if(os.path.isfile(configFile)):
            self.__config = self.__LoadConfig(configFile)
        else:
            self.__config = self.__CreateConfigFile(configFile)
    
    def __CreateConfigFile(self, configFile):
        config = {
            'chromeArgs' : [
                '--incognito'
            ]
        }
        with open('config.json', 'w') as json_file:
            json.dump(config, json_file)
        return config 
    
    def __LoadConfig(self, configFile):
        with open(configFile) as json_file:
            config = json.load(json_file)
        return config
    
    def GetChromeArgs(self):
        return self.__config['chromeArgs']