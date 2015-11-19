#coding=utf-8
__author__ = 'wxy'
from . import unittest
from builder.builder import Builder

class TestBuilder(unittest.TestCase):
    def test_net_builder(self):
        builder=Builder()
        builder.net_builde()
        builder.instance_build()
        for instance in builder.instances:
            print instance.name


