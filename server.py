import IRC

server = IRC.server(port = 6667)
irc = IRC.irc

@server.registerCommand("NICK")
def command_nick(self, client, raw, command):
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


@server.registerCommand("USER")
def command_user(self, client, raw, command):
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


@server.registerCommand("PING")
def command_ping(self, client, raw, command):
    irc.pong(client, command[1].decode())


@server.registerCommand("NOTICE")
def command_notice(self, client, raw, command):
    nick = command[1].decode().lower()
    if nick in self.clients:
        irc.message(
            self.clients[nick],
            client["mask"],
            "NOTICE",
            client["nick"].lower(),
            command[2].decode()
        )
        

@server.registerCommand("PRIVMSG")
def command_privmsg(self, client, raw, command):
    nick = command[1].decode().lower()
    if nick in self.clients:
        irc.message(
            self.clients[nick],
            client["mask"],
            "PRIVMSG",
            client["nick"].lower(),
            command[2].decode()
        )


@server.registerCommand("QUIT")
def command_quit(self, client, raw, command):
    client.close()

while True:
    server.poll()
