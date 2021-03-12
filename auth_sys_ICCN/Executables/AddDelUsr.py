from auth_sys_ICCN.Executables.SSHconnect import *

def AddUser(host,passwd,username,userpasswd) :
    SSHexec(host,"root",passwd,"useradd "+username)
    SSHexec(host,"root",passwd,'echo "'+username+':'+userpasswd+'" | chpasswd')

def DelUser(host,passwd,username) :
    SSHexec(host,"root",passwd,"userdel -fr "+username)

def ModUserPwd(host,passwd,username,usernewpasswd):
    SSHexec(host,"root",passwd,'echo "'+username+':'+usernewpasswd+'" | chpasswd')

def utilexist(host,password,name):
    s = SSHexec(host, 'root', password, 'cat /etc/passwd | grep ' + name)
    if len(s) == 0:
        return False
    else:
        return True
def delcrontab(host,passwd):
    SSHexec(host, 'root', passwd,'rm -r /root/filecrontabconfig')
    SSHexec(host, 'root', passwd,'rm -r /root/disk_and_ram_usage.txt')
    SSHexec(host, 'root', passwd,'crontab -u $USER -l | grep -v \'date\'  | crontab -u $USER -')

def crontab(host,passwd):
    delcrontab(host,passwd)
    SSHexec(host, 'root', passwd,'echo "*/1 * * * *  date  >> /root/disk_and_ram_usage.txt && df --total | tail -1 | awk \'{print \$5}\' >> /root/disk_and_ram_usage.txt && free |grep Mem | awk \'{print \$3/\$2 * 100.0}\' >> /root/disk_and_ram_usage.txt">>/root/filecrontabconfig')
    SSHexec(host, 'root', passwd, 'crontab -u $USER /root/filecrontabconfig')


def getinfo(host,passwd):
    liste= SSHexec(host, 'root', passwd, 'cat /root/disk_and_ram_usage.txt')
    l = []
    l2 = []
    l3 = []
    for i in liste:
        l.append(i.strip('\n'))
    for i in range(0, len(liste) - 2, 3):
        l2.append(l[i:i + 3])
    for i in range(len(l2)):
        l3.append(l2[len(l2) - 1 - i])
    return l3
