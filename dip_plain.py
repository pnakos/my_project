#!/usr/bin/python

import sleekxmpp
import random
import time
import logging
import argparse

# Argument parser set-up
parser = argparse.ArgumentParser()
parser.add_argument("--connection", help="Fuzz the JID fields(node, domain, resource)", action="store_true")# action="store_true" no need for argument
args = parser.parse_args()

#Setup logging
logging.basicConfig(format='%(levelname)-8s %(message)s')
 
def message(xmpp):
	#a list of all printable chars
	pool = list('!#$%&()*+,-./:;<=>?@[\]^_{|}~/0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_abcdefghijklmnopqrstuvwxyz{|}~')

	xmpp.send_message(mto='ken@ubuntu',mbody='Hello World!!!', 
		mtype= 'chat')

def fuzz_connection():
	payload = 'a' * 1024

	xmpp = sleekxmpp.ClientXMPP(payload +'@ubuntu/test', 'bill')
	xmpp['feature_mechanisms'].unencrypted_plain = True # Force plaintext authentication https://groups.google.com/forum/?fromgroups=#!topic/sleekxmpp-discussion/RCzU4qa0Bfg
	xmpp.connect(address=('172.16.206.152', 5222), use_tls = False)
	xmpp.disconnect(wait=True)

	# xmpp = sleekxmpp.ClientXMPP('bill@' + payload + '/test', 'bill')
	# xmpp['feature_mechanisms'].unencrypted_plain = True # Force plaintext authentication https://groups.google.com/forum/?fromgroups=#!topic/sleekxmpp-discussion/RCzU4qa0Bfg
	# xmpp.connect(address=('172.16.206.152', 5222), use_tls = False)
	# xmpp.disconnect(wait=True)

	xmpp = sleekxmpp.ClientXMPP('bill@ubuntu/' + payload, 'bill')
	xmpp['feature_mechanisms'].unencrypted_plain = True # Force plaintext authentication https://groups.google.com/forum/?fromgroups=#!topic/sleekxmpp-discussion/RCzU4qa0Bfg
	xmpp.connect(address=('172.16.206.152', 5222), use_tls = False)
	xmpp.disconnect(wait=True)

	xmpp = sleekxmpp.ClientXMPP(payload + '@ubuntu/' + payload, 'bill')
	xmpp['feature_mechanisms'].unencrypted_plain = True # Force plaintext authentication https://groups.google.com/forum/?fromgroups=#!topic/sleekxmpp-discussion/RCzU4qa0Bfg
	xmpp.connect(address=('172.16.206.152', 5222), use_tls = False)
	xmpp.disconnect(wait=True)
	
def main():
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
	if args.connection:
		print "Fuzzing JID fields..."
		fuzz_connection()
	else:
		main()