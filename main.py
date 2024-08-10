import socket;
import threading;
import rsa;

public_key, private_key = rsa.newkeys(1024)
partner_key = None


option = input("Choose option: 1 =>  host, 2 => connect\n")

if option == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 8050))
    server.listen()

    client, _ = server.accept()
    client.send(public_key.save_pkcs1("PEM"))
    partner_key = rsa.PublicKey.load_pkcs1(client.recv(1024))

elif option == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8050))
    partner_key = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1("PEM"))

else :
    exit()

def send_message(c):
    while True:
        message = input()
        encrypted_message = rsa.encrypt(message.encode(), partner_key)
        c.send(encrypted_message)

        print("Sent message is ", message)

def receive_message(c):
    while True:
        received_message = rsa.decrypt(c.recv(1024), private_key).decode()
        
        print("Received message : ", received_message)
        

threading.Thread(target=send_message, args=(client, )).start()
threading.Thread(target=receive_message, args=(client, )).start()