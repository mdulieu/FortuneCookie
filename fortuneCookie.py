import zulip
import os

client = zulip.Client(os.environ['ZULIP_EMAIL'], os.environ['ZULIP_KEY']) 

# Send a stream message
client.send_message({
    "type": "stream",
    "to": "bot-test",
    "subject": "Fortune Cookie",
    "content": "Meeting adversity well is the source of your strength."
})
