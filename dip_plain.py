import sleekxmpp
import random
import time
import logging

#Setup logging
logging.basicConfig(format='%(levelname)-8s %(message)s')
 
def message(xmpp):
	#a list of all printable chars
	pool = list('!#$%&()*+,-./:;<=>?@[\]^_{|}~/0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_abcdefghijklmnopqrstuvwxyz{|}~')

	xmpp.send_message(mto='ken@ubuntu',mbody='Hello World!!!', 
		mtype= 'chat')

	
def main():
	name = 'a'*10240
	xmpp = sleekxmpp.ClientXMPP('bill@ubuntu/test', 'bill')
	xmpp['feature_mechanisms'].unencrypted_plain = True # Force plaintext authentication https://groups.google.com/forum/?fromgroups=#!topic/sleekxmpp-discussion/RCzU4qa0Bfg
	xmpp.connect(address=('172.16.206.152', 5222), use_tls = False)
	xmpp.process(block=False)
	xmpp.send_presence()
	#xmpp.get_roster()
	
	i = 1

	while i > 0:
		message(xmpp)
		time.sleep(1)
		i -= 1

	xmpp.disconnect(wait=True)


if __name__ == '__main__':
	main()