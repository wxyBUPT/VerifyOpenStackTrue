__author__ = 'cy-openstack'
print u'这个文件现在还没有用到，还没有更改现在的bug'
from . import authInfo

import pprint
from openstackClient import AuthInfo
if __name__=="__main__":
    authInfo=AuthInfo()
    service_list=authInfo.get_service_list()
    print service_list


