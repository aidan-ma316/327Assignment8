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
    clientMessage = input("Please type the message that you'd like to send (Or type \"exit\" to exit):\n>");

    tcpSocket.send(bytearray(str(clientMessage), encoding='utf-8'))
    data = tcpSocket.recv(1024)

    d_data = data.decode("utf-8")

    data_list = json.loads(d_data)

    print(data)

    best_highway = data[0][1];

    print('The best highway to take is', best_highway, ' with a traffic score of', data[0][0], '\n');
    
    for h,i in data[1:]:
        print(best_highway)

    
tcpSocket.close();

