#!/usr/bin/env python3
# coding:UTF-8
# author = 'HingLo.C'
""""
文件说明：AES对xml的加密与解密
"""
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError


class WXBizMsgCrypt(object):
    def __init__(self, signature, msg_signature, timestamp, nonce):
        self.signature = signature
        self.msg_signature = msg_signature
        self.timestamp = timestamp
        self.nonce = nonce

    def encrypt(self, body_text):
        conf = WechatConf(
            token='HingLo',
            appid='wx83f0d8afba67e8c1',
            appsecret='b455d3e1790a62bcd3f4aa16d3cd1dcf',
            encrypt_mode='safe',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
            encoding_aes_key='mTcmKtjfiDD66iDlz7Mq2yIDHGSXkBoNJKDmFJTNxis'  # 如果传入此值则必须保证同时传入 token, appid
        )
        wechat = WechatBasic(conf=conf)
        if wechat.check_signature(self.signature, self.timestamp, self.nonce):
            try:
                print(type(body_text))
                wechat.parse_data(body_text, self.msg_signature, self.timestamp, self.nonce)
                return 0, wechat.message.raw
            except ParseError as e:
                print(e)
        else:
            print('Wrong')
