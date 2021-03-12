import sqlite3
from SSHconnect import *

"""
def createtable():
    db = sqlite3.connect("servers.db")
    db.execute("CREATE TABLE if not exists servers(Server_ID TEXT PRMARY KEY, IP TEXT, root_Password TEXT)")
    db.commit()
    db.close()
"""

def ajouterserveur(Server_ID, IP, root_Password):
    db = sqlite3.connect("servers.db")
    db.execute("insert into servers values (?,?,?)",(Server_ID, IP, root_Password))
    db.commit()
    db.close()

def modifserverPwd(Server_ID,root_Password):
    db = sqlite3.connect("servers.db")
    db.execute("update servers set root_Password=? where Server_ID=?",(root_Password,Server_ID))
    db.commit()
    db.close()

def modifserverIP(Server_ID, IP):
    db = sqlite3.connect("servers.db")
    db.execute("update servers set IP=? where Server_ID=?", (IP, Server_ID))
    db.commit()
    db.close()

def listesevers():
    db = sqlite3.connect("servers.db")
    c = db.cursor()
    c.execute("select * from servers")
    listeservers = c.fetchall()
    db.commit()
    db.close()
    return listeservers

def deleteserver(Server_ID):
    db = sqlite3.connect("servers.db")
    db.execute("DELETE FROM servers WHERE Server_ID=?",(Server_ID,))
    db.commit()
    db.close()

def shutdownServer(host,passwd) :
    SSHexec(host,"root",passwd,"shutdown now")

def rebootServer(host,passwd) :
    SSHexec(host,"root",passwd,"reboot")
    
def extractServerIP(ServerID):
    db = sqlite3.connect("servers.db")
    c = db.cursor()
    c.execute("select IP from servers where Server_ID=?",(ServerID,))
    serverIP = c.fetchall()
    db.commit()
    db.close()
    return serverIP

def extractServerPasswd(ServerID):
    db = sqlite3.connect("servers.db")
    c = db.cursor()
    c.execute("select root_Password from servers where Server_ID=?",(ServerID,))
    serverPasswd = c.fetchall()
    db.commit()
    db.close()
    return serverPasswd
