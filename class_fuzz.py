#!/usr/bin/python

import sleekxmpp
import random
import time
import logging
import argparse
import thread
import sys

class MessageFuzzer(sleekxmpp.ClientXMPP):
	"""docstring for Fuzz
	"""
	def __init__(self, jid, password):
		sleekxmpp.ClientXMPP.__init__(self, jid, password)
		self['feature_mechanisms'].unencrypted_plain = True # Force plaintext authentication https://groups.google.com/forum/?fromgroups=#!topic/sleekxmpp-discussion/RCzU4qa0Bfg
		self.connect(address=('172.16.206.152', 5222), use_tls = False)
		self.process(block=False)
		self.add_event_handler("session_start", self.start)

	def start(self, event):
		self.send_presence()
		self.send_message(mto="ken@ubuntu",mbody="Hello World!!!",mtype='chat')
		self.disconnect(wait=True)


class ConnectionFuzzer(sleekxmpp):
	"""docstring for ConnectionFuzzer"""
	def __init__(self, arg):
		super(ConnectionFuzzer, self).__init__()
		self.arg = arg
		


if __name__ == '__main__':

	# Argument parser set-up
	parser = argparse.ArgumentParser()
	parser.add_argument("--connection", help="Fuzz the JID fields(node, domain, resource)", action="store_true")# action="store_true" no need for argument
	args = parser.parse_args()

	# Setup logging
	logging.basicConfig(format='%(levelname)-8s %(message)s')

	# Read fuzzing strings
	fuzz = open("fuzz_strings.txt", 'r')

	if args.connection:
		print "Fuzzing JID fields..."
		for j in range(5):
			thread.start_new_thread(Fuzzer.fuzz_connection,())
		while True:
			pass
	
	else:
		MessageFuzzer("bill@ubuntu/test", "bill")
