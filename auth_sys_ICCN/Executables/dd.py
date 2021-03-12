import paramiko
import time
from datetime import datetime


def tp_reel_dd(ip,passwd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=ip, username="root", password=passwd)
    except:
        print("[!]Cannot connect to SSH server")
        exit()
    z=[]

    for i in range(0,15):
        stdin, stdout, stderr = client.exec_command("df -x squashfs --total ")
        A = stdout.read().decode()
        B = A.split("\n")
        k = datetime.now()
        S = 0
        for j in range(len(B[-2])):
            if B[-2][j] == '%':
                S = (int(B[-2][j - 3:j]))
        z.append(str(k)[11:])
        z.append(str(S))
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
        print("[!]Cannot connect to SSH server")
        exit()
    stdin, stdout, stderr = client.exec_command("df -x squashfs --total ")
    A = stdout.read().decode()
    B = A.split("\n")
    k = datetime.now()
    S = 0
    for j in range(len(B[-2])):
        if B[-2][j] == '%':
            S = (int(B[-2][j - 3:j]))
    z=[str(k)[11:19], str(S)]
    err = stderr.read().decode()
    if err:
        print(err)
    print(z)
    return z
def servs(ip,user,passwd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    z=[]
    while True:
        for i in range(len(ip)):
            try:
                client.connect(hostname=ip[i], username=user[i], password=passwd[i])
            except:
                print("[!] Cannot connect to the SSH Server")
                exit()
            stdin, stdout, stderr = client.exec_command("df -x squashfs --total ")
            A = stdout.read().decode()
            B = A.split("\n")
            k = datetime.now()
            S = 0
            for j in range(len(B[-2])):
                if B[-2][j] == '%':
                    S = (int(B[-2][j - 3:j]))
            z += ["serveur" + str(i),str(k)[11:19],str(S)]
            err = stderr.read().decode()
            print(z)
            if err:
                print(err)
    return z

#tp_reel("192.168.231.135","root","adminadmin")
#now("192.168.231.135","root","adminadmin")
#servs(["192.168.231.135","192.168.231.136"],["root","root"],["adminadmin","adminadmin"])







