import socket
import select
import time

DISCOONECT_ERROR = 0
DISCONNECT_TIMEOUT = 1
DISCONNECT_CLOSED = 2

class client:
    host = ""
    port = 0
    out = []
    lastio = 0
    backbuf = b""
    localData = {}
    shouldClose = False
    
    def __init__(self, con):
        self.port = con[1][1]
        self.host = con[1][0]
        self.lastio = time.time()
        
    def write(self, data):
        self.out.append(data)
    
    def close(self):
        self.shouldClose = True
    
    def __str__(self):
        return "{}:{}".format(self.host,self.port)
    
    def __eq__(self, other):
        if type(other) is not client:
            return False
        return self.host == other.host and self.port == other.port
    
    def __getitem__(self, key):
        if key in self.localData:
            return self.localData[key]
        return None
    
    def __setitem__(self, key, value):
        self.localData[key] = value
    
    def __delitem__(self, key):
        del self.localData[key]
    
    def __contains__(self, item):
        return item in self.localData
    
    def __iter__(self):
        return iter(self.localData.keys())
    
class server:
    sock = None
    connections = {}
    def __init__(self, host="0.0.0.0", port=0, readSize = 0xFFFF, \
                 idleCheck = 1, ping = 5, die = 5, dieTime = 60, \
                 opts={}):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.sock.setblocking(False)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #Keep alive
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.sock.setsockopt(
            socket.IPPROTO_TCP,
            socket.TCP_KEEPIDLE,
            idleCheck
        )
        self.sock.setsockopt(
            socket.IPPROTO_TCP,
            socket.TCP_KEEPINTVL,
            ping
        )
        self.sock.setsockopt(
            socket.IPPROTO_TCP,
            socket.TCP_KEEPCNT,
            die
        )
        
        #Bind
        self.sock.bind((host,port))
        self.sock.listen(0)
        
        self.init(opts)
        
        while True:
            read, write, error = select.select(
                [self.sock],
                [],
                [self.sock],
                0
            )
            if len(read) > 0:
                con = self.sock.accept()
                con[0].setblocking(False)
                self.connections[con[0]] = client(con)
                self.connect(self.connections[con[0]])
                
            if len(error) > 0:
                print("ERROR!?")
                
            connections = list(self.connections.keys())
            read, write, error = select.select(
                connections,
                connections,
                connections,
                0
            )
            
            now = time.time()
            #Read
            for con in read:
                try:
                    if con in self.connections:
                        data = con.recv(readSize)
                        if data:
                            self.recv(
                                self.connections[con], 
                                self.connections[con].backbuf + data
                            )
                            self.connections[con].backbuf = b""
                            self.connections[con].lastio = now
                        else:
                            self.disconnect(self.connections[con],2)
                            del self.connections[con]
                except ConnectionResetError as e:
                    if con in self.connections:
                        self.disconnect(self.connections[con],0)
                        del self.connections[con]
            
            #Write
            for con in write:
                try:
                    if con in self.connections:
                        for data in self.connections[con].out:
                            con.send(data)
                        self.connections[con].out = []
                        self.connections[con].lastio = now
                except ConnectionResetError as e:
                    if con in self.connections:
                        self.disconnect(self.connections[con],0)
                        del self.connections[con]
            
            #Error checking
            for con in error:
                try:
                    if con in self.connections:
                        self.error(self.connections[con])
                        self.disconnect(self.connections[con],0)
                        del self.connections[con]
                except ConnectionResetError as e:
                    if con in self.connections:
                        self.error(self.connections[con])
                        self.disconnect(self.connections[con],0)
                        del self.connections[con]
            cons = list(self.connections)
            for con in cons:
                if dieTime:
                    if self.connections[con].lastio + dieTime < now:
                        self.disconnect(self.connections[con], 1)
                        del self.connections[con]
                if self.connections[con].shouldClose:
                    con.close()
                    self.disconnect(self.connections[con],0)
                    del self.connections[con]
            self.idle()
    
    def init(self):
        pass
    
    def idle(self):
        pass
    
    def recv(self, client, data):
        pass
    
    def connect(self, client):
        pass
        
    def disconnect(self, client, reason):
        pass
    
    def error(self, client):
        pass
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
