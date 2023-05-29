from nonebot import get_driver, on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.log import logger
from nonebot.exception import ActionFailed
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent, MessageEvent, Message
import requests, uuid, base64
from .processData import *
from nonebot_plugin_imageutils import text2image, BuildImage

my_uuid = uuid.uuid4()
global_config = get_driver().config

getE = on_command("随机发电", aliases=set(global_config.gete_key), priority=50, block=True)
setE = on_command("创作发电", aliases=set(global_config.sete_key), priority=50, block=True)


@getE.handle()
async def getElect(bot: Bot, event: Event, state: T_State):
    ids = event.get_session_id()

    reply = getMeg()
    msg_img = BuildImage(
        text2image(reply[3]+"\n--"+reply[0]+'\n'+reply[2], padding=(20, 20), max_width=800),
    ).save_jpg()
    msg=MessageSegment.image(msg_img)+"\n"+MessageSegment.image(reply[1])
    try:
        logger.info(reply)
        await getE.send(msg)
    except ActionFailed:
        await getE.finish("风控了没发出去喵...")
    await getE.finish()

@setE.handle()
async def setElect(bot: Bot, event: Event, state: T_State):
    ids = event.get_session_id()

    try:
        setMsg(event.get_user_id(),event.get_plaintext().strip("创作发电 "))
        await setE.send("创建成功!")
    except:
        await setE.finish("创建失败...")
    await setE.finish()


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
