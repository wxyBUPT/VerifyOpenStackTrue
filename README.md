# verifyOpenstack True

脚本本意是验证新搭建的一套 openstack 集群的可用性。

使用方法：
1、通过 global.ini 配置认证信息、neutron、nova、cinder服务的地址信息，认证信息的user_name 和 password需要是在 Horizon 能正常登陆的账号

2、通过 struct.ini 配置要在 openstack 环境中创建的拓扑结构，目前支持需要创建的网络、网络上挂载的主机、主机需要挂载的硬盘
（5个以内，单位为G）

3、当前情况执行 python tests.py 

4、创建信息在 ./log/builder_info.log 中，错误信息在 ./log/builder_error.log 中
