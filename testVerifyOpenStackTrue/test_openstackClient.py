#coding=utf-8
__author__ = 'wxy'

from . import unittest,json,pprint,authInfo

class TestAuthInfo(unittest.TestCase):
    print authInfo.get_token()



