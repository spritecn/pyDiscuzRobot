#coding:utf8
#重载DiscuzReboot 实现验证码登录逻辑
#
import re
from time import sleep
import random
from DiscuzRobot import DiscuzRobot as DR
from DiscuzRobot import logging,LoginError,ParseError
from config import rk_user,rk_passwd,froum_url,froum_user,froum_passwd
from rk import getVerfyCode

class verfyDR(DR):
    def login(self):
        '''login and get forum'''
        login_url = self.forum_url + "member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&inajax=1"
        #print(login_url)
        login_data = {
            'username': self.username,
            'password': self.password,
            'answer': '',
            'cookietime': '2592000',
            'handlekey': 'ls',
            'questionid': '0',
            'quickforward': 'yes',
            'fastloginfield': 'username'
        }
        resp = self.session.post(login_url, login_data)
        if self.username in resp.text:
            #这个判断方法好牛！
            logging.info('%s - login succeed' % self.username)
            self.isLogin = True
            self.get_formhash()
        elif '验证码填写错误' in resp.text:
            #判断是否是因为有验证码的原因造成的不能登录
            logging.warning('verify code error')
            #raise LoginError("verfiy error.")
        else:
            logging.warning('%s - login failed' % self.username)
            raise LoginError("Wrong username or password.")

    def verfyLogin(self):
        #验证码识别登录
        verfyLogin_url = self.forum_url + 'member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login'
        verfyLogin_resp = self.session.get(verfyLogin_url)
        #获取idhash
        m = re.findall(r'<span id="seccode_(\w+)"></span>',verfyLogin_resp.text)
        idhash = m[0]
        m = re.findall(r"'loginform_(\w+)'",verfyLogin_resp.text)
        loginhash = m[0]
        self.session.headers.update({'Referer':f'{self.forum_url}forum.php'})
        while 1:
            #获取验证码地址
            verfryCodeUpdate_url = f'{self.forum_url}misc.php?mod=seccode&action=update&idhash={idhash}&{random.random()}&modid=member::logging'
            verfryCodeUpdate_resp = self.session.get(verfryCodeUpdate_url)
            m = re.findall(r'src="(\S+)"',verfryCodeUpdate_resp.text)
            verfryCodePic_url = f'{self.forum_url}{m[0]}'
            #下载验证码，并使用若快识别
            verfryCodePic_resp = self.session.get(verfryCodePic_url)
            getVerfryCode_result = getVerfyCode(rk_user,rk_passwd,verfryCodePic_resp.content)
            if not 'Error' in getVerfryCode_result:
                verfryCode = getVerfryCode_result['Result']
            else:
                #识别失败，重新下载，重试
                logging.warning(f'rk_{getVerfryCode_result["Error"]}')
                sleep(0.2)
                continue
            #提交验证码验证
            '''
            misc.php?mod=seccode&action=check&inajax=1&modid=member::logging&idhash=cSAxtYup6&secverify=396G
            '''
            postVerfyCode_url = f'{self.forum_url}misc.php?mod=seccode&action=check&inajax=1&modid=member::logging&idhash={idhash}&secverify={verfryCode}'
            postVerfyCode_resp = self.session.get(postVerfyCode_url)
            #print(postVerfyCode_resp.text)
            if not 'succeed' in postVerfyCode_resp.text:
                #验证码验证不通过
                logging.warning('error verifyCode')
                sleep(0.2)
                continue
            ###开始验证码登录
            verifyLogin_url = f'{self.forum_url}member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash={loginhash}&inajax=1'
            verifyLogin_data = {
                'formhash':self.formhash,
                'referer':f'{self.forum_url}forum.php',
                'loginfield':'username',
                'username':self.username,
                'password':self.password,
                'questionid':0,
                'answer':'',
                'seccodehash':idhash,
                'seccodemodid':'member::logging',
                'seccodeverify':verfryCode
            }
            verifyLogin_resp = self.session.post(verifyLogin_url,data=verifyLogin_data)
            print(verifyLogin_resp.text)
            input('')

            '''
            member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash=LTb44&inajax=1

            data:
            
            '''


    def getTest(self,url):
        resp = self.session.get(url)
        '''
        获取idhash
        <span id="seccode_cSAh9sx9C"></span>
        '''
        m = re.findall(r'<span id="seccode_(\w+)"></span>',resp.text)
        idhash = m[0]
        print(idhash)

if __name__ == '__main__':
    dr = verfyDR(froum_url,froum_user,froum_passwd)
    dr.login()
    test_url ='http://qkl.51fxt.com/discuz/member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login'
    verfryCode_url = 'http://qkl.51fxt.com/discuz/misc.php?mod=seccode&action=update&idhash=cSAIw0n8O&0.17623825167070462&modid=member::logging'
    verfryCodePic_url = 'http://qkl.51fxt.com/discuz/misc.php?mod=seccode&update=96454&idhash=cSAIw0n8O'
    dr.verfyLogin()
    