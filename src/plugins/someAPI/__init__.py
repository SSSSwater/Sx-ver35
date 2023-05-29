from nonebot import get_driver, on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.log import logger
from nonebot.exception import ActionFailed
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent, MessageEvent, Message
from src.plugins.chatgpt35.config import Config
import requests, uuid, base64
from .uomgapi import *

my_uuid = uuid.uuid4()
global_config = get_driver().config

tuwei = on_command("土味情话", aliases=set(global_config.tuwei_key), priority=50, block=True)
gedan = on_command("查询最近听歌品味", aliases=set(global_config.gedan_key), priority=50, block=True)


@tuwei.handle()
async def send_qinghua(bot: Bot, event: Event, state: T_State):
    ids = event.get_session_id()

    reply = rand_qinghua();
    try:
        await tuwei.send(reply)
    except ActionFailed:
        await tuwei.finish("风控了没发出去喵...")
    await tuwei.finish()

@gedan.handle()
async def send_gedan(bot: Bot, event: Event, state: T_State):
    ids = event.get_session_id()

    reply = rand_music()
    msg=reply['name']+"-"+reply['artistsname']+'\n'+MessageSegment.image(reply['picurl'])+'\n'+reply['url']
    try:
        await gedan.send(msg)
    except ActionFailed:
        await gedan.finish("风控了没发出去喵...")
    await gedan.finish()


async def send_forward_msg(
        bot: Bot,
        event: MessageEvent,
        name: str,
        uin: str,
        msgs: list,
) -> dict:
    """调用合并转发API

        bot: Bot
        event: 消息事件类型
        name: 发送者昵称
        uin: 发送者账号
        msgs: 消息列表
    """

    def to_json(msg: Message):
        return {"type": "node", "data": {"name": name, "uin": uin, "content": msg}}

    messages = [to_json(msg) for msg in msgs]

    if isinstance(event, GroupMessageEvent):
        return await bot.call_api(
            "send_group_forward_msg", group_id=event.group_id, messages=messages
        )
    else:
        return await bot.call_api(
            "send_private_forward_msg", user_id=event.user_id, messages=messages
        )
