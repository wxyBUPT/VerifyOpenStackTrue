#coding=utf-8
__author__ = 'wxy'
import logging
import logging.config
import uuid
from configparser import ConfigParser
gconf=ConfigParser()
gconf.read('./global.ini')
blog=logging.getLogger('builder')

print gconf.sections()

#日志
logging.config.fileConfig('logger.ini')
uuidtag=uuid.uuid1()

#认证
from openstackClient import AuthInfo

authInfo=AuthInfo(auth_host=str(gconf.get('auth','host')),
                  auth_port=str(gconf.get('auth','port')),
                  auth_path=str(gconf.get('auth','path')),
                  tenantName=str(gconf.get('auth','tenant')),
                  username=str(gconf.get('auth','user_name')),
                  password=str(gconf.get('auth','password')))

auth_token=authInfo.get_token()
tenant_id=authInfo.get_tenant_id()
print u'uuid : {}'.format(uuidtag)
blog.info(u'auth_token : {} uuid : {}'.format(auth_token,uuidtag))

#数据结构的公共基类
class Structure:
    _fields=[]
    def __init__(self,*args):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        #Set the arguments
        for name,value in zip(self._fields,args):
            setattr(self,name,value)

#为了在 build 阶段多次实例化各种 Util ，所以将所有的 Util 实例化在这里完成
from neutron import NetworkUtil,PortsUtil,SubnetUtil
from nova import ComputeUtil,FlavorUtil
from cinder import VolumeUtil
_neutron_host=str(gconf.get('neutron','api_host'))
_neutron_port=str(gconf.get('neutron','api_port'))
_nova_host=str(gconf.get('nova','api_host'))
_nova_port=str(gconf.get('nova','api_port'))
_cinder_host=str(gconf.get('cinder','api_host'))
_cinder_port=str(gconf.get('cinder','api_port'))


