import configparser as cp

config = cp.ConfigParser()
config.read("config.ini")

ACCESS_TOKEN = config["ACCESS"]["TOKEN"]
API_VERSION = config["API"]["VERSION"]
URL = config["API"]["URL"]
OFFSET = int(config["API"]["OFFSET"])
COUNT = config["API"]["COUNT"]
