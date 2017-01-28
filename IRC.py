import uuid
import os
import IRC
import sys
import datetime
import socket
import select
import time

DISCOONECT_ERROR = 0
DISCONNECT_TIMEOUT = 1
DISCONNECT_CLOSED = 2

class irc:
    RPL_WELCOME = 1
    RPL_YOURHOST = 2
    RPL_CREATED = 3
    RPL_MYINFO = 4
    RPL_BOUNCE = 5
    RPL_TRACELINK         = 200
    RPL_TRACECONNECTING   = 201
    RPL_TRACEHANDSHAKE    = 202
    RPL_TRACEUNKNOWN      = 203
    RPL_TRACEOPERATOR     = 204
    RPL_TRACEUSER         = 205
    RPL_TRACESERVER       = 206
    RPL_TRACESERVICE      = 207
    RPL_TRACENEWTYPE      = 208
    RPL_TRACECLASS        = 209
    RPL_TRACERECONNECT    = 210
    RPL_STATSLINKINFO     = 211
    RPL_STATSCOMMANDS     = 212
    RPL_STATSCLINE        = 213
    RPL_STATSNLINE        = 214
    RPL_STATSILINE        = 215
    RPL_STATSKLINE        = 216
    RPL_STATSQLINE        = 217
    RPL_STATSYLINE        = 218
    RPL_ENDOFSTATS        = 219
    RPL_UMODEIS           = 221
    RPL_SERVICEINFO       = 231
    RPL_ENDOFSERVICES     = 232
    RPL_SERVICE           = 233
    RPL_SERVLIST          = 234
    RPL_SERVLISTEND       = 235
    RPL_STATSVLINE        = 240
    RPL_STATSLLINE        = 241
    RPL_STATSUPTIME       = 242
    RPL_STATSOLINE        = 243
    RPL_STATSSLINE        = 244
    RPL_STATSHLINE        = 244
    RPL_STATSPING         = 246
    RPL_STATSBLINE        = 247
    RPL_STATSDLINE        = 250
    RPL_LUSERCLIENT       = 251
    RPL_LUSEROP           = 252
    RPL_LUSERUNKNOWN      = 253
    RPL_LUSERCHANNELS     = 254
    RPL_LUSERME           = 255
    RPL_ADMINME           = 256
    RPL_ADMINLOC1         = 257
    RPL_ADMINLOC2         = 258
    RPL_ADMINEMAIL        = 259
    RPL_TRACELOG          = 261
    RPL_TRACEEND          = 262
    RPL_TRYAGAIN          = 263
    RPL_NONE              = 300
    RPL_AWAY              = 301
    RPL_USERHOST          = 302
    RPL_ISON              = 303
    RPL_UNAWAY            = 305
    RPL_NOWAWAY           = 306
    RPL_WHOISUSER         = 311
    RPL_WHOISSERVER       = 312
    RPL_WHOISOPERATOR     = 313
    RPL_WHOWASUSER        = 314
    RPL_ENDOFWHO          = 315
    RPL_WHOISCHANOP       = 316
    RPL_WHOISIDLE         = 317
    RPL_ENDOFWHOIS        = 318
    RPL_WHOISCHANNELS     = 319
    RPL_LISTSTART         = 321
    RPL_LIST              = 322
    RPL_LISTEND           = 323
    RPL_CHANNELMODEIS     = 324
    RPL_UNIQOPIS          = 325
    RPL_NOTOPIC           = 331
    RPL_TOPIC             = 332
    RPL_INVITING          = 341
    RPL_SUMMONING         = 342
    RPL_INVITELIST        = 346
    RPL_ENDOFINVITELIST   = 347
    RPL_EXCEPTLIST        = 348
    RPL_ENDOFEXCEPTLIST   = 349
    RPL_VERSION           = 351
    RPL_WHOREPLY          = 352
    RPL_NAMREPLY          = 353
    RPL_KILLDONE          = 361
    RPL_CLOSING           = 362
    RPL_CLOSEEND          = 363
    RPL_LINKS             = 364
    RPL_ENDOFLINKS        = 365
    RPL_ENDOFNAMES        = 366
    RPL_BANLIST           = 367
    RPL_ENDOFBANLIST      = 368
    RPL_ENDOFWHOWAS       = 369
    RPL_INFO              = 371
    RPL_MOTD              = 372
    RPL_INFOSTART         = 373
    RPL_ENDOFINFO         = 374
    RPL_MOTDSTART         = 375
    RPL_ENDOFMOTD         = 376
    RPL_YOUREOPER         = 381
    RPL_REHASHING         = 382
    RPL_YOURESERVICE      = 383
    RPL_MYPORTIS          = 384
    RPL_TIME              = 391
    RPL_USERSSTART        = 392
    RPL_USERS             = 393
    RPL_ENDOFUSERS        = 394
    RPL_NOUSERS           = 395
    ERR_NOSUCHNICK        = 401
    ERR_NOSUCHSERVER      = 402
    ERR_NOSUCHCHANNEL     = 403
    ERR_CANNOTSENDTOCHAN  = 404
    ERR_TOOMANYCHANNELS   = 405
    ERR_WASNOSUCHNICK     = 406
    ERR_TOOMANYTARGETS    = 407
    ERR_NOSUCHSERVICE     = 408
    ERR_NOORIGIN          = 409
    ERR_NORECIPIENT       = 411
    ERR_NOTEXTTOSEND      = 412
    ERR_NOTOPLEVEL        = 413
    ERR_WILDTOPLEVEL      = 414
    ERR_BADMASK           = 415
    ERR_UNKNOWNCOMMAND    = 421
    ERR_NOMOTD            = 422
    ERR_NOADMININFO       = 423
    ERR_FILEERROR         = 424
    ERR_NONICKNAMEGIVEN   = 431
    ERR_ERRONEUSNICKNAME  = 432
    ERR_NICKNAMEINUSE     = 433
    ERR_NICKCOLLISION     = 436
    ERR_UNAVAILRESOURCE   = 437
    ERR_USERNOTINCHANNEL  = 441
    ERR_NOTONCHANNEL      = 442
    ERR_USERONCHANNEL     = 443
    ERR_NOLOGIN           = 444
    ERR_SUMMONDISABLED    = 445
    ERR_USERSDISABLED     = 446
    ERR_NOTREGISTERED     = 451
    ERR_NEEDMOREPARAMS    = 461
    ERR_ALREADYREGISTRED  = 462
    ERR_NOPERMFORHOST     = 463
    ERR_PASSWDMISMATCH    = 464
    ERR_YOUREBANNEDCREEP  = 465
    ERR_YOUWILLBEBANNED   = 466
    ERR_KEYSET            = 467
    ERR_CHANNELISFULL     = 471
    ERR_UNKNOWNMODE       = 472
    ERR_INVITEONLYCHAN    = 473
    ERR_BANNEDFROMCHAN    = 474
    ERR_BADCHANNELKEY     = 475
    ERR_BADCHANMASK       = 476
    ERR_NOCHANMODES       = 477
    ERR_BANLISTFULL       = 478
    ERR_NOPRIVILEGES      = 481
    ERR_CHANOPRIVSNEEDED  = 482
    ERR_CANTKILLSERVER    = 483
    ERR_RESTRICTED        = 484
    ERR_UNIQOPPRIVSNEEDED = 485
    ERR_NOOPERHOST        = 491
    ERR_NOSERVICEHOST     = 492
    ERR_UMODEUNKNOWNFLAG  = 501
    ERR_USERSDONTMATCH    = 502
    
    def notice(self, client, message, typ="GENERIC"):
        self.send(client, ":{} NOTICE {} :{}".format(
                client["server"],
                typ,
                message
            )
        )
        
    def command(self, client, typ=300, message="", autoStr=True):
        if type(message) == list:
            message = (" ".join(message))
        elif type(message) == str and autoStr:
            message = (":"+message)
        self.send(client, ":{} {:0>3} {} {}".format(
                client["server"],
                typ,
                client["nick"],
                message
            )
        )
    
    def message(self, client, From, Type, Name, Message):
        self.send(client, ":{} {} {} :{}".format(From,Type,Name,Message))
    
    def pong(self, client, id):
        self.send(client, "PONG :{}".format(id))
        
    def send(self, client, message):
        if type(message) == str:
            message = message.encode()
        client.write(message+b"\r\n")

