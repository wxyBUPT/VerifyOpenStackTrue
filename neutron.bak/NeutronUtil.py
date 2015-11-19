#coding=utf-8
__author__ = 'cy-openstack'

import logging
import neutronclient.v2_0.client as neclient

class NeutronUtil(object):
    '''
    封装neutronclient的功能以满足验证组网的需求
    '''
    def __init__(self,endpoint_url,token):
        '''
        初始化
        :return:
        '''
        self.neutronClient=neclient.Client(token=token,endpoint_url=endpoint_url)
        print u'下面是auth info'
        print self.neutronClient.get_auth_info()
        pass

    def _getToken(self):
        pass

    def _updateToken(self):
        '''
        当token超时时重新获得token
        :return:
        '''
        pass

    def _updateNeturnClient(self):
        '''
        出现neturnClient失效时更新neturnClient
        :return:
        '''
        pass

    def createNetwork(self,networkList):
        '''
        根据netWorkList列表中的信息创建网络
        列表项为字典
        :param netWorkList:
        :return:
        '''
        self.neutronClient.format='json'
        for network in networkList:
            self.neutronClient.create_network({'network':network})

    def getNetworkByName(self,netNames):
        '''
        根据生成器中的名字生成network
        :param netNameList:
        :return:
        '''
        for netName in netNames:
            yield self.neutronClient.list_networks(name=netName)

    def test(self):
        self.neutronClient


