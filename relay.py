import znc

class relay(znc.Module):

    description = "oneway relay"
    module_types = [znc.CModInfo.UserModule]

    def OnChanMsg(self, nick, channel, message):
        self._sendMsg(nick, channel, f"<{nick}> {message}")
        return znc.CONTINUE

    def OnChanAction(self, nick, channel, message):
        self._sendMsg(nick, channel, f"*{nick} {message}")
        return znc.CONTINUE

    def _sendMsg(self, network, channel, message):
        if str(channel.GetName()).lower() == channel:
            network = self.GetUser().FindNetwork(network)
            network.PutIRC(f"PRIVMSG {channel} :{message}")
        return znc.CONTINUE
