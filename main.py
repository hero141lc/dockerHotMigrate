import os
import datetime

class hosts(object):
    pass

#需要迁移主机的信息
hots_local=hosts
hots_local.ip='192.168.36.128'
hots_local.username='ly'
hots_local.password='12345'
#接收迁移主机的信息
hots_remote=hosts
hots_remote.ip='192.168.36.130'
hots_remote.username='ly'
hots_remote.password='12345'
hots_remote.container=''
def installCRIU():
    os.system(r"""
    apt update
    apt upgrade
    apt install build-essential
    apt install pkg-config
    apt install libnet-dev python-yaml libaio-dev
    apt install libprotobuf-dev libprotobuf-c0-dev protobuf-c-compiler protobuf-compiler python-protobuf libnl-3-dev libcap-dev python-future
    curl -O -sSL http://download.openvz.org/criu/criu-version.tar.bz2 
    tar xjf criu-version.tar.bz2 
    cd criu-3.10
    make
    cp ./criu/criu /usr/local/bin
    echo "{\"experimental\": true}" >> /etc/docker/daemon.json
    systemctl restart docker
    """)

def neofetch():
    os.system("neofetch")
os.system('')
def runDocker():
    os.system(r"docker run -d --name looper2 --security-opt seccomp:unconfined busybox /bin/sh -c 'i=0; while true; do echo $i; i=$(expr $i + 1); sleep 1; done'")
def bakDocker():
    os.system("mkdir /home/zy/tempData")
    os.system(r"docker checkpoint create --checkpoint-dir=/home/zy/tempData/ looper2 checkpoint2")
def dockerLog():
    os.system("docker logs --tail 20 looper2")
def createDocker():
    string_value=os.popen(r"docker create --name looper2 --security-opt seccomp:unconfined busybox /bin/sh -c 'i=0; while true; do echo $i; i=$(expr $i + 1); sleep 1; done'").read()
    hots_remote.container=''.join(ch for ch in string_value if ch.isalnum())
    print("hots_remote.container ID:",hots_remote.container,"end")
def sendData():
    print("------------------------算法测试-------------------------------")
    startTime=datetime.datetime.now()
   
    print("开启优化算法",startTime)
    os.system(r"scp -r -C /home/zy/tempData zy@192.168.36.130:/home/zy/garbage")
    endTime=datetime.datetime.now()
    print("运行结束",endTime)
    print("共用时",(endTime-startTime).seconds,"秒")

    print("不开启优化算法",startTime)
    os.system(r"scp -r /home/zy/tempData zy@192.168.36.130:/home/zy/")
    endTime=datetime.datetime.now()
    print("运行结束",endTime)
    print("共用时",(endTime-startTime).seconds,"秒")
    print("-----------------------------------------------------------")
def reliveDocker():
    
    os.system(r"mv /home/zy/tempData/checkpoint2/  /var/lib/docker/containers/"+hots_remote.container+"/checkpoints")
    os.system(r"docker start --checkpoint=checkpoint2 looper2")
def clearDocker():
    os.system(r"docker checkpoint rm looper2 checkpoint2")
    os.system(r"docker stop looper2")
    os.system(r"docker rm looper2")
    os.system("rm -rf /home/zy/tempData")
    os.system("rm -rf /home/zy/garbage")
if os.getuid() != 0:
    print(r"""
----------------------------ERROR---------------------------
-----------------无权限，请用root用户运行本程序---------------
------------------------------------------------------------
    """)
    exit()
while True:
    print(r"""
-----------------------------------------------------------
---------------------Docker热迁移演示-----------------------
-----------------------------------------------------------
-------------------------传输机-----------------------------
1. 安装CRIU并配置(安装后需要重启)
2. 演示操作系统信息
3. 创建并运行需要迁移的docker
4. 备份并创建检查点
5. 显示docker log
7. 发送数据到接收迁移主机
9. 清空docker数据
-------------------------接收机-----------------------------
1. 安装CRIU并配置(安装后需要重启)
2. 演示操作系统信息
5. 显示docker log
6. 接收迁移主机创建docker
8. 接收迁移主机运行docker
9. 清空docker数据
-----------------------------------------------------------
0. 退出演示
-----------------------作者：张瀛---------------------------
-----------------------------------------------------------
    """)
    i=int(input())
    print("-----------------------------------------------------------")
    if i ==1:
        print("--------------------CRIU已安装--------------------")
    if i==2:
        os.system("neofetch")
    if i==3:
        runDocker()
    if i==4:
        bakDocker()
    if i==5:
        dockerLog()
    if i==6:
        createDocker()
    if i==7:
        sendData()
    if i==8:
        reliveDocker()
    if i==9:
        clearDocker()
    if i==0:
        print("已退出，祝您生活愉快")
        exit()