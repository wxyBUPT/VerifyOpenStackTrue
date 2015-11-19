#coding=utf-8
__author__ = 'cy-openstack'
import json

from openstackClient import OpenstackClient

class NetworkUtil(object):
    '''
    有关网络的操作
    '''
    def __init__(self,auth_token,neutron_api_host='172.16.138.138',
                 neutron_api_port='9696'):
        self.auth_token=auth_token
        self.api_headers={'Accept':'application/json','X-Auth-Project-Id':
                          'admin','User-Agent':'python-neutronclient',
                          'X-Auth-Token':auth_token}
        self.neutron_client=OpenstackClient(neutron_api_host,'http',
                                            neutron_api_port)

    def get_networks(self):
        '''
        获得网络相关信息
        :return:
        '''
        api_path='/v2.0/networks'
        resp=self.neutron_client.call_only_header('GET',api_path,'application/json',self.api_headers)
        return resp

    def create_network(self,name,admin_state_up=True):
        '''
        创建新的网络
        :param name: 网络的名称
        :param admin_state_up:
        :return:
        '''
        net={}
        net['name']=name
        net['admin_state_up']=admin_state_up
        body={}
        body['network']=net
        api_body=json.dumps(body)
        api_path='/v2.0/networks'
        resp=self.neutron_client.call_with_body('POST',api_path,api_body
                                                ,'application/json',len(api_body),
                                                self.api_headers)
        return resp

    def create_networks(self,name_list,admin_set_up=True):
        '''
        批量创建网络
        :param name_list:
        :param admin_set_up:
        :return:
        '''
        nets=[]
        for name in name_list:
            net={}
            net['name']=name
            net['admin_state_up']=admin_set_up
            nets.append(net)
        body={}
        body['networks']=nets
        api_body=json.dumps(body)
        api_path='/v2.0/networks'
        resp=self.neutron_client.call_with_body('POST',api_path,api_body,
                                                'application/json',len(api_body),
                                                self.api_headers)
        return resp

    def __get_method(self,api_path):
        resp=self.neutron_client.call_only_header('GET',api_path,'application/json',self.api_headers)
        return resp

    def __put_method(self,api_path,api_body):
        resp=self.neutron_client.call_with_body('PUT',api_path,api_body,'application/json',len(api_body),self.api_headers)
        return resp

    def show_network(self,net_id):
        '''
        显示网络信息
        :param net_id: net_id
        :return:
        '''
        api_path='/v2.0/networks/%s'%net_id
        return self.__get_method(api_path)

    def change_network(self,net_id,api_body):
        '''
        更改网络
        :param net_id:
        :param api_body:
        :return:
        '''
        api_path='/v2.0/networks/%s'%net_id
        resp=self.neutron_client.call_with_body('PUT',api_path,api_body,'application/json',len(api_body),self.api_headers)
        return resp

    def delete_network(self,net_id):
        '''
        删除网络,当这个网络还有端口的时候则不能删除这个网络
        :param net_id:
        :return:
        '''

        api_path='/v2.0/networks/%s'%net_id
        print u'删除网络%s'%api_path
        #print u'删除的api_path为'
        #print api_path
        resp=self.neutron_client.call_only_header('DELETE',api_path,'application/json',self.api_headers)
        return resp

    def delete_networks(self,net_id_list):
        '''
        批量删除网络
        :param net_id_list:
        :return:
        '''
        for net_id in net_id_list:
            self.delete_network(net_id)


