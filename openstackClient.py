#coding=utf-8
import os
import sys
from httplib import HTTPConnection, HTTPSConnection
import ast
import json
import time
nova_api_host = '172.16.138.138'
nova_api_port = '8774'

class OpenstackClient(object):
    def __init__(self, host, scheme, port):
        self.header = {}
        if scheme == 'http':
            self.conn = HTTPConnection(host, port)
        elif scheme == 'https':
            self.conn = HTTPSConnection(host, port)

    def round_tripper(self, method, path, body=None):
        if not body:
            body = ''
        self.conn.request(method, path, body, self.header)

        resp = self.conn.getresponse()
        #print resp.getheaders()
        #print resp
        return resp

    def call_with_body(self, method, path, body, content_type, content_length, headers):
        if headers:
           self.set_headers(headers)
        if content_type:
            self.add_header('Content-Type', content_type)
        if content_length:
            self.add_header('Content-Length', content_length)
        resp = self.round_tripper(method, path, body)
        return resp

    def call_only_header(self, method, path, content_type, headers):
        if headers:
            self.set_headers(headers)
        if content_type:
            self.add_header('Content-Type', content_type)
        return self.round_tripper(method, path, body=None)

    def set_headers(self, headers):
        self.header.update(headers)

    def add_header(self, k, v):
        self.header[k] = v

def get_token():
    #auth_host = '172.16.138.138'
    auth_host='180.97.185.114 '
    auth_port = '35357'
    auth_path = '/v2.0/tokens'
    auth_headers = {'Accept': 'application/json','User-Agent': 'python-novaclient'}
    content_type = 'application/json'
    client_auth = OpenstackClient(auth_host, 'http', auth_port)
    auth_body = '{"auth": {"tenantName": "admin",\
    "passwordCredentials":{"username":"admin","password":"57af19784cde8c7b"}}}'
    resp = client_auth.call_with_body('POST',auth_path,auth_body,content_type,len(auth_body),auth_headers)
    auth_result = resp.read()
    auth_result = json.loads(auth_result)
    auth_token = auth_result['access']['token']['id']
    return auth_token

def get_auth_resp():
    auth_host = '172.16.138.138'
    #auth_host='180.97.185.114 '
    auth_port = '35357'
    auth_path = '/v2.0/tokens'
    auth_headers = {'Accept': 'application/json','User-Agent': 'python-novaclient'}
    content_type = 'application/json'
    client_auth = OpenstackClient(auth_host, 'http', auth_port)
    auth_body = '{"auth": {"tenantName": "admin",\
    "passwordCredentials":{"username":"admin","password":"57af19784cde8c7b"}}}'
    #print auth_body
    resp = client_auth.call_with_body('POST',auth_path,auth_body,content_type,len(auth_body),auth_headers)
    return resp

#下面的类中又一处硬编码，如果不是硬编码相应的部分需要改正
class AuthInfo(object):
    '''
    获得auth相关的信息
    '''

    def __init__(self,auth_host='172.16.138.138',auth_port='35357',auth_path='/v2.0/tokens',
                 tenantName="admin",username="admin",password="57af19784cde8c7b"):
        '''
        初始化
        :param auth_host: 提供认证服务的地址，例如 '172.16.138.138'
        :param auth_port:
        :param auth_path:
        :param tenantName:
        :param username:
        :param password:
        :return:
        '''
        #auth_body='{"auth": {"tenantName": "{0}","passwordCredentials":{"username":"{1}","password":"{2}"}}}'.format(tenantName,username,password)
        passwordCredentials={}
        passwordCredentials['username']=username
        passwordCredentials['password']=password
        auth={}
        auth['tenantName']=tenantName
        auth['passwordCredentials']=passwordCredentials
        auth_body={}
        auth_body['auth']=auth
        auth_body=json.dumps(auth_body)
        auth_headers = {'Accept': 'application/json','User-Agent': 'python-novaclient'}
        content_type='application/json'
        client_auth=OpenstackClient(auth_host,'http',auth_port)
        self.auth_resp=client_auth.call_with_body('POST',auth_path,auth_body,content_type,len(auth_body),auth_headers)
        tmp=self.auth_resp.read()
        self.auth_resault=json.loads(tmp)


    #def __init__(self):
    #    self.auth_resp=get_auth_resp()
    #   resault=self.auth_resp.read()
    #    self.auth_resault=json.loads(resault)

    def get_token(self):
        '''
        获得认证token
        :return:
        '''
        return self.auth_resault['access']['token']['id']

    def get_service_list(self):
        '''
        获得在auth注册的服务的列表
        :return:
        '''
        serviceList=[]
        for service in self.auth_resault['access']['serviceCatalog']:
            tmp={}
            tmp['name']=service['name']
            tmp['adminURL']=service['endpoints'][0]['adminURL']
            tmp['id']=service['endpoints'][0]['id']
            serviceList.append(tmp)
        return serviceList

    def get_tenant(self):
        '''
        返回租户的信息
        :return:
        '''
        return self.auth_resault['access']['token']['tenant']

    def get_tenant_id(self):
        tenant=self.get_tenant()
        return tenant['id']

