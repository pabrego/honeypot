
#Author:D4Vinci
#Squnity Developers 
import socket

from datetime import datetime
our_log=open("Attackers_Data.txt","w") #Our text file to save attackers data in it

def ssh(msg="",listeners=2):
    welcome="""BIENVENIDO AL HONEYPOT DE SSH\n
    """
    s = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 22))#binding for the ssh port
    print("\nSSH Honeypot ready(Waiting For Attackers)..\n")
    s.listen()
    # stat=0
    n=0
    ips=[]
    # rqs=["http","HTTP/1.0","GET","bind","version","OPTIONS"]
    while True:
        n+=1
        (c,attacker)= s.accept()
        port=attacker[1]
        ip=attacker[0]
        print("Atacante "+str(ip)+":"+str(port)+" se conecto")
        m = c.recv(1024)
        print(m.decode())
        print("\n ["+str(n)+"] IP: "+str(ip)+"\tPort: "+str(port)+"\n") 
        c.send("login as: ".encode())
        login=c.recvfrom(1024)
        c.send(login+b"@host's password: ")
        a=c.recv(1024)
        PROMPT = str(login)+"@host:~$"
        c.send(welcome.encode())
        ips.append(ip)
        our_log.write("\n ["+str(n)+"] ["+str(datetime.now())+"] IP: "+str(ip)+"\tPort: "+str(port)+" User: "+str(login.decode())+" Pass: "+str(a.decode())+"\n")
        print("\n ["+str(n)+"] IP: "+str(ip)+"\tPort: "+str(port)+"\n")
        c.send(PROMPT.encode())
        data = str(c.recv(1024).decode())
        print(data)

    our_log.close()

ssh()
