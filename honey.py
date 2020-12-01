
#Author:D4Vinci
#Squnity Developers 
import socket
from datetime import datetime
our_log=open("Attackers_Data.txt","w") #Our text file to save attackers data in it

def ssh(msg="",listeners=2):
    welcome="""BIENVENIDO AL HONEYPOT DE SSH\n
    Te recomiendo que cortes la ejecución del comando porque estas aquí eternamente\n
    """
    s = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 22))#binding for the ssh port
    print("\nSSH Honeypot ready(Waiting For Attackers)..\n")
    s.listen(int(listeners))
    stat=0
    n=0
    ips=[]
    rqs=["http","HTTP/1.0","GET","bind","version","OPTIONS"]
    while True:
        n+=1
        c,attacker= s.accept()
        port=attacker[1]
        ip=attacker[0]
        c.send(b"login as: ")
        login=c.recv(1024)
        c.send(login+b"@host's password: ")
        a=c.recv(1024)
        PROMPT = str(login)+"@host:~$"
        c.send(welcome.encode())
        ips.append(ip)
        our_log.write("\n ["+str(n)+"] ["+str(datetime.now())+"] IP: "+str(ip)+"\tPort: "+str(port)+" User: "+str(login.decode())+" Pass: "+str(a.decode())+"\n")
        print("\n ["+str(n)+"] IP: "+str(ip)+"\tPort: "+str(port)+"\n")
        c.send(PROMPT.encode())
        data = str(c.recv(1024).decode())

        for rq in rqs:          # detecta escaneos con nmap, y deja registro de quién escanea
            if rq in data.split(" ") or data.split(" ")=="" or data==" " :
                our_log.write(" ["+str(datetime.now())+"] ["+str(ip)+"] is Scanning us With nmap looking for service info.!"+"\n")
                print(" ["+str(datetime.now())+"] ["+str(ip)+"] is Scanning us With nmap looking for service info.!"+"\n")
                if ip in ips:c.close()
                stat=1
                break

        if data.split(" ")[0] == "id":
            our_log.write(" ["+str(ip)+"][!]Command: "+str(data)+"\n")
            print(" ["+str(ip)+"][!]Command: "+str(data)+"\n")
            c.send(b"\nuid=0(root) gid=0(root) groups=0(root)")
            our_log.write("  ["+str(ip)+"]>Output: uid=0(root) gid=0(root) groups=0(root)\n")
            print("  ["+str(ip)+"]>Output: uid=0(root) gid=0(root) groups=0(root)\n")
            c.send(str(msg).encode()+b'\n')
            stat=1
            c.close()

        elif data.split(" ")[0] == "uname":
            our_log.write(" ["+str(ip)+"]!]Command: "+str(data)+"\n")
            print(" ["+str(ip)+"][!]Command: "+str(data)+"\n")
            c.send(b"\nLinux f001 3.13.3-7-high-octane-fueled #3000-LPG SMPx4 Fri Jun 31 25:24:23 UTC 2200 x86_64 x64_86 x13_37 GNU/Linux")
            our_log.write("  ["+str(ip)+"]>Output: Linux f001 3.13.3-7-high-octane-fueled #3000-LPG SMPx4 Fri Jun 31 25:24:23 UTC 2200 x86_64 x64_86 x13_37 GNU/Linux\n")
            print("  ["+str(ip)+"]>Output: Linux f001 3.13.3-7-high-octane-fueled #3000-LPG SMPx4 Fri Jun 31 25:24:23 UTC 2200 x86_64 x64_86 x13_37 GNU/Linux\n")
            c.send(str(msg).encode()+b'\n')
            stat=1
            c.close()

        elif stat==0:
            our_log.write("\t[!]Command: "+str(data)+"\n")
            print(" ["+str(ip)+"][!]Command: "+str(data)+"\n")
            c.send(b"\n"+str(data.split(" ")[0]).encode() + b": command not found")
            our_log.write("   ["+str(ip)+"]>Output: "+ data.split(" ")[0] + ": command not found\n")
            print("   ["+str(ip)+"]>Output: "+ data.split(" ")[0] + ": command not found\n")
            c.send(str(msg).encode()+b'\n')
            c.close()
        our_log.write("="*10)
        print("="*10)

    our_log.close()

ssh()
