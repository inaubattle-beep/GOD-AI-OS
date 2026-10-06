from typing import Dict, Any, List, Optional
import time

class CommunicationChannel:
    def __init__(self, channel_id: str, name: str, channel_type: str, provider: str = "builtin", status: str = "ONLINE"):
        self.channel_id = channel_id
        self.name = name
        self.channel_type = channel_type # facebook, whatsapp, email, sms, local_message, telegram, slack, vicidial
        self.provider = provider
        self.status = status

class CommunicationsHub:
    def __init__(self):
        self._channels: Dict[str, CommunicationChannel] = {}
        self._dispatch_logs: List[Dict[str, Any]] = []
        self._register_default_channels()

    def _register_default_channels(self):
        self.register_channel(CommunicationChannel("facebook-messenger", "Facebook Messenger / Meta API", "facebook", provider="meta"))
        self.register_channel(CommunicationChannel("whatsapp-business", "WhatsApp Business Cloud API", "whatsapp", provider="meta"))
        self.register_channel(CommunicationChannel("email-gateway", "Executive SMTP/IMAP Email Gateway", "email", provider="smtp"))
        self.register_channel(CommunicationChannel("sms-gateway", "Twilio & Cellular SMS Modem Gateway", "sms", provider="twilio"))
        self.register_channel(CommunicationChannel("local-message", "Local OS & Desktop System Notification", "local_message", provider="system"))
        self.register_channel(CommunicationChannel("telegram-bot", "Telegram Alert Bot", "telegram", provider="telegram"))
        self.register_channel(CommunicationChannel("slack-ops", "Slack DevOps Alerts", "slack", provider="slack"))
        self.register_channel(CommunicationChannel("vicidial-ivr", "ViciDial Telephony & Voice IVR", "vicidial", provider="vicidial"))

    def register_channel(self, channel: CommunicationChannel):
        self._channels[channel.channel_id] = channel

    def list_channels(self) -> List[Dict[str, Any]]:
        return [
            {
                "channel_id": c.channel_id,
                "name": c.name,
                "channel_type": c.channel_type,
                "provider": c.provider,
                "status": c.status
            }
            for c in self._channels.values()
        ]

    def dispatch_message(self, channel_id: str, recipient: str, message_text: str, media_url: Optional[str] = None) -> Dict[str, Any]:
        if channel_id not in self._channels:
            raise ValueError(f"Channel '{channel_id}' not found.")
        
        channel = self._channels[channel_id]
        log = {
            "dispatch_id": f"disp-{len(self._dispatch_logs) + 101}",
            "timestamp": time.time(),
            "channel_id": channel_id,
            "channel_type": channel.channel_type,
            "provider": channel.provider,
            "recipient": recipient,
            "message_snippet": message_text[:120],
            "media_url": media_url,
            "status": "SENT"
        }
        self._dispatch_logs.append(log)
        return log

    def get_logs(self) -> List[Dict[str, Any]]:
        return self._dispatch_logs[-20:]

comm_hub = CommunicationsHub()
