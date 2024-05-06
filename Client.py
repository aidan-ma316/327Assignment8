import socket
import ipaddress
import threading
import time
import contextlib
import errno
import json

maxPacketSize = 1024
defaultPort = 2424 
#localhost testing
serverIP = '127.0.0.1'
#serverIP = '***.***.***.***' #TODO: Change this to your instance IP

tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
try:
    tcpPort = int(input("Please enter the TCP port of the host..."));
except:
    tcpPort = 0;
if tcpPort == 0:
    tcpPort = defaultPort;
tcpSocket.connect((serverIP, tcpPort));

clientMessage = "";

while clientMessage != "exit":
    clientMessage = input("Please type the message that you'd like to send (Or type \"leave\" to exit):\n>");

    tcpSocket.send(bytearray(str(clientMessage), encoding='utf-8'))
    data = tcpSocket.recv(1024)

    if data == b'':
        print("Session Ended")
        break

    d_data = data.decode("utf-8").strip('[]').split(',')

    
    #print(d_data)
    #now its a list

    best_highway = d_data[0].strip("'");
    best_highway_score = d_data[1];

    print(f'1. The best freeway to take is {best_highway} with a traffic score of: {best_highway_score}\n')


    print('Rankings:')
    i = 0
    j = 1
    while i < len(d_data) and i < 10:
        # print(f'{j}. {d_data[i].strip("'")}: {d_data[i+1]}')
        print(f'{j}. {(d_data[i])}: {d_data[i+1]}')
        j += 1
        i += 2

    print()
    
    
tcpSocket.close();
