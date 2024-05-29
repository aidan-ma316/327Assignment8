
import socket
import ipaddress
import threading
import time
import contextlib
import errno
from dataclasses import dataclass
import random
import sys
import json

maxPacketSize = 1024
# defaultPort = 24251
serverIP = input("Enter host ip address: ")
defaultPort = input("Enter host port here: ")

exitSignal = False

# def GetFreePort(minPort: int = 1024, maxPort: int = 65535):
#     for i in range(minPort, maxPort):
#         print("Testing port",i);
#         with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as potentialPort:
#             try:
#                 potentialPort.bind((serverIP, i));
#                 potentialPort.close();
#                 print("Server listening on port",i);
#                 return i
#             except socket.error as e:
#                 if e.errno == errno.EADDRINUSE:
#                     print("Port",i,"already in use. Checking next...");
#                 else:
#                     print("An exotic error occurred:",e);

def GetServerData() -> []:
    import MongoDBConnection as mongo
    return mongo.QueryDatabase();


def ListenOnTCP(tcpSocket: socket.socket, socketAddress):
    import logging
    try:
        while True:
            data = tcpSocket.recv(1024).decode('utf-8') 
            #when it gets the data from the client
            if data.lower() == "leave":  
                print("Server ended")
                break
            else:
            #prints out the traffic data from the client sides
                traffic_data = str(GetServerData())
                print(traffic_data)  
                #then send it back to the client
                tcpSocket.sendall(traffic_data.encode('utf-8'))

    except Exception as e:
        logging.error(f"Error handling connection {socketAddress}: {e}")
    finally:
        tcpSocket.close()


def CreateTCPSocket() -> socket.socket:
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    tcpPort = int(defaultPort)
    print("TCP Port:",tcpPort);
    #connects tcpSocket to the serverIP
    tcpSocket.bind((serverIP, tcpPort));
    return tcpSocket;

def LaunchTCPThreads():
    tcpSocket = CreateTCPSocket();
    tcpSocket.listen(5);
    while True:
        #connects the sockets between server and client
        connectionSocket, connectionAddress = tcpSocket.accept();
        connectionThread = threading.Thread(target=ListenOnTCP, args=[connectionSocket, connectionAddress]);
        connectionThread.start();

if __name__ == "__main__":
    tcpThread = threading.Thread(target=LaunchTCPThreads);
    tcpThread.start();

    while not exitSignal:
        time.sleep(1);
    print("Ending program by exit signal...");
