#coding=utf-8
__author__ = 'cy-openstack'

from . import networkUtil,unittest,json,pprint,portsUtil

class TestNetWorkUtil(unittest.TestCase):
    def test_get_networks(self):
        res=networkUtil.get_networks()
        resstr=res.read()
        resjson=json.loads(resstr)
        pprint(resjson)

class TestPortUtil(unittest.TestCase):
    def notest_get_ports(self):
        res=portsUtil.get_ports()
        resstr=res.read()
        resjson=json.loads(resstr)
        pprint(resjson)

    def test_create_port_for_network(self):
        # f6d20bb5-40fd-4d61-83a3-d20404f07874
        res=portsUtil.create_port_for_network('5109a171-0d68-4ab5-8447-2fc20f040f2e')







