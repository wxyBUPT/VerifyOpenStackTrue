#coding=utf-8
__author__ = 'cy-openstack'
print u'在openstackClient的AuthInfo处有一个硬编码需要解决'
import unittest
from configparser import ConfigParser
from pprint import pprint
import json
import time

from openstackClient import AuthInfo
from neutron.networkUtil import NetworkUtil,SubnetUtil

cfg=ConfigParser()
cfg.read('global.ini')
host=cfg.get('auth','host')
port=cfg.get('auth','port')
username=cfg.get('auth','user_name')
password=cfg.get('auth','password')
tenant=cfg.get('auth','tenant')
auth_path=cfg.get('auth','path')
auth_token=None

class Test000AuthInfo(unittest.TestCase):
    '''
    这个测试最先被执行，并产生auth_token
    '''
    def setUp(self):
        self.authInfo=AuthInfo()
        pass

    def tearDown(self):
        self.authInfo=None

    #def test_get_token(self):
    #    global auth_token
    #    auth_token=self.authInfo.get_token()
    #    self.assertIsNotNone(auth_token)
    #    print u'获得token为{ }'.format(auth_token)

    #def test_service_list(self):
    #   serviceList=self.authInfo.get_service_list()
    #   print u'有如下服务注册在keystone中'
    #    for service in serviceList:
    #        print service['name']
    def test_get_token(self):
        global auth_token
        auth_token=self.authInfo.get_token()
        print auth_token

    def test_get_service_list(self):
        service_list=self.authInfo.get_service_list()
        return service_list
        #pprint(service_list)
        #do futher things

class Test001NetworkUtil(unittest.TestCase):
    '''
    测试NetworkUtil
    '''
    def __get_exist_net_id_list(self):
        print u'执行 get_exist_net_id_list'
        #print u'执行了获得网络id列表'
        resp=self.networkUtil.get_networks()
        #print u'foo'
        resDict=json.loads(resp.read())
        networks=resDict['networks']
        exist_net_id_list=[network['id'] for network in networks]
        #print u'执行获得网络id列表成功'
        print u'执行成功'
        return exist_net_id_list

    def setUp(self):
        print u'执行setUp'
        global auth_token
        self.networkUtil=NetworkUtil(auth_token,'172.16.138.138','9696')
        #当前已经有的网络id列表
        self.exist_net_id_list=self.__get_exist_net_id_list()
        #print u'目前已经有的网络'
        #print self.exist_net_id_list

    def test_get_networks(self):
        print u'执行了get_networks'
        resp=self.networkUtil.get_networks()
        resjson=json.loads(resp.read())
        #print type(resjson)
        #pprint(resjson)
        #do more work here

    def test_create_network(self):
        print u'执行create_network'
        resp=self.networkUtil.create_network('net01')
        resjson=json.loads(resp.read())
        #pprint(resjson)
        #do more work here

    def test_create_networks(self):
        print u'执行了 create_networks'
        names=['example01','example02']
        resp=self.networkUtil.create_networks(names)
        resjson=json.loads(resp.read())
        #print u'创建网络成功'
        #pprint(resjson)
        #do more work here

    def test_show_network(self):
        print u'执行了 show_network'
        resp=self.networkUtil.show_network('36b92d77-efd9-4d30-af9f-b264656bf3cc')
        resjson=json.loads(resp.read())
        #pprint(resjson)

    def test_change_network(self):
        print u'执行了 change_network'
        net={}
        net['name']="changed_network_name"
        tmpDict={}
        tmpDict['network']=net
        api_body=json.dumps(tmpDict)
        resp=self.networkUtil.change_network('36b92d77-efd9-4d30-af9f-b264656bf3cc',api_body)
        #print u'更改网络名称后的网络'
        #print resp.read()
        #resjson=json.loads(resp.read())
        #pprint(resjson)

    def test_delete_network(self):
        print u'执行了delete_network'
        resp=self.networkUtil.delete_network('041bd6d1-7897-4034-81e7-443aa13619f3')
        #print resp.read()

    def rm_nets(self):
        print u'执行了rm_nets'
        self.networkUtil.delete_networks(self.exist_net_id_list)
        print u'删除所有网络成功'
        pass

    def tearDown(self):
        #下面两行是一个耗时比较大的操作，之后可以优化
        print u'执行tearDown'
        self.networkUtil=None
        #cur_exist_net_list=self.__get_exist_net_id_list()
        #print cur_exist_net_list
        #del_net_list=[netid for netid in cur_exist_net_list if netid not in self.exist_net_id_list]
        #print u'下面的网络需要删除'
        #print del_net_list
        #print self.exist_net_id_list
        #self.networkUtil.delete_networks(self.exist_net_id_list)
        #self.networkUtil=None

class Test002SubnetUtile(unittest.TestCase):
    '''
    测试子网
    '''
    def __get_cur_subnets(self):
        '''
        获得当前子网的列表
        :return:
        '''
        pass

    def setUp(self):
        '''
        初始化，列出当前的subNet
        :return:
        '''
        self.subNetUtil=SubnetUtil(auth_token)
        pass

    def tearDown(self):
        '''

        :return:
        '''
        self.subNetUtil=None

    def test_get_subnets(self):
        resp=self.subNetUtil.get_subnets()
        print resp.read()

    def test_create_sub_net_for(self):
        '''
        测试create_sub_net_for
        :return:
        '''
        print u'为网络创建了一个sub_net'
        resp=self.subNetUtil.create_sub_net_for('21d58779-e5a4-45f2-ba7c-bbdd43e57ca1','10.0.0.1/24')
        print resp.read()
        print u'为网络创建一个sub_net完毕'

if __name__=="__main__":
    unittest.main()