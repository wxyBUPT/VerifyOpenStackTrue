#coding=utf-8
__author__ = 'cy-openstack'
from . import flavorUtil,json,pprint,unittest

class TestFlavorUtil(unittest.TestCase):
    '''
    FlavorUtil的单元测试
    '''
    def test_get_flavors(self):
        res=flavorUtil.get_flavors()
        tmp=res.read()
        print u'测试FlavorUtil'
        tmp=json.loads(tmp)
        self.assertIsNotNone(tmp)
        #pprint(tmp)

    def test_get_flavors_details(self):
        res=flavorUtil.get_flavors_details()
        tmp=res.read()
        print u'测试获得flavors_details'
        tmp=json.loads(tmp)
        pprint(tmp)