irc = irc()

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

class channel:
    clients = []
    def send(self, message):
        pass
    
    def join(self, who):
        self.send("{} joined the channel.".format(who["nick"]))
        
    def part(self, who):
        self.send("{} left the channel.".format(who["nick"]))

class server:
    #Networking
    sock = None
    connections = {}
    net = {}
    
    #IRC
    server_info = {}
    channels = {}
    clients = {}
    commands = {}
    
    def registerCommand(self, command):
        def decorator(self, command, func):
            command = command.encode()
            if command not in self.commands:
                self.commands[command] = []
            self.commands[command].append(func)
            return func
        return lambda func: decorator(self, command, func)
    
    def irc_processCommand(self, client, raw):
        command = []
        tmp = raw.split(b" :",1)
        if len(tmp)>1:
            command = tmp[0].split(b" ") + [tmp[1]]
        else:
            command = tmp[0].split(b" ")
        
        try:
            if command[0] in self.commands:
                for function in self.commands[command[0]]:
                    function(self, client, raw, command)
            else:
                print("Unknown command: "+str(raw))
        except Exception as e:
            irc.notice(
                client,
                "An error occured when processing \"{}\": {}".format(
                    raw.decode(),
                    str(e)
                )
            )
            client.close()
    
    def __init__(self, host="0.0.0.0", port=0, readSize = 0xFFFF, \
                 idleCheck = 1, ping = 5, die = 5, dieTime = 60):        
        self.net = {
            "host": host,
            "port": port,
            "readSize": readSize,
            "idleCheck": idleCheck,
            "ping": ping,
            "die": die,
            "dieTime": dieTime
        }
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
        
        #Setup IRC
        chars = "".join([chr(c+32)+chr(c) for c in range(65,91)])
        
        self.server_info = {
            "version": "Python({}.{}.{}_{})".format(
                sys.version_info.major,
                sys.version_info.minor,
                sys.version_info.micro,
                sys.version_info.releaselevel
            ),
            "created": datetime.datetime.now() \
                       .strftime("%Y-%m-%dT%H:%M:%SZ"),
            "host": host,
            "client_modes": chars,
            "channel_modes": chars
        }
    
    def poll(self):
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
                    data = con.recv(self.net["readSize"])
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
            if self.net["dieTime"]:
                if self.connections[con].lastio + self.net["dieTime"] < now:
                    self.disconnect(self.connections[con], 1)
                    del self.connections[con]
            if self.connections[con].shouldClose:
                con.close()
                self.disconnect(self.connections[con],0)
                del self.connections[con]
        self.idle()
    
    def recv(self, client, data):
        commands = data.split(b"\r\n")
        if data[-1] != 0x0A: #0x0A = \n
            client.backbuf = client.backbuf + commands.pop()
        for command in commands:
            if command != b"":
                self.irc_processCommand(client, command)
    
    def connect(self, client):
        client["uuid"] = uuid.UUID(bytes=os.urandom(16))
        print("{} connected.".format(str(client)))
        
    def disconnect(self, client, reason):
        #Free nick
        nick = client["nick"].lower()
        if nick in self.clients:
            if self.clients[nick] == client:
                del self.clients[nick]
        print("{} disconnected.".format(str(client)))

    def idle(self):
        pass
    
    def error(self, client):
        pass
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

