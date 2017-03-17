from django.shortcuts import render
from django.http import HttpResponse
from blog import weiUtil
from blog import weixinUtils
import xml.etree.ElementTree as ET


# Create your views here.
def hello(request):
    return render(request, 'index.html')


def handle(request):
    """微信公众号码平台搭建验证：
    1：提取四个参数
    2：配置token信息
    3：将token,timestamp,nonce,三个参数放入list集合中，
    4：他排序list集合，并连接成一个字符串
    5：将字符串使用hash算法中的sha1加密
    6：与传入的signature比较是否相同
    """
    Token = "HingLo"
    EncodingAESKey = "mTcmKtjfiDD66iDlz7Mq2yIDHGSXkBoNJKDmFJTNxis"
    AppId = "wx83f0d8afba67e8c1"
    if request.method == 'GET':
        try:
            data = request.GET
            if len(data) == 0:
                return HttpResponse("hello, this is handle view")
            signature = "".join(data["signature"])
            timestamp = "".join(data["timestamp"])
            nonce = "".join(data["nonce"])
            echostr = "".join(data["echostr"])
            token = "HingLo"  # 请按照公众平台官网\基本配置中信息填写
            hashcode = weiUtil.getSHA1(token, timestamp, nonce)  # 得到加密结果
            if hashcode == signature:
                return HttpResponse(echostr)
            else:
                return HttpResponse("")
        except Exception as e:
            return HttpResponse(e)
    else:
        signature = ''.join(request.GET.get('signature'))
        msg_signature = ''.join(request.GET.get('msg_signature'))
        timestamp = ''.join(request.GET.get('timestamp'))
        nonce = ''.join(request.GET.get('nonce'))
        data = request.body.decode('utf-8')
        wXBizMsgCrypt = weixinUtils.WXBizMsgCrypt(signature=signature, msg_signature=msg_signature, timestamp=timestamp,
                                                  nonce=nonce)
        ret, xml_content = wXBizMsgCrypt.encrypt(body_text=data)

        if ret == 0:
            # 解码为utf-8
            xml_content = xml_content.decode('utf-8')
            print(xml_content)
            # 解析xml 字符串
            xml = ET.fromstring(xml_content)  # 进行XML解析
            msgType = xml.find("MsgType").text
            if msgType == 'text':
                # content = textMassage(request, wXBizMsgCrypt, xml)
                content = xml.find('Content')
                print(content)
                return HttpResponse(content, content_type="application/xml")
            elif msgType == 'image':
                pass
            elif msgType == 'voice':
                pass
            elif msgType == 'video':
                pass
            elif msgType == 'shortvideo':
                pass
            elif msgType == 'location':
                pass
            elif msgType == 'link':
                pass

        else:
            print(ret)


def textMassage(request, wXBizMsgCrypt, xml):
    """文本消息处理"""
    content = xml.find("Content").text
    # 返回消息
    nonce = ''.join(request.GET.get('nonce'))
    timestamp = ''.join(request.GET.get('timestamp'))
    ret, content = wXBizMsgCrypt.EncryptMsg(content, nonce)
    return content


def imageMassage(request, xml):
    """图片消息处理"""
    pass


def voiceMassage(request, xml):
    """语音消息处理"""
    pass


def videoMassage(request, xml):
    """频消息处理"""
    pass


def shortVideoMassage(request, xml):
    """短视频消息处理"""
    pass


def locationMassage(request, xml):
    """位置消息处理"""
    pass


def linkMassage(request, xml):
    """连接消息处理"""
    pass
