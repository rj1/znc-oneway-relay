import znc
import json

class relay(znc.Module):

    description = "oneway relay"
    module_types = [znc.CModInfo.UserModule]

    def OnChanMsg(self, nick, channel, message):
        if str(channel.GetName()).lower() == "#source":
            network = self.GetUser().FindNetwork("target-network")
            network.PutIRC(f"PRIVMSG #target-channel :<{str(nick)}> {str(message)}")
        return znc.CONTINUE

