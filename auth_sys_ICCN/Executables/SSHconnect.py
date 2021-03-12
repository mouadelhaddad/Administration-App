import paramiko

def SSHexec(host,username,password,command) :
    port = 22

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)

    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()
    return lines

#SSHexec('192.168.1.7','mouad','elhaddad','crontab -u mouad /home/mouad/file')