def action_detail(auth_token):
    api_path = '/v2/fc170b1b8a9a467b9e1a63d85ced5a86/servers/detail'
    api_headers = {'Accept': 'application/json', 'X-Auth-Project-Id':\
    'admin','User-Agent':'python-novaclient','X-Auth-Token':auth_token}
    api_body = None
    client_api = OpenstackClient(nova_api_host, 'http', nova_api_port)
    content_type = 'application/json'
    resp = client_api.call_only_header('GET', api_path, content_type , api_headers)
    api_result = resp.read()
    print api_result

def change_password(auth_token=None):
    if len(sys.argv) < 2:
        print "please input the instance UUID"
        sys.exit(1)
    instance = sys.argv[1]
    print instance
    api_path='/v2/fc170b1b8a9a467b9e1a63d85ced5a86/servers/%s/action'%instance
    print api_path
    api_headers = {'Accept': 'application/json', 'X-Auth-Project-Id':\
                    'admin','User-Agent':'python-novaclient','X-Auth-Token':auth_token}
    api_body = '{"changePassword": {"adminPass": "8888"}}'
    client_api = OpenstackClient(nova_api_host, 'http', nova_api_port)
    resp = client_api.call_with_body('POST',api_path,\
    api_body,'application/json',len(api_body),api_headers)
    get_result = resp.read()
    print get_result

def instances_list(auth_token=None):
    api_path = '/v2/fc170b1b8a9a467b9e1a63d85ced5a86/servers'
    api_headers = {'Accept': 'application/json', 'X-Auth-Project-Id':\
                    'admin','User-Agent':'python-novaclient','X-Auth-Token':auth_token}
    client_api = OpenstackClient(nova_api_host, 'http', nova_api_port)
    resp = client_api.call_only_header('GET',api_path,\
    'application/json',api_headers)
    get_result = resp.read()
    print get_result

def images_list(auth_token=None):
    api_path = '/v2/images'
    api_headers = {'Accept': 'application/json', 'X-Auth-Project-Id':\
                    'admin','User-Agent':'python-novaclient','X-Auth-Token':auth_token}
    client_api = OpenstackClient('172.16.138.138', 'http', '9292')
    resp = client_api.call_only_header('GET',api_path,\
    'application/json',api_headers)
    get_result = resp.read()
    print get_result

def cached_images_list(auth_token=None):
    api_path = '/v2/cached-images'
    api_headers = {'Accept': 'application/json', 'X-Auth-Project-Id':\
                    'admin','User-Agent':'python-novaclient','X-Auth-Token':auth_token}
    client_api = OpenstackClient('172.16.138.138', 'http', '9292')
    resp = client_api.call_only_header('GET',api_path,\
    'application/json',api_headers)
    get_result = resp.read()
    print get_result

if __name__ == '__main__':
    pass