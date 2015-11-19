#coding=utf-8
__author__ = 'cy-openstack'
import sys
sys.path.append('..')
import unittest
from configparser import ConfigParser

from keystone.verify import KeystoneClientWorker

class TestKeystoneClientWorker(unittest.TestCase):
    def setUp(self):
        cfg=ConfigParser()
        cfg.read('keystone.ini')
        auth_url=cfg.get(u'auth',u'auth_url')
        username=cfg.get(u'auth',u'username')
        password=cfg.get(u'auth',u'password')
        self.keystoneClientWorker=KeystoneClientWorker(auth_url,username=username,
                                                       password=password)
    def tearDown(self):
        self.keystoneClientWorker=None

    def testGetToken(self):
        print u'产生了一个token'
        token=self.keystoneClientWorker.getToken()
        self.assertIsNotNone(token)
        print token

    def testGetClient(self):
        print u'测试是否成功的返回了一个认证客户端'
        auth_url=self.keystoneClientWorker.getClient().auth_url
        print u'auth_url是 {}'.format(auth_url)
        self.assertIsNotNone(auth_url)

    def testKeyStoneAttri(self):
        attris=dir(self.keystoneClientWorker)
        for key in attris:
            tmp=getattr(self.keystoneClientWorker,key)
            print '{}是'.format(key)
            #print tmp
            #print getattr(self.keystoneClientWorker,key)


if __name__=="__main__":
    unittest.main()