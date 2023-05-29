from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, GROUP, Message, MessageSegment
from nonebot.plugin import on_command
from nonebot import get_driver
from nonebot.params import CommandArg
from typing import List
import time


jrrp = on_command("jrrp", aliases=set(get_driver().config.jrrp_key), permission=GROUP, priority=50)
message: List[dict] = [
    {
        "expr": "jrrp[0] == 100",
        "start": "！！！你今天的人品值是：",
        "end": "sx要恭喜你满分了捏！！！"
    },
    {
        "expr": "jrrp[0] == 99",
        "end": "我超，但是性了捏！"
    },
    {
        "expr": "jrrp[0] >= 90",
        "end": "sx认为你运气爆棚了捏！"
    },
    {
        "expr": "jrrp[0] >= 60",
        "end": "sx觉得会是不错的一天捏！"
    },
    {
        "expr": "jrrp[0] > 50",
        "end": "sx觉得还行捏！"
    },
    {
        "expr": "jrrp[0] == 50",
        "end": "折中捏！sx觉得运气不错！"
    },
    {
        "expr": "jrrp[0] >= 40",
        "end": "s…sx觉得还……还行捏！"
    },
    {
        "expr": "jrrp[0] >= 11",
        "end": "呃呃呃呃呃呃呃呃"
    },
    {
        "expr": "jrrp[0] >= 1",
        "end": "sx想说其实这是百分制捏！"
    },
    {
        "expr": "True",
        "end": "专家sx建议今天不要出门了捏"
    }
]


@jrrp.handle()
async def _h(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    words = args.extract_plain_text()
    if not words:
        session = event.get_session_id()
        id = session.split('_')[2]
        jrrpmsg = get_jrrp(str(id))
        result = get_msg(jrrpmsg)
        reply = MessageSegment.reply(event.message_id)
        await jrrp.send(reply + result)


def rol(num: int, k: int, bits: int = 64):
    b1 = bin(num << k)[2:]
    if len(b1) <= bits:
        return int(b1, 2)
    return int(b1[-bits:], 2)


def get_hash(string: str):
    num = 5381
    num2 = len(string) - 1
    for i in range(num2 + 1):
        num = rol(num, 5) ^ num ^ ord(string[i])
    return num ^ 12218072394304324399


def get_num(string: str, element: str):
    now = time.localtime()
    num = round(abs((get_hash("".join([
        "asdfgbn",
        str(now.tm_yday),
        "12#3$45",
        str(now.tm_year),
        "IUY"
    ])) / 3 + get_hash("".join([
        "QWERTY",
        string,
        "0*8&6",
        str(now.tm_mday),
        "kjhg",
        element,
        "nmsl"
    ])) / 3) / 527) % 10001)
    return num


def get_jrrp(string: str):
    what_to_eat_list = ['萨莉亚', 'KFC', '金拱门', '雪', '白菜肉大馄饨', '沙县小吃', '食堂', '泡面', '滴蜡熊', '大米', '淀粉肠', '绝赞大星星']
    what_to_drink_list = ['可乐', '雪碧', '劲凉冰红茶', '薄荷奶绿', '昏睡红茶', '矿泉水', '杨枝甘露', '蜜雪冰城', '迎宾酒', '沪上阿姨', '一点点']
    when_to_play_list = ['早上堵门', '吃完午饭', '下午', '吃完晚饭', '夜晚', '睡机厅']
    how_to_play_list = ['地铁', '打车', '自行车/电瓶车', '步行', '火箭', '开车', '公交车']
    play_count_list1 = list(range(1, 16))
    play_count_list2 = [39, 2233, 3939, 114514, 1919810, 65535, 2147483647]
    score_to_run_list1 = list(range(1, 26))
    score_to_run_list2 = [100, 514, 233, 8172, 10000, 2010, -1, 10182]
    num_jrrp = 100 if get_num(string, 'jrrp') >= 9600 else round(get_num(string, 'jrrp') / 9599 * 99)
    what_to_eat = what_to_eat_list[get_num(string, 'what_to_eat') % len(what_to_eat_list)]
    what_to_drink = what_to_drink_list[get_num(string, 'what_to_drink') % len(what_to_drink_list)]
    when_to_play = when_to_play_list[get_num(string, 'when_to_play') % len(when_to_play_list)]
    how_to_play = how_to_play_list[get_num(string, 'how_to_play') % len(how_to_play_list)]
    play_count = play_count_list1[get_num(string, 'play_count1') % len(play_count_list1)] if get_num(string,
                                                                                                     'play_count') % 10 != 6 else \
    play_count_list2[get_num(string, 'play_count2') % len(play_count_list2)]
    score_to_run = score_to_run_list1[get_num(string, 'score_to_run1') % len(score_to_run_list1)] if get_num(string,
                                                                                                             'score_to_run') % 10 != 7 else \
    score_to_run_list2[get_num(string, 'score_to_run2') % len(score_to_run_list2)]
    return [num_jrrp, what_to_eat, what_to_drink, when_to_play, how_to_play, play_count, score_to_run]


def get_msg(jrrp):
    msg = ''
    start: str = "你今天的人品值是："
    end: str = "……"
    what_to_eat_msg = '吃' + jrrp[1] + '!'
    what_to_drink_msg = '喝' + jrrp[2] + '!'
    when_to_play_msg = '出勤时间是' + jrrp[3] + '!'
    how_to_play_msg = '出勤方式是' + jrrp[4] + '!'
    play_count_msg = '出勤不超' + str(jrrp[5]) + 'pc!'
    score_to_run_msg = '上' + str(jrrp[6]) + '分后退勤!'
    for msg_obj in message:
        if eval(msg_obj["expr"]):
            start = msg_obj.get("start") if msg_obj.get("start") else start
            end = msg_obj.get("end") if msg_obj.get("end") else end
            msg += start + str(jrrp[0]) + '\n' + end + '\n'
            msg += '\nsx建议你今天:\n\n'
            msg = msg + what_to_eat_msg + '\n' + what_to_drink_msg + '\n' + when_to_play_msg + '\n' + how_to_play_msg + '\n' + play_count_msg + '\n' + score_to_run_msg
            return msg
