from configparser import ConfigParser

configFile = ConfigParser()
configFile.read("config.ini")

try:
    login_header = {
        "Authorization": "Bearer " + configFile["Login"]["authorization_key"],
        "x-hq-client": configFile["General"]["hq_client"]
    }
except:
    login_header = {}

negationWords = ['not']  # NOTE: Everything should be lowercase
whichWords = ['which']  # NOTE: Everything should be lowercase


def readFromConfig(section, parameter):
    value = configFile[section][parameter]

    if value == "True":
        return True
    elif value == "False":
        return False
    else:
        return value