class SubnetUtil(object):
    '''
    Lists，shows information for , create ,updates ,and deletes subnet resources.
    '''
    def __init__(self,auth_token,neutron_api_host='172.16.138.138',
                 neutron_api_port='9696'):
        self.auth_token=auth_token
        self.api_headers={'Accept':'application/json','X-Auth-Project-Id':
                          'admin','User-Agent':'python-neutronclient',
                          'X-Auth-Token':auth_token}
        self.neutron_client=OpenstackClient(neutron_api_host,'http',neutron_api_port)

    def __get_method(self,api_path):
        resp=self.neutron_client.call_only_header('GET',api_path,'application/json',self.api_headers)
        return resp

    def __put_method(self,api_path,api_body):
        resp=self.neutron_client.call_with_body('PUT',api_path,api_body,'application/json',
                                                len(api_body),self.api_headers)
        return resp

    def __post_method(self,api_path,api_body):
        resp=self.neutron_client.call_with_body('POST',api_path,api_body,'application/json',
                                                len(api_body),self.api_headers)
        return resp

    def get_subnets(self):
        return self.__get_method('/v2.0/subnets')

    def create_sub_net_for(self,network_id,cidr):
        '''
        为某个网络创建子网,目前只支持ipv4,目前未考虑ip地址非法
        :param network_id:为
        :param cidr:
        :return:
        '''
        api_path='/v2.0/subnets'
        subnet={}
        subnet['network_id']=network_id
        subnet['ip_version']=4
        subnet['cidr']=cidr
        tmp={}
        tmp['subnet']=subnet
        api_body=json.dumps(tmp)
        return self.neutron_client.call_with_body('POST',api_path,api_body,
                                                  'application/json',len(api_body),self.api_headers)

    def bulk_create_sub_net(self,subnetsDict):
        '''
        批量创建网络，但是因为目前没有实用价值还没有进行单元测试
        :param createDict: 需要创建的字典
        :return:
        '''
        api_path='/v2.0/subnets'
        tmp={}
        tmp['subnets']=subnetsDict
        api_body=json.dumps(tmp)
        return self.__post_method(api_path,api_body)

    def get_sub_net_by_id(self,subnet_id):
        '''
        根据sub_net的id来获得这个子网的情况
        :param network_id:
        :return:
        '''
        api_path='/v2.0/subnets/%s'%subnet_id
        return self.__get_method(api_path)

    def put_sub_net_by_id(self,subnet_id,confDict):
        '''

        :param confDict: 字典，转换为json格式如下
        {
            "subnet":{
                "name":"my_subnet"
            }
        }
        :return:
        '''
        api_path='/v2.0/subnets/%s'%subnet_id
        api_body=json.dumps(confDict)
        return self.__put_method(api_path,api_body)

    def deltee_sub_net_by_id(self,subnet_id):
        '''
        根据sub_net 的id删除网络
        :return:
        '''
        api_path='/v2.0/subnets/%s'%subnet_id
        return self.neutron_client.call_only_header('DELETE',api_path,'application/json',self.api_headers)

class PortsUtil(object):
    '''
    对端口执行操作的一系列动作
    '''
    def __init__(self,auth_token,neutron_api_host='172.16.138.138',
                 neutron_api_port='9696'):
        self.auth_token=auth_token
        self.api_headers={'Accept':'application/json','X-Auth-Project-Id':
                          'admin','User-Agent':'python-neutronclient',
                          'X-Auth-Token':auth_token}
        self.neutron_client=OpenstackClient(neutron_api_host,'http',neutron_api_port)

    def __get_method(self,api_path):
        resp=self.neutron_client.call_only_header('GET',api_path,'application/json',self.api_headers)
        return resp

    def __put_method(self,api_path,api_body):
        resp=self.neutron_client.call_with_body('PUT',api_path,api_body,'application/json',
                                                len(api_body),self.api_headers)
        return resp

    def __post_method(self,api_path,api_body):
        resp=self.neutron_client.call_with_body('POST',api_path,api_body,'application/json',
                                                len(api_body),self.api_headers)
        return resp

    def get_ports(self):
        api_path='/v2.0/ports'
        return self.__get_method(api_path)

    def create_port_for_network(self,network_id,admin_state_up=True):
        '''
        在网络中
        :param network_id:
        :param prot_name:
        :param admin_state_up:
        :return:
        '''
        port={}
        port['network_id']=network_id
        port['admin_state_up']=admin_state_up
        tmp={}
        tmp['port']=port
        api_body=json.dumps(tmp)
        api_path='/v2.0/ports'
        return self.__post_method(api_path,api_body)

    def get_port_by_id(self,port_id):
        api_path='/v2.0/ports/%s'%port_id
        return self.__get_method(api_path)

    def delete_port_by_id(self,port_id):
        api_path='/v2.0/ports/%s'%port_id
        self.neutron_client.call_only_header('DELETE',api_path,'application/json',
                                             self.api_headers)
