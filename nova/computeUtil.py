#coding=utf-8
'''
对创建主机的操作执行封装
'''
__author__ = 'cy-openstack'
import json

from openstackClient import OpenstackClient
class ComputeUtil(object):
    '''
    有关创建主机
    '''
    def __init__(self,auth_token,tenant_id,nova_api_host='172.16.138.138',
                 nova_api_port='8774'):
        self.auth_token=auth_token
        self.tenant_id=tenant_id
        self.api_headers={'Accept':'application/json','X-Auth-Project-Id':
                          'admin','User-Agent':'python-neutronclient',
                          'X-Auth-Token':auth_token}
        self.nova_client=OpenstackClient(nova_api_host,'http',nova_api_port)

    def __get_method(self,api_path):
        resp=self.nova_client.call_only_header('GET',api_path,'application/json',self.api_headers)
        return resp

    def __put_method(self,api_path,api_body):
        resp=self.nova_client.call_with_body('PUT',api_path,api_body,'application/json',
                                                len(api_body),self.api_headers)
        return resp

    def __post_method(self,api_path,api_body):
        resp=self.nova_client.call_with_body('POST',api_path,api_body,'application/json',
                                                len(api_body),self.api_headers)
        return resp


    def get_servers(self):
        '''
        获得主机列表
        '''
        api_path='/v2/{0}/servers'.format(self.tenant_id)
        return self.__get_method(api_path)

    def get_servers_detail(self):
        '''
        获得主机列表的详细信息
        '''
        api_path='/v2/{0}/servers/detail'.format(self.tenant_id)
        return self.__get_method(api_path)

    def create_server(self,imageRef,flavorRef,name,networks,medata={}):
        '''
        创建主机
        '''
        api_path='/v2/{tenant_id}/servers'.format(
            tenant_id=self.tenant_id
        )
        server={}
        server['name']=name
        server['imageRef']=imageRef
        server['flavorRef']=flavorRef
        server['metadata']=medata
        server['networks']=networks
        tmp={}
        tmp['server']=server
        api_body=json.dumps(tmp)
        return self.__post_method(api_path,api_body)

    def delete_server(self,server_id):
        '''
        删除主机
        '''
        api_path='/v2.1/{0}/servers/{1}'.format(
            self.tenant_id,server_id
        )
        self.nova_client.call_only_header('DELETE',api_path
                                          ,'application/json',self.api_headers)


class FlavorUtil(object):
    '''
    有关flavors
    '''
    def __init__(self,auth_token,tenant_id,nova_api_host='172.16.138.138',
                 nova_api_port='8774'):
        self.auth_token=auth_token
        self.tenant_id=tenant_id
        self.api_headers={'Accept':'application/json','X-Auth-Project-Id':
                          'admin','User-Agent':'python-neutronclient',
                          'X-Auth-Token':auth_token}
        self.nova_client=OpenstackClient(nova_api_host,'http',nova_api_port)

    def __get_method(self,api_path):
        resp=self.nova_client.call_only_header('GET',api_path,'application/json',self.api_headers)
        return resp

    def __put_method(self,api_path,api_body):
        resp=self.nova_client.call_with_body('PUT',api_path,api_body,'application/json',
                                                len(api_body),self.api_headers)
        return resp

    def __post_method(self,api_path,api_body):
        resp=self.nova_client.call_with_body('POST',api_path,api_body,'application/json',
                                                len(api_body),self.api_headers)
        return resp

    def get_flavors(self):
        api_path='/v2/{tenant_id}/flavors'.format(tenant_id=self.tenant_id)
        print api_path
        return self.__get_method(api_path)

    def get_flavor_details(self,flavor_id):
        '''
        根据flavor_id显示详细信息
        :param flavor_id:
        :return:
        '''
        api_path='/v2.1/{tenant_id}/flavors/{flavor_id}'.format(
            tenant_id=self.tenant_id,flavor_id=flavor_id
        )
        return self.__get_method(api_path)

    def get_flavors_details(self):
        api_path='/v2/{tenant_id}/flavors/detail'.format(
            tenant_id=self.tenant_id
        )
        #print api_path
        return self.__get_method(api_path)

