import socket
import ipaddress
import threading
import time
import contextlib
import errno

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

    best_highway = "";

    print('The best highway to take is', best_highway);
    #TODO: Print the best highway to take
    
tcpSocket.close();

