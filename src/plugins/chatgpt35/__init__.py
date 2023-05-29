from nonebot import get_driver, on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.log import logger
from nonebot.exception import ActionFailed
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent, MessageEvent, Message
from src.plugins.chatgpt35.config import Config
import requests, uuid, base64

my_uuid = uuid.uuid4()
my_content = ''
global_config = get_driver().config
api = global_config.openai_api
resp_key = global_config.openai_resp_key
img_key = global_config.openai_img_key

headers = {
    'Content-Type': 'application/json',
    "Authorization": "Bearer " + api
}
url_root = "https://api.openai.com/v1/"
# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass

def chatgpt_resp(msg):
    # url="https://api.openai-proxy.com/pro/chat/completions"
    url = url_root+"chat/completions"
    param = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": my_content + msg}],
        "temperature": 0.7
    }
    try:
        response = requests.post(url=url, headers=headers, json=param)
        logger.info(response.json())
        return response.json()['choices'][0]['message']['content']
    except:
        return response.text

def chatgpt_model_list():
    # url="https://api.openai-proxy.com/pro/chat/completions"
    url = url_root+"models"
    param = {
    }
    try:
        response = requests.get(url=url, headers=headers)
        logger.info(response.json())
        return [d['id'] for d in response.json()['data']]
    except:
        return response.text


def chatgpt_img(msg):
    # url="https://api.openai-proxy.com/pro/chat/completions"
    url = url_root+"/images/generations"
    param = {
        "prompt": msg,
        "response_format": "b64_json"
    }
    try:
        response = requests.post(url=url, headers=headers, json=param)
        return response.json()['data'][0]['b64_json']
    except:
        return "你先别急，现在被限流了喵..."


response = on_command(resp_key, priority=Config.Config.priority, rule=to_me(), block=True)
image = on_command(img_key, priority=Config.Config.priority, rule=to_me(), block=True)


@response.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    ids = event.get_session_id()

    if ids.startswith("group"):
        if not event.is_tome():
            await response.skip()
    msg = event.get_plaintext().replace(resp_key, '').strip().replace('\n', '').replace('\r\n', '')
    if(msg.startswith("list")):reply=chatgpt_model_list()
    else:reply = chatgpt_resp(msg)
    logger.info(reply)
    logger.info(len(reply))
    if (len(reply) > 200):
        div_num = (len(reply) // 200) + 1
        reply_list = []
        for i in range(0, div_num):
            if i < div_num - 1:
                reply_list.append(reply[i * 200:(i + 1) * 200])
            else:
                reply_list.append(reply[i * 200:])
        logger.info(reply_list)
        try:
            await send_forward_msg(bot, event, "Sx", bot.self_id, reply_list)
        except ActionFailed:
            await response.finish("合并转发失败，请重试，如果多次失败可能是账户风控了喵")
        await response.finish()
    else:
        try:
            await response.send(reply)
        except:
            await response.finish("风控了没发出去喵...")
        await response.finish()


@image.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    ids = event.get_session_id()

    if ids.startswith("group"):
        if not event.is_tome():
            await image.skip()
    msg = event.get_plaintext().replace(img_key, '').strip().replace('\n', '').replace('\r\n', '')
    reply = chatgpt_img(msg)
    try:
        try:
            rep_img=base64.b64decode(reply)
        except:
            image.finish("你先别急，现在被限流了喵...")
        await image.send(MessageSegment.image(rep_img))
    except:
        await image.finish("风控了没发出去喵...")
    await response.finish()


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

