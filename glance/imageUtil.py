#coding=utf-8
'''
对创建主机的操作执行封装
'''
__author__ = 'cy-openstack'
from openstackClient import OpenstackClient
class ImageUtil(object):
    '''
    有关创建主机
    '''
    def __init__(self,auth_token,glance_api_host='172.16.138.138',
                 glance_api_port='9292'):
        self.auth_token=auth_token
        self.api_headers={'Accept':'application/json','X-Auth-Project-Id':
                          'admin','User-Agent':'python-glanceclient',
                          'X-Auth-Token':auth_token}
        self.glance_client=OpenstackClient(glance_api_host,'http',glance_api_port)

    def __get_method(self,api_path):
        resp=self.glance_client.call_only_header('GET',api_path,'application/json',self.api_headers)
        return resp

    def __put_method(self,api_path,api_body):
        resp=self.glance_client.call_with_body('PUT',api_path,api_body,
                                               'application/json',
                                                len(api_body),self.api_headers)
        return resp

    def __post_method(self,api_path,api_body):
        resp=self.glance_client.call_with_body('POST',api_path,api_body,
                                               'application/json',
                                                len(api_body),self.api_headers)
        return resp

    def get_images(self):
        '''
        请求获得images 的详细信息
        :return:
        '''
        api_path='/v2/images'
        return self.__get_method(api_path)