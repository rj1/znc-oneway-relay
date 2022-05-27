import znc

class relay(znc.Module):

    description = "oneway relay"
    module_types = [znc.CModInfo.UserModule]

    def OnLoad(self, args, message):
        self.relays = {}
        message.s = "loading relay module"
        return True

    def OnModCommand(self, command):
        command = str(command)
        if command == "help":
            self.PutModule("commands:")
            self.PutModule("help - show this help message")
            self.PutModule("add - add a relay - e.g. add <sourcechannel> <targetnetwork> <targetchannel>")
            self.PutModule("del - delete a relay - e.g. del <relayid>")
            return self.PutModule("list - list all relays")

        if command.startswith("add"):
            return self._addRelay(command)

        if command.startswith("del"):
            return self._delRelay(command)

        if command == "list":
            if not self.relays:
                return self.PutModule("no relays are configured, please configure one")

            for i,relay in self.relays.items():
                self.PutModule(f"[{i}] {relay['sourceChan']} -> {relay['targetNet']}.{relay['targetChan']}")
            return

        return self.PutModule("unknown command, type help")

    def OnChanMsg(self, nick, channel, message):
        for relay in self.relays.values():
            if str(channel.GetName()).lower() == relay['sourceChan'].lower():
                network = self.GetUser().FindNetwork(relay['targetNet'])
                formattedMsg = f"<{nick}> {message}"
                network.PutIRC(f"PRIVMSG {relay['targetChan']} :{formattedMsg}")
        return znc.CONTINUE

    def OnChanAction(self, nick, channel, message):
        for relay in self.relays.values():
            if str(channel.GetName()).lower() == relay['sourceChan'].lower():
                network = self.GetUser().FindNetwork(relay['targetNet'])
                formattedMsg = f"*{nick} {message}"
                network.PutIRC(f"PRIVMSG {relay['targetChan']} :{formattedMsg}")
        return znc.CONTINUE

    def _addRelay(self, cmd):
        parts = cmd.split()
        if len(parts) < 4:
            self.PutModule("usage: add <sourcechannel> <targetnetwork> <targetchannel>")
            return self.PutModule("e.g. add #znc privatenetwork #znc-relay")

        if not parts[1].startswith("#") or not parts[3].startswith("#"):
            return self.PutModule("irc channels must start with #")

        for relay in self.relays.values():
            if relay['sourceChan'] == parts[1]:
                return self.PutModule("relay already exists")

        relay = {
            'sourceChan': parts[1],
            'targetNet': parts[2],
            'targetChan': parts[3]
        }

        self.relays[len(self.relays)] = relay
        # self.nv['relays'] = self.relays
        return self.PutModule(f"relay for {relay['sourceChan']} added!")

    def _delRelay(self, cmd):
        # delete relay
        parts = cmd.split()
        if len(parts) < 2:
            self.PutModule("usage: del <relayid>")
            return self.PutModule("e.g. del 0")

        try:
            relayId = int(parts[1])
        except ValueError:
            return self.PutModule("relay id must be an integer")

        if relayId not in self.relays:
            return self.PutModule("relay id not found")

        del self.relays[relayId]
        # self.nv['relays'] = self.relays
        return self.PutModule("relay deleted")

