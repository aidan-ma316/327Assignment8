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
defaultPort = 24250

exitSignal = False

def GetFreePort(minPort: int = 1024, maxPort: int = 65535):
    for i in range(minPort, maxPort):
        print("Testing port",i);
        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as potentialPort:
            try:
                potentialPort.bind(('localhost', i));
                potentialPort.close();
                print("Server listening on port",i);
                return i
            except socket.error as e:
                if e.errno == errno.EADDRINUSE:
                    print("Port",i,"already in use. Checking next...");
                else:
                    print("An exotic error occurred:",e);

def GetServerData() -> []:
    import MongoDBConnection as mongo
    return mongo.QueryDatabase();


def ListenOnTCP(tcpSocket: socket.socket, socketAddress):
    import logging

    try:
        data = str(tcpSocket.recv(1024).decode('utf-8'))

        trafficData = GetServerData()

        trafficDataJson = json.dumps(trafficData)
        tcpSocket.sendall(trafficDataJson.encode('utf-8'))

    except Exception as e:
        logging.error(f"Error handling connection {socketAddress}: {e}")
    finally:
        tcpSocket.close()


    print('incoming data: ' + data); #TODO: Implement TCP Code, use GetServerData to query the database.


def CreateTCPSocket() -> socket.socket:
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    tcpPort = defaultPort
    print("TCP Port:",tcpPort);
    tcpSocket.bind(('localhost', tcpPort));
    return tcpSocket;

def LaunchTCPThreads():
    tcpSocket = CreateTCPSocket();
    tcpSocket.listen(5);
    while True:
        connectionSocket, connectionAddress = tcpSocket.accept();
        connectionThread = threading.Thread(target=ListenOnTCP, args=[connectionSocket, connectionAddress]);
        connectionThread.start();

if __name__ == "__main__":
    tcpThread = threading.Thread(target=LaunchTCPThreads);
    tcpThread.start();

    while not exitSignal:
        time.sleep(1);
    print("Ending program by exit signal...");
