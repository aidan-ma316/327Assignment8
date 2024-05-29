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
#enter serverIP
serverIP = input("Enter server ip address: ")
#serverIP = '***.***.***.***' #TODO: Change this to your instance IP

#initalize the tcpSocket
tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
try:
    #enter tcp ports
    tcpPort = int(input("Please enter the TCP port of the host..."));
except:
    tcpPort = 0;
if tcpPort == 0:
    #intialize the default port if tcpPort is 0
    tcpPort = defaultPort;
#connect the tcpSocket to the tcpPort
tcpSocket.connect((serverIP, tcpPort));

clientMessage = "";

#enter msg to echo between server and client
while clientMessage != "exit":
    clientMessage = input("Please type the message that you'd like to send (Or type \"leave\" to exit):\n>");

    #send msg to the server
    tcpSocket.send(bytearray(str(clientMessage), encoding='utf-8'))
    #recieves data from the user
    data = tcpSocket.recv(1024)

    #if the data is empty then the loop breaks
    if data == b'':
        print("Session Ended")
        break
    
    #returns a matrix
    d_data = data.decode("utf-8").strip('[]').split(',')
    
    #print(d_data)
    #now its a list

    #get the highway name and its score
    best_highway = d_data[0].strip("'");
    best_highway_score = d_data[1];

    #display to the user the best highway and its score
    print(f'1. The best freeway to take is {best_highway} with a traffic score of: {best_highway_score}\n')


    print('Rankings:')
    i = 0
    j = 1
    #print the rankings of the highways
    while i < len(d_data) and i < 10:
        # print(f'{j}. {d_data[i].strip("'")}: {d_data[i+1]}')
        print(f'{j}. {(d_data[i])}: {d_data[i+1]}')
        j += 1
        i += 2

    print()
    
#closes the tcp socket when the loop breaks
tcpSocket.close();
