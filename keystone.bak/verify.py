#coding=utf-8
__author__ = 'cy-openstack'
from configparser import ConfigParser

import keystoneclient.v2_0.client as ksclient

cfg=ConfigParser()
cfg.read(u'keystone.ini')

class KeystoneClientWorker(object):
    '''
    封装并扩展keystoneclient客户端能够完成的操作
    '''
    def __init__(self,auth_url,token=None,username=None,password=None):
        if not token:
            if not username or not password:
                SystemExit(u'Need token or username and password')
        if token:
            self.keystone=ksclient.Client(token=token,endpoint=auth_url)
        else:
            self.keystone=ksclient.Client(username=username,password=password,auth_url=auth_url)
        pass

    def getToken(self):
        '''
        获得Token
        '''
        return self.keystone.auth_token

    def getClient(self):
        '''
        获得keystone客户端
        '''
        return self.keystone

def createAdmin():
    '''
    以keystone创建一个管理员身份并返回
    :return:
    '''
    auth_url=cfg.get(u'auth',u'auth_url')
    username=cfg.get(u'auth',u'username')
    password=cfg.get(u'auth',u'password')
    tenant_name=cfg.get(u'auth',u'tenant_name')
    keystone=ksclient.Client(auth_url=auth_url,username=username,password=password)
    #print keystone.users.find()
    print keystone
    print keystone.auth_token
    #print keystone.tenants.list()
    return keystone

if __name__=="__main__":
    createAdmin()