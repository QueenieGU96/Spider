#!/usr/bin/env python
# encoding: utf-8

"""
@author:
@contact:
@site:
@software: PyCharm
@file: music.py
@time: 2019
"""
import requests
import random, math
from Crypto.Cipher import AES
import base64
import codecs
import os
"""
接口依据2018年的教程；现已更改但愿接口未关闭
现接口：https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token=
"""


class Spider(object):
    def __init__(self):
        self.headers = {
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
                 'Cookie':'_iuqxldmzr_=32; _ntes_nnid=59096a5199b067c39039e318a72b6868,1539863032635; _ntes_nuid=59096a5199b067c39039e318a72b6868; WM_TID=mmDnP%2BiMnEtFQFAEVEcsKJV8r7daGwG5; nts_mail_user=gqx960528@163.com:-1:1; mail_psc_fingerprint=b2e2d3a8a6b746361fb476a3fc13bec7; usertrack=CrHudlvhqZ+k/6m/AxqhAg==; __utma=94650624.2003605371.1539863033.1544971406.1546971982.3; __utmz=94650624.1546971982.3.3.utmcsr=cnblogs.com|utmccn=(referral)|utmcmd=referral|utmcct=/; P_INFO=gqx960528@163.com|1551517349|0|mail163|00&99|gud&1551515851&mail_client#gud&440100#10#0#0|133921&0||gqx960528@163.com; JSESSIONID-WYYY=2GP7pWJ7Sn%2BUxONVgRCFiKuTfSfcccvW1tIs3RmmfC45%2F3wTnY%2BHdHPoEoIPFQD5gXtniHkuVeuuGBRJSpfH93Cc1kB3iXhVixKq4t5rn8b%5CiHAF3ec%2FhBe87YEOj9%2BHr4Uoijr8aOXOX3mHHz1%5ChRK28rSNI%2BZV28bOts6OV0gGMRaJ%3A1553004993049; WM_NI=6jXRfeiGqpxllEVSmFQ64VnZjVyVL8wCy9MCvD%2BbznMLRg0EBESgT6AyRUObjRlbU8%2Fe0iPY9xRqBTu6sfc1uEdm7kHOVBf21gvoO%2Bp3Il7mm1IrWy9BQZtRNcteQGnZMWQ%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eea6b64b898afeccd87fb0968ea7c44f869f9eaff361ad96a1a8e94e8bb5bba8c22af0fea7c3b92af6b698b3e56fab99bf91fb68b09b9ab4f04e93eafcb7ed52aa8ab7b7cf34b59db7dad049b69ce583f9668f949e88b34f829b9d88d73e83a79eb6ce6aaa8ea483d834edbb008ad353fba89e92c160b7eabd87e23bb79bac8eb6618c919aa3e53af3b9ba90ce21b4ed878db667afef8793d673fb9e9fbbf75a8ebdbc86d44dae8683b8d437e2a3'

        }

    def __get_songs(self, name):
        d = '{"hlpretag":"<span class=\\"s-fc7\\">","hlposttag":"</span>","s":"%s","type":"1","offset":"0","total":"true","limit":"30","csrf_token":""}' % name
        wyy = WangYiYun(d)    # 要搜索的歌曲名在这里
        data = wyy.get_data()
        url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        response = requests.post(url, data=data, headers=self.headers).json()
        return response['result']


    def __get_mp3(self, id):
        d = '{"ids":"[%s]","br":320000,"csrf_token":""}' % id
        wyy = WangYiYun(d)
        data = wyy.get_data()
        url = 'https://music.163.com/weapi/song/enhance/player/url?csrf_token='
        response = requests.post(url, data=data, headers=self.headers).json()
        print(response)
        return response['data'][0]['url']

    def __download_mp3(self, url, filename):
        """下载mp3"""
        abspath = os.path.abspath('.')  # 获取绝对路径
        os.chdir(abspath)
        response = requests.get(url, headers=self.headers).content
        path = os.path.join(abspath, filename)
        with open(filename + '.mp3', 'wb') as f:
            f.write(response)
            print('下载完毕,可以在%s   路径下查看' % path + '.mp3')

    def __print_info(self, songs):
        """打印歌曲需要下载的歌曲信息"""
        songs_list = []
        for num, song in enumerate(songs):
            print(num, '歌曲名字：', song['name'], '作者：', song['ar'][0]['name'])
            songs_list.append((song['name'], song['id']))
        return songs_list

    def run(self):
        while True:
            name = input('请输入你需要下载的歌曲名：')
            songs = self.__get_songs(name)
            if songs['songCount'] == 0:
                print('没有搜到此歌曲，请换个关键字')
            else:
                songs = self.__print_info(songs['songs'])
                num = input('请输入需要下载的歌曲，输入左边对应数字即可')
                url = self.__get_mp3(songs[int(num)][1])
                if not url:
                    print('歌曲需要收费，下载失败')
                else:
                    filename = songs[int(num)][0]
                    self.__download_mp3(url, filename)
                flag = input('如需继续可以按任意键进行搜歌，否则按0结束程序')
                if flag == '0':
                    break
        print('程序结束！')


class WangYiYun(object):
    def __init__(self, d):
        self.d = d
        self.e = '010001'
        self.f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5a" \
                 "a76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46be" \
                 "e255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        self.g = "0CoJUm6Qyw8W8jud"
        self.random_text = self.get_random_str()

    def get_random_str(self):
        """js中的a函数"""
        str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        res = ''
        for x in range(16):
            index = math.floor(random.random() * len(str))
            res += str[index]
        return res

    def aes_encrypt(self, text, key):
        iv = '0102030405060708'  # 偏移量
        pad = 16 - len(text.encode()) % 16  # 使加密信息的长度为16的倍数，要不会报下面的错
        # 长度是16的倍数还会报错，不能包含中文，要对他进行unicode编码
        text = text + pad * chr(pad)  # Input strings must be a multiple of 16 in length
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        msg = base64.b64encode(encryptor.encrypt(text))  # 最后还需要使用base64进行加密
        return msg

    def rsa_encrypt(self, value, text, modulus):
        '''进行rsa加密'''
        text = text[::-1]
        rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(value, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def get_data(self):
        # 这个参数加密两次
        params = self.aes_encrypt(self.d, self.g)
        params = self.aes_encrypt(params.decode('utf-8'), self.random_text)
        enc_sec_key = self.rsa_encrypt(self.e, self.random_text, self.f)
        return {
            'params': params,
            'encSecKey': enc_sec_key
        }


def main():
    spider = Spider()
    spider.run()


if __name__ == '__main__':
    main()
