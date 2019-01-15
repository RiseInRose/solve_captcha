import random
from io import BytesIO
import json
import re
import time
from io import StringIO

from PIL import Image
import execjs
import requests

from wuba.utils import product_trace, RClient


class AJK_Slide_Captcha():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                      AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
    }
    def get_sessionId(self,captcha_url):
        resp = requests.get(captcha_url, headers=self.headers)
        html = resp.content.decode()
        serialId = re.search('<input type="hidden" id="serialId" value="(.*?)"', html).group(1)
        code = re.search('<input type="hidden" id="code" value="(.*?)"', html).group(1)
        sign = re.search('<input type="hidden" id="sign" value="(.*?)"', html).group(1)
        data = {
            'code':code,
            'serialId':serialId,
            'sign':sign,
        }
        resp = requests.post('https://callback.58.com/firewall/codev2/getsession.do',data=data,headers=self.headers)
        sessionId = json.loads(resp.text)['data']['sessionId']
        # sessionId = re.search('name="sessionId".*?value="(.*?)"', html).group(1)
        return sessionId


    def get_responseId_bgImgUrl(self,sessionId):
        resp = requests.get(
            "https://verifycode.58.com/captcha/getV3",
            headers=self.headers,
            params={
                "callback": "callback",
                "showType": "embed",
                "sessionId": sessionId,
                "_": str(int(time.time() * 1000))
            }
        )

        captchaData = json.loads(resp.text.replace("callback(", "").replace(")", ""))
        responseId = captchaData["data"]["responseId"]
        bgImgUrl = captchaData["data"]["bgImgUrl"]
        return (responseId,bgImgUrl)

    def get_image(self,bgImgUrl):
        resp = requests.get(
            "https://verifycode.58.com" + bgImgUrl,
            headers=self.headers
        )

        # req.content是二进制的字符串 传化为file 的 io对象
        image = Image.open(BytesIO(resp.content))
        image = image.resize((284, 160))

        o = BytesIO()
        image.save(o,'JPEG')
        image.show()

        return o.getvalue()

    def get_4_zuobiao(self,image):
        """
        得到4个坐标
        :param image:
        :return: 返回
        """
        rc = RClient('xxx', 'xxx', 'xxx', 'xxx')
        result = rc.rk_create(image, 6904)['Result'].split('.')
        print(result)
        return result
        # product_trace(result)


    def get_trace(self,res):
        return product_trace(res)

    def get_fpToken(self):
        resp = requests.get(
            "https://cdata.58.com/fpToken",
            headers=self.headers,
            params={
                "callback": "callback",
            }
        )
        fpData = json.loads(resp.text.replace("callback(", "").replace(")", ""))
        fpToken = fpData["token"]
        return fpToken

    def get_jiami_data(self,responseId,fpToken,lastXpos,trace):
        jsCode = execjs.compile(open("./jiami.js", "r").read())
        jiami_data = jsCode.call("getSlideAnswer", responseId, fpToken, lastXpos, trace)
        return jiami_data

    def slove(self,jiami_data,responseId,sessionId):
        response = requests.get(
            "https://verifycode.58.com/captcha/checkV3",
            headers=self.headers,
            params={
                "data": jiami_data,
                "responseId": responseId,
                "sessionId": sessionId,
                "_": str(int(time.time() * 1000))
            }
        )
        return response.text

    def run(self):
        # step1: 在验证码页面中 获取 sessionId
        sessionId = self.get_sessionId('https://callback.58.com/firewall/verifycode?serialId=abde8e15deadd6543bd0f3e89028db5c_2c5813f1189b4ed6a8744f7149e9968a&code=22&sign=b8d925f88a1c2412f896dac9c83182fc&namespace=jianzhi_list&url=https://info5.58.com:443/hf/partime/?b_q=%E5%85%BC%E8%81%8C')
        print('step1:    sessionId->', sessionId)
        # step2: 获取 responseId 和 bgImgUrl
        (responseId, bgImgUrl) = self.get_responseId_bgImgUrl(sessionId)
        print('step2:    responseId->', responseId)
        # Step 3, Get Image
        image = self.get_image(bgImgUrl)
        print('step3:    image->', image)
        # Step 4 ,get 4 zuobiao
        position_4 = self.get_4_zuobiao(image)
        print('step4:    position->', position_4)
        # Step 5 get trace
        lastXpos,trace = self.get_trace(position_4)
        print('step5:    trace->', trace)
        # Step 6 get fpToken
        fpToken = self.get_fpToken()
        print('step6:    fpToken->', fpToken)
        # Step 7 加密data
        jiami_data = self.get_jiami_data(responseId,fpToken,lastXpos,trace)
        print('step7:    jiami_data->', jiami_data)
        # Step 8 slove
        responseText = self.slove(jiami_data,responseId,sessionId)
        print('\nstep8:    最后请求结果->', responseText)



if __name__ == '__main__':
    AJK_Slide_Captcha().run()
















