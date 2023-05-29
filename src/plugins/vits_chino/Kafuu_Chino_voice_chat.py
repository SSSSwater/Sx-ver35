from nonebot import on_keyword,get_driver
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.rule import command
from nonebot.adapters.onebot.v11 import MessageSegment
import os
from .config import Config
from .moegoe.MoeGoe import inference
import random

global_config = get_driver().config
chatmodel_path = os.path.split(os.path.realpath(__file__))[0] + '\\moegoe\\'
response = on_keyword(global_config.vits_key, rule=command(global_config.vits_key), priority=Config.priority, block=True)


@response.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    rand = random.randint(1,10000)

    ids = event.get_session_id()
    msg = event.get_plaintext().replace(global_config.vits_key, '').strip().replace('\n', '').replace('\r\n', '')
    inference(chatmodel_path + "models\\G_74000.pth", chatmodel_path + "models\\config.json", 0, msg, chatmodel_path + "output\\temp"+str(rand)+".wav")
    try:
        await response.send(MessageSegment.record('file:///' + chatmodel_path + "output\\temp"+str(rand)+".wav"))
    except:
        await response.finish("啊呜呜~uwu")
    try:
        os.remove(chatmodel_path + "output\\temp"+str(rand)+".wav")
    except:
        pass
    await response.finish()
