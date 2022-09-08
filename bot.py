import botpy
from botpy.types.message import Message
from botpy import logging
from configparser import ConfigParser
from threading import Thread
from botpy.user import Member
from utils.transfur import Tailapi
import platform
from botpy.types.message import Reference
import os
import requests
import re
def download_img(img_url,filename):
    r = requests.get(img_url, stream=True)
    if r.status_code == 200:
        open(filename,'wb').write(r.content)
        return filename
    del r
onlog = logging.get_logger()

class readcfg():
    def __init__(self,path) -> None:
        global config
        config = ConfigParser()
        config.read(path, encoding='UTF-8')
        return 
    def on_load(self,key,value) -> str:
        return config[key][value]
class MyClient(botpy.Client):
    async def on_guild_member_add(self, member: Member):
        pass
    async def on_at_message_create(self, message: Message):
        # 构造消息发送请求数据对象
        message_reference = Reference(message_id=message.id)
        a=await self.api.get_message(channel_id=message.channel_id, message_id=message.id)
        msg_plain=str(a['message']['content'][23:len(a['message']['content'])])
        # 通过api发送回复消息
        if msg_plain.startswith("/来只毛"):
            api=Tailapi("./config/bot.conf")
            context=api.getFursuitRand()
            await self.api.post_message(
                channel_id=message.channel_id,
                content="--- 每日吸毛 Bot ---\n今天你吸毛了嘛？\nFurID: {}\n毛毛名字: {}\n搜索方法：全局随机".format(context['data']['id'],context['data']['name']),
                file_image=download_img(context['data']['url'],os.getcwd()+'\cache\\fursuit\{}.jpg'.format(context['data']['id'])),
                msg_id=message.id,
            )
        if msg_plain.startswith("/来只 "):
            #print(furname)
            api=Tailapi("./config/bot.conf")
            context=api.getFursuitByName(msg_plain.split(" ")[1])
            if context['code'] == 200:
                await self.api.post_message(
                    channel_id=message.channel_id,
                    content="--- 每日吸毛 Bot ---\n今天你吸毛了嘛？\nFurID: {}\n毛毛名字: {}\n搜索方法：模糊搜索".format(context['data']['id'],context['data']['name']),
                    file_image=download_img(context['data']['url'],os.getcwd()+'\cache\\fursuit\{}.jpg'.format(context['data']['id'])),
                    msg_id=message.id,
                )
            else:
                await self.api.post_message(
                    channel_id=message.channel_id,
                    content="这只毛毛不存在",
                    msg_id=message.id,
                )
        if msg_plain.startswith("/查毛图"):
            api=Tailapi("./config/bot.conf")
            context=api.getFursuitByID(msg_plain.split(u"\u56fe")[1])
            if context['code'] == 200:
                await self.api.post_message(
                    channel_id=message.channel_id,
                    content="--- 每日吸毛 Bot ---\n今天你吸毛了嘛？\nFurID: {}\n毛毛名字: {}\n搜索方法：精确".format(context['data']['id'],context['data']['name']),
                    file_image=download_img(context['data']['url'],os.getcwd()+'\cache\\fursuit\{}.jpg'.format(context['data']['id'])),
                    msg_id=message.id,
                )
            else:
                await self.api.post_message(
                    channel_id=message.channel_id,
                    content="这只毛毛不存在",
                    msg_id=message.id,
                )
        if msg_plain.startswith("/每日鉴毛"):
            api=Tailapi("./config/bot.conf")
            context=api.getDaliyFursuitRand()
            if context['code'] == 200:
                await self.api.post_message(
                    channel_id=message.channel_id,
                    file_image=download_img(context['data']['url'],os.getcwd()+'\cache\daily\{}.jpg'.format(context['data']['id'])),
                    msg_id=message.id,
                )
            else:
                await self.api.post_message(
                    channel_id=message.channel_id,
                    content="这期每日鉴毛不存在",
                    msg_id=message.id,
                )
        if msg_plain.endswith("期每日鉴毛") and msg_plain in ["/"+re.findall('\\d+',msg_plain)[0]+"期每日鉴毛"]:
            api=Tailapi("./config/bot.conf")
            context=api.getDaliyFursuitByID(re.findall('\\d+',msg_plain)[0])
            if context['code'] == 200:
                await self.api.post_message(
                    channel_id=message.channel_id,
                    file_image=download_img(context['data']['url'],os.getcwd()+'\cache\daily\{}.jpg'.format(context['data']['id'])),
                    msg_id=message.id,
                )
            else:
                await self.api.post_message(
                    channel_id=message.channel_id,
                    content="这期每日鉴毛不存在",
                    msg_id=message.id,
                )
        if msg_plain in ["/"+msg_plain[1:msg_plain.rfind(u'\u7684')]+"的每日鉴毛"]:
            api=Tailapi("./config/bot.conf")
            context=api.getDaliyFursuitByName(msg_plain[1:msg_plain.rfind(u'\u7684')])
            if context['code'] == 200:
                await self.api.post_message(
                    channel_id=message.channel_id,
                    file_image=download_img(context['data']['url'],os.getcwd()+'\cache\daily\{}.jpg'.format(context['data']['id'])),
                    msg_id=message.id,
                )
            else:
                await self.api.post_message(
                    channel_id=message.channel_id,
                    content="这期每日鉴毛不存在",
                    msg_id=message.id,
                )
if __name__ == '__main__':
    f=readcfg('./config/bot.conf')
    intents = botpy.Intents(public_guild_messages=True) 
    client = MyClient(intents=intents)
    onlog.info("Starting (Ver.%s)..." % readcfg.on_load(f,'bot','version'))
    onlog.info("Platform: %s" % platform.platform())
    onlog.info("Python version: %s" % platform.python_version())
    client.run(appid=readcfg.on_load(f,'app','appid'), token=readcfg.on_load(f,'app','token'))
