#coding=utf-8
'''
create net by configure file
'''
__author__ = 'cy-openstack'
import logging
import logging.config

logging.config.fileConfig('logger.ini')
logger=logging.getLogger('root')

class NetBuilder(object):
    '''
    创建网络，并验证所创建的网络是否可以通信的工具
    '''
    def __init__(self):
        pass




