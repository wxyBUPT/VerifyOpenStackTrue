#coding=utf-8
__author__ = 'cy-openstack'

from . import authInfo,auth_token,\
    json,pprint,unittest,flavorUtil,imageUtil,computeUtil,portsUtil

class TestComputeUtil(unittest.TestCase):
    '''
    测试创建主机部分是否能够工作
    '''
    def test_get_servers(self):
        print u'测试获得主机信息'
        res=computeUtil.get_servers()
        res_body=res.read()
        #pprint(json.loads(res_body))

    def test_get_servers_detail(self):
        print u'测试获得主机详细信息'
        res=computeUtil.get_servers_detail()
        res_body=res.read()
        #pprint(json.loads(res_body))

    def test_zcreate_server(self):
        print u'测试创建主机'
        print u'通过硬编码测试'
        #f0a7d21a-aac5-4e4d-9ebb-71e2aac2c40a  image id
        # 1 flavor id
        # 0482ef5f-0bbe-410b-bb33-e469d447aa46 networ id
        metadata={}
        metadata['My Server Name']='KeyStoneServer'
        create_port_res=portsUtil.create_port_for_network('0482ef5f-0bbe-410b-bb33-e469d447aa46')
        portInfo=create_port_res.read()
        portInfo=json.loads(portInfo)
        print u'下面是portInfo'
        pprint(portInfo)
        portID=portInfo['port']['id']
        network={}
        network['uuid']='0482ef5f-0bbe-410b-bb33-e469d447aa46'
        network['port']=portID
        networks=[network,]
        res=computeUtil.create_server('f0a7d21a-aac5-4e4d-9ebb-71e2aac2c40a',
                                  '1',name='newNet',networks=networks)
        print res.status
        print res.reason
        print res.read()
        print res.getheaders()










