#coding=utf-8
__author__ = 'cy-openstack'

from . import authInfo,auth_token,VolumeUtil,pprint,json,unittest
tenant_id=authInfo.get_tenant_id()
#print tenant_id



class TestVolumeUtil(unittest.TestCase):
    def test_get_volumes(self):
        volumeUtil=VolumeUtil(auth_token)
        volumeUtil.create_volumes(tenant_id,1)
        volumeUtil=VolumeUtil(auth_token)
        res=volumeUtil.get_volumes(tenant_id)
        cont=res.read()
        tmp=json.loads(cont)
        pprint(tmp)

