
from socket import *

def main():
    ip_add = "192.168.0.38"
    port = 22
    print("Homeypot start..........")
    try:
        get_socket_con = socket(AF_INET, SOCK_STREAM)
        get_socket_con.bind((ip_add,port))
        get_socket_con.listen(10)
        while 1:
            client_con,client_addr = get_socket_con.accept()
            print("Visiter found!   -   [{}]".format(client_addr[0]))
            client_con.send(b"<h1>te cagué perro ql</h1>")
            data = client_con.recv(2048)
            print(data)
    except error as ide:
        print("[+] Unspecified error [{}]".format(ide))
    except KeyboardInterrupt as key:
        print("[-] Process stoped !")
    finally:
        get_socket_con.close()

if __name__ == "__main__":
    main()