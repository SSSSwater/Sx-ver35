import json
from nonebot import get_driver
from nonebot.log import logger
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models

cfg = get_driver().config


def get_ocr(url: str) -> bytes:
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
        cred = credential.Credential(cfg.txcloud_secretid, cfg.txcloud_secretkey)
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = ocr_client.OcrClient(cred, "ap-shanghai", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.GeneralAccurateOCRRequest()
        params = {
            "ImageUrl": url,
            "IsWords": True,
            "EnableDetectSplit": True,
            "IsPdf": False
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个GeneralAccurateOCRResponse的实例，与请求对象对应
        resp = client.GeneralAccurateOCR(req)
        # 输出json格式的字符串回包
        data = json.loads(resp.to_json_string())
        texts = [text['DetectedText'] for text in data['TextDetections']]
        result = '\n'.join(texts)
        return result


    except TencentCloudSDKException as err:
        print(err)
