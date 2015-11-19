#coding=utf-8
__author__ = 'cy-openstack'
import unittest
import json
from pprint import pprint

from cinder.volumeUtil import VolumeUtil
from glance.imageUtil import ImageUtil
from neutron.networkUtil import NetworkUtil,SubnetUtil,PortsUtil
from nova.computeUtil import ComputeUtil,FlavorUtil
from openstackClient import AuthInfo

authInfo=AuthInfo()
auth_token=authInfo.get_token()
tenant_id=authInfo.get_tenant_id()

volumeUtil=VolumeUtil(auth_token)
imageUtil=ImageUtil(auth_token)
networkUtil=NetworkUtil(auth_token)
subnetUtil=SubnetUtil(auth_token)
portsUtil=PortsUtil(auth_token)
computeUtil=ComputeUtil(auth_token,tenant_id)
flavorUtil=FlavorUtil(auth_token,tenant_id)
