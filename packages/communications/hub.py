from typing import Dict, Any, List, Optional
import time

class CommunicationChannel:
    def __init__(self, channel_id: str, name: str, channel_type: str, status: str = "ONLINE"):
        self.channel_id = channel_id
        self.name = name
        self.channel_type = channel_type # email, telegram, whatsapp, slack, vicidial
        self.status = status

class CommunicationsHub:
    def __init__(self):
        self._channels: Dict[str, CommunicationChannel] = {}
        self._dispatch_logs: List[Dict[str, Any]] = []
        self._register_default_channels()

    def _register_default_channels(self):
        self.register_channel(CommunicationChannel("email-main", "Executive Email Gateway", "email"))
        self.register_channel(CommunicationChannel("telegram-bot", "Telegram Alert Bot", "telegram"))
        self.register_channel(CommunicationChannel("whatsapp-business", "WhatsApp Business API", "whatsapp"))
        self.register_channel(CommunicationChannel("slack-ops", "Slack DevOps & Alerts", "slack"))
        self.register_channel(CommunicationChannel("vicidial-ivr", "ViciDial Telephony & Voice IVR", "vicidial"))

    def register_channel(self, channel: CommunicationChannel):
        self._channels[channel.channel_id] = channel

    def list_channels(self) -> List[Dict[str, Any]]:
        return [
            {
                "channel_id": c.channel_id,
                "name": c.name,
                "channel_type": c.channel_type,
                "status": c.status
            }
            for c in self._channels.values()
        ]

    def dispatch_message(self, channel_id: str, recipient: str, message_text: str) -> Dict[str, Any]:
        if channel_id not in self._channels:
            raise ValueError(f"Channel '{channel_id}' not found.")
        
        channel = self._channels[channel_id]
        log = {
            "dispatch_id": f"disp-{len(self._dispatch_logs) + 101}",
            "timestamp": time.time(),
            "channel_id": channel_id,
            "channel_type": channel.channel_type,
            "recipient": recipient,
            "message_snippet": message_text[:100],
            "status": "SENT"
        }
        self._dispatch_logs.append(log)
        return log

    def get_logs(self) -> List[Dict[str, Any]]:
        return self._dispatch_logs[-20:]

comm_hub = CommunicationsHub()
