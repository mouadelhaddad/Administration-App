from datetime import datetime
import paramiko
import time


def tp_reel(ip,user,passwd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=ip, username=user, password=passwd)
    except:
        print("[!] Cannot connect to the SSH Server")
        exit()
    z=[]
    for i in range(0,15):
        stdin, stdout, stderr = client.exec_command("vmstat -s |cut -c1-14 |head -2")
        c = stdout.read().decode()
        b = c.split("\n")
        k = datetime.now()
        v = (int(b[1]) / int(b[0])) * 100
        z += [str(k)[11:], str(v)]
        err = stderr.read().decode()
        if err:
            print(err)
        time.sleep(0.02)

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

#print(tp_reel("192.168.1.114","root","roottoor"))
#now("192.168.231.135","root","adminadmin")
#print(servs(["192.168.1.114","192.168.1.115"],["root","root"],["roottoor","roottoor"]))