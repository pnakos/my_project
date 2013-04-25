#!/usr/bin/python

"""
	XMPP Fuzzer v0.1

	An XMPP Fuzzer based on a tweaked SleekXMPP: The Sleek XMPP Library
	Copyright (C) 2010  Nathanael C. Fritz

	The fields that are fuzzed are the JID , message to: field and 
	message type field.

	pnakos@gmail.com
"""

import sleekxmpp
import random
import time
# import logging
import argparse
# import thread
import sys

class MessageFuzzer(sleekxmpp.ClientXMPP):
	"""
	docstring for Fuzz
	"""
	def __init__(self, jid, password, recipient, msg_typ):
		sleekxmpp.ClientXMPP.__init__(self, jid, password)
		self['feature_mechanisms'].unencrypted_plain = True # Force plaintext authentication https://groups.google.com/forum/?fromgroups=#!topic/sleekxmpp-discussion/RCzU4qa0Bfg
		self.connect(address=('172.16.206.152', 5222), use_tls = False)
		self.process(block=False)
		self.recipient = recipient
		self.msg_typ = msg_typ
		self.add_event_handler("session_start", self.start)

	def start(self, event):
		"""
		Process the session_start event.
		"""
		self.send_presence()
		self.get_roster()

		self.send_message(mto=self.recipient,mbody="Hello World!!!",mtype=self.msg_typ)

		self.disconnect(wait=True)


class ConnectionFuzzer(sleekxmpp.ClientXMPP):
	"""
	docstring for ConnectionFuzzer
	"""
	def __init__(self, jid, password):
		sleekxmpp.ClientXMPP.__init__(self, jid, password)
		self['feature_mechanisms'].unencrypted_plain = True # Force plaintext authentication https://groups.google.com/forum/?fromgroups=#!topic/sleekxmpp-discussion/RCzU4qa0Bfg
		self.connect(address=('172.16.206.152', 5222), use_tls = False)
		self.process(block=False)
		self.add_event_handler("session_start", self.start, threaded=True)
		# self.add_event_handler("failed_auth", self.failed_auth, threaded=True)
		# self.add_event_handler("disconnected", self.disconnected, threaded=True)

	def start(self, event):
		"""
		Process the session_start event.
		"""
		self.send_presence()
		self.disconnect(wait=False)
		
	# def failed_auth(self, event):
	# 	print "Authentication Failed"
		
	# def disconnected(self):
	# 	self.disconnect(wait=False)
		



if __name__ == '__main__':

	# Argument parser set-up
	parser = argparse.ArgumentParser()
	parser.add_argument("--connection", help="Fuzz the JID fields(node, domain, resource)", action="store_true")# action="store_true" not mandatory argument
	args = parser.parse_args()

	# Setup logging
	# logging.basicConfig(format='%(levelname)-8s %(message)s')

	# Open fuzzing strings file
	fuzz = open("fuzz_strings.txt", "r")

	if args.connection:
		print "Fuzzing JID fields..."
		line = fuzz.readline()
		
		while line != '':
			print "Fuzzing string... " + line.strip()
			#thread.start_new_thread(ConnectionFuzzer,(line.strip() + '@ubuntu/test', 'bill'))
			ConnectionFuzzer(line.strip() + "@ubuntu/test", "bill")
			# ConnectionFuzzer("bill@" + line.strip() + "/test", "bill")
			ConnectionFuzzer("bill@ubuntu/" + line.strip(), "bill")
			time.sleep(0.25)
			line = fuzz.readline()

		fuzz.close()
		sys.exit()
				
	else:
		
		print "Fuzzing message fields mto and mtype fields..."
		line = fuzz.readline()
		
		while line != '':
			print "Fuzzing string... " + line.strip()
			MessageFuzzer("bill@ubuntu/test", "bill", line + "@ubuntu", line)
			time.sleep(0.25)
			line = fuzz.readline()

		fuzz.close()
		sys.exit()
		
