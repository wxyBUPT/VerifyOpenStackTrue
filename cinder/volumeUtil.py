#coding=utf-8
__author__ = 'cy-openstack'
'''
对卷存储进行操作
'''
from openstackClient import OpenstackClient
import json

class VolumeUtil(object):
    '''
    创建卷存储相关
    '''
    def __init__(self,auth_token,cinder_api_host='172.16.138.138',
                 cinder_api_port='8776'):
        self.auth_token=auth_token
        self.api_headers={'Accept':'application/json','X-Auth-Project-Id':
                          'admin','User-Agent':'python-cinderclient',
                          'X-Auth-Token':auth_token}
        self.cinder_client=OpenstackClient(cinder_api_host,'http',cinder_api_port)

    def __get_method(self,api_path):
        resp=self.cinder_client.call_only_header('GET',api_path,'application/json',
                                                 self.api_headers)
        return resp

    def __put_method(self,api_path,api_body):
        resp=self.cinder_client.call_with_body('PUT',api_path,api_body,
                                               'application/json',
                                                len(api_body),self.api_headers)
        return resp

    def __post_method(self,api_path,api_body):
        resp=self.cinder_client.call_with_body('POST',api_path,api_body,
                                               'application/json',
                                                len(api_body),self.api_headers)
        return resp

    def get_volumes(self,tenant_id):
        api_path='/v2/{tenant_id}/volumes'.format(tenant_id=tenant_id)
        return self.__get_method(api_path)

    def create_volumes(self,tenant_id,size):
        api_path='/v2/{tenant_id}/volumes'.format(tenant_id=tenant_id)
        volume={}
        volume['size']=size
        tmp={}
        tmp['volume']=volume
        api_body=json.dumps(tmp)
        return self.__post_method(api_path,api_body)