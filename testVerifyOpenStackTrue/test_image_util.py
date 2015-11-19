#coding=utf-8
__author__ = 'cy-openstack'
import unittest
import json
import pprint
from glance.imageUtil import ImageUtil

from . import auth_token
imageUtil=ImageUtil(auth_token)
class TestImageUtil(unittest.TestCase):
    def test_get_images(self):
        resp=imageUtil.get_images()
        cont=resp.read()
        tmp=json.loads(cont)
        pprint.pprint(tmp)

if __name__=="__main__":
    unittest.main()