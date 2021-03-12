from datetime import datetime
import paramiko
import time
from auth_sys_ICCN.Executables.SSHconnect import *

def tp_reel_mem(ip, passwd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=ip, username="root", password=passwd)
    except:
        print("[!] Cannot connect to the SSH Server")
        exit()
    z = []
    for i in range(0, 15):
        stdin, stdout, stderr = client.exec_command("vmstat -s |cut -c1-14 |head -2")
        c = stdout.read().decode()
        b = c.split("\n")
        k = datetime.now()
        v = (int(b[1]) / int(b[0])) * 100
        z.append(str(k)[11:])
        z.append(str(v))
        err = stderr.read().decode()
        if err:
            print(err)
        time.sleep(0.01)

    return z

def now(ip,user,passwd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=ip, username=user, password=passwd)
    except:
        print("[!] Cannot connect to the SSH Server")
        exit()
    stdin, stdout, stderr = client.exec_command("vmstat -s |cut -c1-14 |head -2")
    c = stdout.read().decode()
    b = c.split("\n")
    k = datetime.now()
    v = (int(b[1]) / int(b[0])) * 100
    z=[str(k),str(v)]
    err = stderr.read().decode()
    print(z)
    if err:
        print(err)
    return z
def servs(list,user,passwd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    z = []
    while True:
        for i in range(len(list)):
            try:
                client.connect(hostname=list[i], username=user[i], password=passwd[i])
            except:
                print("[!] Cannot connect to the SSH Server")
                exit()
            stdin, stdout, stderr = client.exec_command("vmstat -s |cut -c1-14 |head -2")
            c = stdout.read().decode()
            b = c.split("\n")
            k = datetime.now()
            v = (int(b[1]) / int(b[0])) * 100
            z += ["serveur" + str(i), str(k)[11:19],str(v)]
            err = stderr.read().decode()
            if err:
                print(err)
    return z

def memdisk(host,passwd):
    l = SSHexec(host, "root", passwd, "cat /home/mouad/disk.txt")
    l2=[s.strip('\n') for s in l]
    for i in l2:
        print(i)
    return l2
#print(memdisk('192.168.1.7','elhaddad'))