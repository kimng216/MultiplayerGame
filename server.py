import socket
import threading
import hashlib
import time
import random
import pygame.time

# Server setup
host = ''
port = 5555
clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
textchat = []
words = ["COMPUTERS", "PROGRAMMING", "ALGORITHMS", "MATHEMATICS", "CODING", "RANDOM", "DEPARTMENT", "STUDENTS", "PROCESSOR"]
current_word = random.choice(words)
word = f"word,{current_word},"
x = 0
empty = ''
i =0
joined = ''

with open("serverfiles/banned_ips.txt", "r") as file:
    banned_ips = file.read().splitlines()


def handle_client(client,address):
    print(f"address: {address} connected")
    count = 0
    if address[0] in banned_ips:
        print(f"Connection attempt blocked from banned IP: {address[0]}")
        client.close()
        return
    try:
        while True:
            data = client.recv(1024).decode('utf-8')
            print(data)
            if not data:
                return
            parts = data.split(',')
            time.sleep(.1)
            if len(parts) == 3:
                data_type, username, other = parts
                if data_type == 'signup':
                    if store_credentials(username, other):
                        client.sendall("Signup successful".encode('utf-8'))
                    else:
                        client.sendall("Signup failed: Username already exists".encode('utf-8'))
                elif data_type == 'login':
                    if check_credentials(username, other):
                        client.sendall("Login successful".encode('utf-8'))
                        break
                    else:
                        client.sendall("Login failed".encode('utf-8'))

                elif data_type == 'joined':
                    joined = f"joined,{username} joined the game,"
                    for cl in clients:
                        try:
                            time.sleep(.1)
                            cl.sendall(joined.encode('utf-8'))
                            print(f"sent to {cl}")
                        except Exception as e:
                            print(e)
                elif data_type == 'quit':
                    quit = f"quit,{username} left the game,"
                    for cl in clients:
                        try:
                            time.sleep(.1)
                            cl.sendall(quit.encode('utf-8'))
                            print(f"sent to {cl}")
                        except Exception as e:
                            print(e)
                elif data_type == 'chat':
                    textchat = f"chat,{username}: {other},"
                    print(textchat)
                    for cl in clients:
                        try:
                            time.sleep(.1)
                            cl.sendall(textchat.encode('utf-8'))
                            print(f"sent to {cl}")
                        except Exception as e:
                            print(e)
                            print(f"failed to send to {address}")
                            clients.remove(cl)
                elif data_type == 'need world chat':
                    print("went to need world chat")
                    with open("serverfiles/worldchat.txt", "r") as file:
                        worldchat = file.read().splitlines()
                    for worldchat[count] in worldchat:
                        if count > -10:
                            line = f"receivechatmessage,{worldchat[count]},"
                            print(line)
                            pygame.time.wait(100)
                            client.sendall(line.encode('utf-8'))
                            count = count + 1
                            print(count)
                elif data_type == 'world chat':
                    print("went to world chat")
                    newworldchat = f"worldchat,{username}: {other},"
                    with open("serverfiles/worldchat.txt", "a") as file:
                        file.write(f"{username}: {other}\n")
                        file.close()
                    for cl in clients:
                        try:
                            time.sleep(.1)
                            cl.sendall(newworldchat.encode('utf-8'))
                            print(f"sent to {cl}")
                        except Exception as e:
                            print(e)
                elif data_type == 'need word':
                    for cl in clients:
                        try:
                            time.sleep(.1)
                            cl.sendall(word.encode('utf-8'))
                            print(f"sent to {cl}")
                        except Exception as e:
                            print(e)
                            print(f"failed to send to {address}")
                elif data_type == 'guess':
                        guess = f"guess,{username},{other}"
                        print(guess)
                        for cl in clients:
                            try:
                                time.sleep(.1)
                                cl.sendall(guess.encode('utf-8'))
                                print(f"sent to {cl}")
                            except Exception as e:
                                print(e)
                                print(f"failed to send to {address}")

                elif data_type == 'restart':
                    current_word = random.choice(words)
                    newword = f"word,{current_word},"
                    for cl in clients:
                        try:
                            time.sleep(.1)
                            cl.sendall(newword.encode('utf-8'))
                            print(f"sent to {cl}")
                        except Exception as e:
                            print(e)
                            print(f"failed to send to {address}")

                elif data_type == 'ban':
                    banned = f"banned,{username} was banned,"
                    ban_ip(client, address)
                    for cl in clients:
                        try:
                            time.sleep(.1)
                            cl.sendall(banned.encode('utf-8'))
                            print(f"sent to {cl}")
                        except Exception as e:
                            print(e)
            else:
                return
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print({address,"closed"})
        client.close()
        clients.remove(client)


def store_credentials(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    with open("serverfiles/users.txt", "a+") as file:
        file.seek(0)
        for line in file:
            stored_username, _ = line.strip().split(',')
            if username == stored_username:
                return False
        file.write(f"{username},{hashed_password}\n")
    return True

def check_credentials(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    with open("serverfiles/users.txt", "r") as file:
        for line in file:
            stored_username, stored_hash = line.strip().split(',')
            if username == stored_username and hashed_password == stored_hash:
                return True
    return False

def ban_ip(client, address):
    ip = address[0]
    banned_ips.append(ip)
    with open("serverfiles/banned_ips.txt", "a") as file:
        file.write(f"{ip}\n")
    client.close()
    print(f"IP banned: {ip}")

def receive_connections():
    while True:
        client, address = server.accept()
        clients.append(client)
        threading.Thread(target=handle_client, args=(client,address)).start()

threading.Thread(target=receive_connections,).start()
