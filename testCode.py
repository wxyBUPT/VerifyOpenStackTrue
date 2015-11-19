#coding=utf-8
__author__ = 'cy-openstack'
import unittest
from configparser import ConfigParser

from keystone.verify import KeystoneClientWorker
from neutron.NeutronUtil import NeutronUtil

cfg=ConfigParser()
cfg.read('global.ini')
auth_url=cfg.get(u'keystone',u'auth_url')
auth_url=cfg.get(u'keystone',u'auth_url')
username=cfg.get(u'keystone',u'username')
password=cfg.get(u'keystone',u'password')
keystoneClientWorker=KeystoneClientWorker(auth_url,username=username,password=password)
token=keystoneClientWorker.getToken()

class TestKeystone(unittest.TestCase):
    def setUp(self):
        self.keystoneClientWorker=keystoneClientWorker

    def tearDown(self):
        self.keystoneClientWorker=None

    def testGetToken(self):
        print u'验证在顶层文件产生额token是否为空'
        token=self.keystoneClientWorker.getToken()
        self.assertIsNotNone(token)
        print token
        return token

    def testGetClient(self):
        print u'测试是否成功的返回了一个认证客户端'
        auth_url=self.keystoneClientWorker.getClient().auth_url
        print u'auth_url是 {}'.format(auth_url)
        self.assertIsNotNone(auth_url)

class TestNeutronUtil(object):
    '''
    测试网络部分的功能与内容
    '''
    def setUp(self):
        endpoint_url=cfg.get(u'neutron',u'os_url')
        self.neutronUtil=NeutronUtil(endpoint_url=endpoint_url,token=token)
    def tearDown(self):
        self.neutronUtil=None

    def testCreateNetWork(self):
        print u'执行创建网络测试'
        networkList=({'name':'firstnet','admin_state_up':True},{'name':'secondnet','admin_state_up':True},
                     {'name':'thirdnet','admin_state_up':True},)
        self.neutronUtil.createNetwork(networkList)
        netNames=(network['name'] for network in networkList)
        for net in self.neutronUtil.getNetworkByName(netNames):
            self.assertIsNotNone(net)

import keystoneclient.v2_0.client as kClient

class TestKeystone(unittest.TestCase):
    def setUp(self):
        self.keystone=kClient.Client(token=token,endpoint='http://172.16.138.138:35357/v2.0')
    def tearDown(self):
        self.keystone=None
    def test00(self):
        print u'执行了这个测试'
        print self.keystone.tenants
        print dir(self.keystone.tenants)
        print self.keystone.tenants.findall()

if __name__=="__main__":
    unittest.main()
