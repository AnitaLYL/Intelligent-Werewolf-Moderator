# # 扫描局域网主机
#
# # 互相传输数据
#
# import platform
# import os
# import time
# import threading
# import socket
#
# live_ip = 0
#
#
# def get_os():
#     os = platform.system()
#     if os == "Windows":
#         return "n"
#     else:
#         return "c"
#
#
# def ping_ip(ip_str):
#     cmd = ["ping", "-{op}".format(op=get_os()),
#            "1", ip_str]
#     output = os.popen(" ".join(cmd)).readlines()
#     for line in output:
#         if str(line).upper().find("TTL") >= 0:
#             print("ip: %s 在线" % ip_str)
#             global live_ip
#             live_ip += 1
#             break
#
#
# def find_ip(ip_prefix):
#     '''''
#     给出当前的ip地址段 ，然后扫描整个段所有地址
#     '''
#     threads = []
#     for i in range(1, 256):
#         ip = '%s.%s' % (ip_prefix, i)
#         threads.append(threading.Thread(target=ping_ip, args={ip, }))
#     for i in threads:
#         i.start()
#     for i in threads:
#         i.join()
#
#
# def find_local_ip():
#     """
#     获取本机当前ip地址
#     :return: 返回本机ip地址
#     """
#     myname = socket.getfqdn(socket.gethostname())
#     myaddr = socket.gethostbyname(myname)
#     return myaddr
#
#
#
# import socket
#
# def get_host_ip():
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.connect(('8.8.8.8', 80))
#         ip = s.getsockname()[0]
#     finally:
#         s.close()
#
#     return ip
#
# if __name__ == "__main__":
#     print("开始扫描时间: %s" % time.ctime())
#     addr = find_local_ip()
#     args = "".join(addr)
#     ip_pre = '.'.join(args.split('.')[:-1])
#     find_ip('192.168.1')
#
#     host_name = socket.gethostbyaddr('192.168.1.64')
#     print(host_name,' 192.168.1.64')
#
#     print("扫描结束时间 %s" % time.ctime())
#     print('本次扫描共检测到本网络存在%s台设备' % live_ip)
#     print('内网ip: ', get_host_ip())


import time
import threading
import socket

threads = []


def get_hostname(ip):
    try:
        (name, aliaslist, addresslist) = socket.gethostbyaddr(ip)
        print(name, '  ', ip)
    except Exception as e:
        return


def find_ip(ip_prefix):
    for i in range(0, 256):
        ip = '%s.%s' % (ip_prefix, i)
        th = threading.Thread(target=get_hostname, args=(ip,))
        threads.append(th)


if __name__ == "__main__":
    print("start time %s" % time.ctime())
    find_ip('192.168.1')
    for t in threads:
        t.start()
    # 主线程中等待所有子线程退出
    for t in threads:
        t.join()
    print("end time %s" % time.ctime())
