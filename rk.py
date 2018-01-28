#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5


class RClient(object):

    def __init__(self, username, password, soft_id='96247', soft_key='f5d5fac6be5c4929826d51caa3b8d131'):
        self.username = username
        self.password = md5(password.encode('utf8')).hexdigest()
        self.soft_id = soft_id
        self.soft_key = soft_key
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, im, im_type, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
        return r.json()

    def rk_report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return r.json()


def getVerfyCode(username,password,data):
    #data 图片file.read结果
    #返回识别结果
    rc = RClient(username, password)
    return(rc.rk_create(data,3040))
    

    



if __name__ == '__main__':
    rc = RClient('username', 'password')
    im = open('a.jpg', 'rb').read()
    print(rc.rk_create(im, 3040))

