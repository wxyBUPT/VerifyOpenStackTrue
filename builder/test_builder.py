__author__ = 'wxy'
import unittest
from builder import Builder
class TestBuilder(unittest.TestCase):
    def test_net_builder(self):
        builder=Builder()
        builder.net_builde()
        builder.instance_build()
        for instance in builder.instances:
            print instance.name
