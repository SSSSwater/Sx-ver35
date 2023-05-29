from nonebot.adapters.onebot.v11 import Message, MessageEvent, MessageSegment, Bot, Event
from nonebot.params import T_State, CommandArg
from nonebot.plugin import on_command
from nonebot import get_driver
from nonebot.adapters.onebot.v11.helpers import HandleCancellation
from .ocr import *

global_config = get_driver().config
ocr = on_command(
    "ocr", aliases=set(global_config.ocr_key), priority=30
)


@ocr.handle()
async def ocr_first(
        bot: Bot,
        event: MessageEvent,
        state: T_State,
        args: Message = CommandArg(),
):
    state['id'] = event.get_user_id()
    for seg in args:
        if seg.type == "image":
            state['img'] = seg
            break


@ocr.got("img", prompt="上传需要需要ocr的图片喵", parameterless=[HandleCancellation("已取消")])
async def ocr_handle_img(event: MessageEvent, state: T_State):
    for seg in state["img"]:
        if seg.type == "image":
            result = get_ocr(seg.data["url"])
            if result is None:
                await ocr.finish(Message(f"[CQ:at,qq={state['id']}]找不到文字喵..."))
            await ocr.finish(Message(f"[CQ:at,qq={state['id']}]{result}"))

        else:
            await ocr.finish(Message(f"[CQ:at,qq={state['id']}]不是图喵"))
