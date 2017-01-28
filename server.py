import ssock
import uuid
import os
import IRC
import sys
import datetime

irc = IRC.irc()

class channel:
    clients = []
    def send(self, message):
        pass
    
    def join(self, who):
        self.send("{} joined the channel.".format(who["nick"]))
        
    def part(self, who):
        self.send("{} left the channel.".format(who["nick"]))

class server(ssock.server):
    server_info = {}
    channels = {}
    clients = {}
    def irc_processCommand(self, client, raw):
        command = []
        tmp = raw.split(b" :",1)
        if len(tmp)>1:
            command = tmp[0].split(b" ") + [tmp[1]]
        else:
            command = tmp[0].split(b" ")
        
        try:
            if command[0] == b"NICK":
                nick = command[1].decode().lower()
                if nick in self.clients:
                    if self.clients[nick] == client:
                        pass
                    else:
                        irc.command(client, irc.ERR_NICKNAMEINUSE,
                            "Nickname is already in use, using UUID."
                        )
                        nick = str(client["uuid"]).lower()
                else:
                    self.clients[nick] = client
                client["nick"] = command[1].decode()
            elif command[0] == b"USER":
                client["user"] = command[1].decode()
                client["mode"] = int(command[2].decode())
                client["server"] = command[3].decode()
                client["realname"] = command[4].decode()
                client["mask"] = client["nick"]+"!~"+client["realname"]+"@"+client.host
                irc.command(client, irc.RPL_WELCOME,
                    "Welcome {}".format(client["mask"])
                )
                irc.command(client, irc.RPL_YOURHOST,
                    "Your host is {}".format(self.server_info["host"])
                )
                irc.command(client, irc.RPL_CREATED,
                    "Server created at {}.".format(
                        self.server_info["created"]
                    )
                )
                irc.command(client, irc.RPL_MYINFO,
                    [client["server"], self.server_info.get("version"), 
                    self.server_info.get("client_modes", ""),
                    self.server_info.get("channel_modes", "")
                    ]
                )
            elif command[0] == b"PING":
                irc.pong(client, command[1].decode())
            elif command[0] == b"NOTICE":
                nick = command[1].decode().lower()
                if nick in self.clients:
                    irc.message(
                        self.clients[nick],
                        client["mask"],
                        "NOTICE",
                        client["nick"].lower(),
                        command[2].decode()
                    )
            elif command[0] == b"PRIVMSG":
                nick = command[1].decode().lower()
                if nick in self.clients:
                    irc.message(
                        self.clients[nick],
                        client["mask"],
                        "PRIVMSG",
                        client["nick"].lower(),
                        command[2].decode()
                    )
            elif command[0] == b"QUIT":
                client.close()
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
        #print("[{}] {}".format(str(client), command.decode()))
    
    def init(self, opts):
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
            "host": opts.get("host", "Unknown"),
            "client_modes": chars,
            "channel_modes": chars
        }
    
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

server = server(port = 6667)
