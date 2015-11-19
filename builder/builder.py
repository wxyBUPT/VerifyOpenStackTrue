#coding=utf-8
__author__ = 'wxy'
import json
from configparser import ConfigParser

from . import uuidtag,blog,gconf,auth_token,Structure,tenant_id
from . import _neutron_port,_neutron_host,_nova_port,_nova_host
from . import _cinder_host,_cinder_port
from . import NetworkUtil,PortsUtil,SubnetUtil
from . import ComputeUtil,FlavorUtil,VolumeUtil
sconf = ConfigParser()
sconf.read('./struct.ini')

class InstanceStruct(Structure):
    _fields = ['name','netsId','img_id','flavor_id']
print

class Builder(object):


    def __init__(self):

        #存储创建网络的response.read()后的字典
        self.nets=[]
        #保存所有主机的信息，内容为 InstanceStruct
        self.instances=[]
        pass

    def _build_a_net(self,section):
        '''
        根据section创建网络并测试
        :param section: 在配置文件中的section名称
        :return:
        '''
        networkUtil=NetworkUtil(auth_token,_neutron_host,_neutron_port)
        name=sconf.get(section,'name')
        blog.info(u'创建网络{0}-{1}'.format(name,uuidtag))
        creatRes=networkUtil.create_network(name=name)
        jsonStr=creatRes.read()
        resDict=json.loads(jsonStr)
        self.nets.append(resDict)
        netId=resDict['network']['id']
        status=resDict['network']['status']
        blog.info(u'netId={0}的网络创建成功，当前状态为{1}-{2}'.format(netId,status,uuidtag))
        return netId

    def _build_subnet(self,netId,subnetaddr):
        '''
        根据网络id创建subnet
        :param netId:
        :param subnetaddr:
        :return:
        '''
        subnetUtil=SubnetUtil(auth_token,_neutron_host,_neutron_port)
        creRes=subnetUtil.create_sub_net_for(netId,subnetaddr)
        blog.info(
            u'为网络 {0} 创建了子网 {1}-{2}'.format(netId,subnetaddr,uuidtag)
        )
        return creRes

    #为主机挂载单个硬盘
    def _create_attach_volum_for_instance(self,instanceId,size):
        '''
        根据 ID 主机挂载 '%sG'%size 的硬盘
        :param instanceId:
        :param size:
        :return:
        '''
        print u'为 {0} 创建大小为{1}G 的硬盘'.format(instanceId,size)
        #volumeUtil=VolumeUtil(auth_token,_cinder_host,_cinder_port)
        #creRes=volumeUtil.create_volumes(tenant_id,size)

    #为主机创建其应该挂载的所有磁盘
    def _create_volums_for_instance(
            self,instanceStruct,instanceId
    ):
        print u'为主机 {0} id {1} 创建硬盘，这个函数是一个空'.format(instanceStruct.name,
                                           instanceId)
        name=instanceStruct.name
        section='instance_%s'%name
        if sconf.has_option(section,'volumes'):
            volumes=sconf.get(section,'volumes')
            volumes=volumes.split(',')
            #暂时不允许创建超过四个卷
            if len(volumes)>5:
                blog.error(
                    u'暂时只支持创建 5 个硬盘 不能创建{0} {1}'.format(
                        len(volumes),uuidtag
                    )
                )
                volumes=volumes[0:5]
            for size in volumes:
                self._create_attach_volum_for_instance(instanceId,int(size))

        else:
            blog.info(
                u'主机 {0} id {1} 不用挂载硬盘 - {2}'.format(
                    instanceStruct.name,instanceId,uuidtag
                )
            )


    def _create_a_instance(self,instanceStruct):
        '''
        根据instanceStruct创建
        :param instanceStruct:
        :return:
        '''
        name=instanceStruct.name
        netsId=instanceStruct.netsId
        #下面的循环为instance所处的每一个网络创建一个port，并将id记录
        nets=[]
        for netid in netsId:
            portsUtil=PortsUtil(auth_token,_neutron_host,_neutron_port)
            createPortRes=portsUtil.create_port_for_network(netid)
            portInfo=createPortRes.read()
            portInfo=json.loads(portInfo)
            portID=portInfo['port']['id']
            network={}
            network['uuid']=netid
            network['port']=portID
            nets.append(network)
            pass
        img_id=instanceStruct.img_id
        flavor_id=instanceStruct.flavor_id
        blog.info(
            u'创建主机 name = {0} netsId ={1} img_id ={2} flavor_id ={3} -{4}'.format(
                name,netsId,flavor_id,img_id,uuidtag
            )
        )
        computeUtil=ComputeUtil(
            auth_token,tenant_id,_nova_host,_nova_port
        )
        createRes=computeUtil.create_server(
            img_id,flavor_id,name,nets
        )
        createInfo=createRes.read()
        createInfo=json.loads(createInfo)
        instanceId=createInfo['server']['id']
        #下面将instanceId写回配置文件
        name=instanceStruct.name
        secName='instance_%s'%name
        sconf.set(secName,'id',instanceId)
        self._create_volums_for_instance(
            instanceStruct,instanceId
        )


    #根据配置文件创建网络，需要被第一步执行
    def net_builde(self):
        '''
        根据配置文件创建网络
        :return:
        '''
        nets=sconf.get('nets','keys')
        nets = nets.split(',')
        net_sections=[u'net_{0}'.format(net) for net in nets]
        #初始化一个以实例名为 key 的字典，用来存储实例链接到得网络 id
        instanceDict={}
        instances=sconf.get('instances','keys')
        instances=instances.split(',')
        for instance in instances:
            instance=instance.strip()
            instanceDict[instance]=[]
        print instanceDict
        #创建网络，并初始化实例的字典
        for net_section in net_sections:
            if not sconf.has_section(net_section):
                blog.error(u'配置文件缺少{0}-{1}'.format(net_section,uuidtag))
            else:
                blog.info(u'根据section {0} 创建网络 {1}'.format(net_section,uuidtag))
                netId=self._build_a_net(net_section)
                sconf.set(net_section,'id',netId)
                #将 netId 写到 instance 的配置
                if not sconf.has_option(net_section,'instances'):
                    blog.error(u'网络{0}，id为{1}没有没'
                               u'有需要创建的主机-{2}'.format(
                        net_section,netId,uuidtag
                    ))
                instances=sconf.get(net_section,'instances')
                instances=instances.split(',')
                for instance in instances:
                    instance=instance.strip()
                    instanceDict[instance].append(netId)
                    blog.info(u'主机 {0} 需要添加至网络 {1}-{2}'.format(
                        instance,netId,uuidtag
                    ))
                #创建网络成功后创建子网
                subnetaddr=sconf.get(net_section,'subnetaddr')
                subnetaddr=str(subnetaddr)
                creSubRes=self._build_subnet(netId,subnetaddr)
        #创建网络成功后保存实例对应的网络信息
        instances=sconf.get('instances','keys')
        instances=instances.split(',')
        for instance in instances:
            ins_section='instance_%s'%(instance)
            img_id=sconf.get(ins_section,'img_id')
            flavor_id=sconf.get(ins_section,'flavor_id')
            nets_id=instanceDict[instance]
            insStruct=InstanceStruct(instance,nets_id,img_id,flavor_id)
            self.instances.append(
                insStruct
            )

    #创建主机,
    def instance_build(self):
        '''
        完成硬盘创建，并挂载到对应网络，并挂载对应大小的硬盘
        :return:
        '''
        for instance in self.instances:
            self._create_a_instance(instance)
            pass
        #sconf.write(open('./test.ini','w'))