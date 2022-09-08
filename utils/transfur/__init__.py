import datetime
import hashlib
from configparser import ConfigParser
from typing import List, Union, Any

import urllib3
import json

from utils import to_async

config: ConfigParser  # Declare the type of config, or the IDE will report an error


class Tailapi:
    """Summary of TailApi.

    This code encapsulates the TailApi,
    which can increase the readability of the code after packetting.

    Attributes:
		path: 	A string of the path to the config file
        url: Entrypoint Url. String
        ts: timestamp. but string
        name: A string of Fursuit Name
        furid:A string of Furuit ID
    """

    def __init__(self, path) -> None:
        global config
        config = ConfigParser()
        config.read(path, encoding="UTF-8")
        return

    @classmethod
    def signutil(cls, url, ts) -> List[Union[str, Any]]:
        key = config["Tailapi"]["key"]
        qq = config["Tailapi"]["qq"]
        preSigned = f"{url}-{str(ts)}-{key}"
        return [hashlib.md5(preSigned.encode(encoding="UTF-8")).hexdigest(), qq]

    @to_async
    def getFursuitRand(self):
        ts = datetime.datetime.now().timestamp()
        sign = Tailapi.signutil("api/v2/getFursuitRand", ts)
        prsign = sign[0]
        http = urllib3.PoolManager()
        resp = http.request(
            "GET",
            "https://api.tail.icu/api/v2/getFursuitRand?qq="
            + sign[1]
            + "&timestamp="
            + str(ts)
            + "&sign="
            + prsign,
        )  # get方式请求
        text = json.loads(resp._body)
        return text

    @to_async
    def getFursuitByName(self, name):
        ts = datetime.datetime.now().timestamp()
        sign = Tailapi.signutil("api/v2/getFursuitByName", ts)
        prsign = sign[0]
        http = urllib3.PoolManager()
        resp = http.request(
            "GET",
            "https://api.tail.icu/api/v2/getFursuitByName?qq="
            + sign[1]
            + "&timestamp="
            + str(ts)
            + "&sign="
            + prsign
            + "&name="
            + name,
        )
        text = json.loads(resp._body)
        return text

    @to_async
    def getFursuitByID(self, furid):
        ts = datetime.datetime.now().timestamp()
        sign = Tailapi.signutil("api/v2/getFursuitByID", ts)
        prsign = sign[0]
        http = urllib3.PoolManager()
        resp = http.request(
            "GET",
            "https://api.tail.icu/api/v2/getFursuitByID?qq="
            + sign[1]
            + "&timestamp="
            + str(ts)
            + "&sign="
            + prsign
            + "&fid="
            + furid,
        )
        text = json.loads(resp._body)
        return text

    @to_async
    def getDaliyFursuitRand(self):
        ts = datetime.datetime.now().timestamp()
        sign = Tailapi.signutil("api/v2/DailyFursuit/Rand", ts)
        prsign = sign[0]
        http = urllib3.PoolManager()
        resp = http.request(
            "GET",
            "https://api.tail.icu/api/v2/DailyFursuit/Rand?qq="
            + sign[1]
            + "&timestamp="
            + str(ts)
            + "&sign="
            + prsign,
        )
        text = json.loads(resp._body)
        return text

    @to_async
    def getDaliyFursuitByID(self, dayid):
        ts = datetime.datetime.now().timestamp()
        sign = Tailapi.signutil("api/v2/DailyFursuit/id", ts)
        prsign = sign[0]
        http = urllib3.PoolManager()
        resp = http.request(
            "GET",
            "https://api.tail.icu/api/v2/DailyFursuit/id?qq="
            + sign[1]
            + "&timestamp="
            + str(ts)
            + "&sign="
            + prsign
            + "&id="
            + dayid,
        )
        text = json.loads(resp._body)
        return text

    @to_async
    def getDaliyFursuitByName(self, name):
        ts = datetime.datetime.now().timestamp()
        sign = Tailapi.signutil("api/v2/DailyFursuit/name", ts)
        prsign = sign[0]
        http = urllib3.PoolManager()
        resp = http.request(
            "GET",
            "https://api.tail.icu/api/v2/DailyFursuit/name?qq="
            + sign[1]
            + "&timestamp="
            + str(ts)
            + "&sign="
            + prsign
            + "&name="
            + name,
        )
        text = json.loads(resp._body)
        return text


# api=Tailapi("../config/bot.conf")
# print(api.getFursuitByName("我是你爸爸"))
