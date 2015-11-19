#coding=utf-8
__author__ = 'cy-openstack'
from configparser import ConfigParser

from keystoneclient.v3 import client

cfg=ConfigParser()
cfg.read(u'keystone.ini')

class KeyStoneV3Worker(object):
    '''
    封装并扩展了keystoneclientv3
    '''
    def __init__(self,auth_url,username,password):
        self.keystone=client.Client(auth_url=auth_url,version=(3,),username=username,
                                    password=password)
    def test(self):
        print type(self.keystone)


if __name__=="__main__":
    auth_url=cfg.get(u'auth',u'auth_url')
    username=cfg.get(u'auth',u'username')
    password=cfg.get(u'auth',u'password')
    a=KeyStoneV3Worker(auth_url,username,password)
    a.test()