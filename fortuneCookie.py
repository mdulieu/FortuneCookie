#send one of 823 Fortune Cookie quotes

from bs4 import BeautifulSoup
import zulip
import os
import random
import requests

fortunes = []
for i in range(1,18):

	quotes = open("FortuneCookieQuotes" + str(i) + ".html", "rw")
	soup = BeautifulSoup(quotes)
	fortunesTemp = [t.string for t in soup.table.find_all('a')]
	fortunes += fortunesTemp[1:]

random.seed()

client = zulip.Client(os.environ['ZULIP_EMAIL'], os.environ['ZULIP_KEY']) 

def subscribe_all():
	global client
	response = requests.get('https://api.zulip.com/v1/streams', auth=requests.auth.HTTPBasicAuth(os.environ['ZULIP_EMAIL'], os.environ['ZULIP_KEY']))
	if response.status_code == 200:
		json = response.json()['streams']
		streams = [{'name': stream['name']} for stream in json]
		client.add_subscriptions(streams)
	else:
		raise Exception(response)

def handle_msg(msg):
	if '@**FortuneCookie**' in msg['content']:
		index = random.randint(0,len(fortunes)-1)
		fortune = fortunes[index]
		client.send_message({
    	"type": "stream",
    	#"to": "bot-test",
    	"to":msg["display_recipient"],
    	#"subject": "Fortune Cookie",
    	"subject": msg['subject'],
    	"content": fortune
		})
		


#client.add_subscriptions([{'name':'bot-test'}])
subscribe_all()

client.call_on_each_message(handle_msg)