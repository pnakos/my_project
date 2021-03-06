#!/usr/bin/python

import sleekxmpp
import time
import re
import argparse
import sys
import logging

def banner():
	"""
	XMPP Fuzzer v0.1

	An XMPP Fuzzer based on a modified MIT Licensed 
	SleekXMPP: The Sleek XMPP Library
	Copyright (C) 2010  Nathanael C. Fritz, 

	The fields that are fuzzed are JID , "message to:" field, "subject" 
	field and "message type" field.

	Pantelis Nakos, University of Piraeus, 2013

	pnak.dev@gmail.com

	"""
	return banner.__doc__

print banner()

#Logging levels: CRITICAL, ERROR, WARNING, INFO or DEBUG
#logging.basicConfig(level=logging.ERROR)

# Regular expression for a valid JID format
JID_PATTERN = \
re.compile("^(?:(.{1,10250})@)?([^/@]{1,10250})(?:/(.{1,10250}))?$")

class MessageFuzzer(sleekxmpp.ClientXMPP):
	"""
	A basic sleekXMPP bot that will log in, 
	send a message and then log out.

	"""
	def __init__(self, jid, password, recipient, subject, msg_typ):
		sleekxmpp.ClientXMPP.__init__(self, jid, password)
		self['feature_mechanisms'].unencrypted_plain = True
		self.connect(address=(args.server, 5222), use_tls = False)
		self.process(block=False)
		self.recipient = recipient
		self.msg_typ = msg_typ
		self.subject = subject
		self.add_event_handler("session_start", self.start, threaded=True)

	def start(self, event):
		"""
		Process the session_start event.

		"""
		self.send_presence()
		self.get_roster()

		self.send_message(mto=self.recipient, msubject = self.subject, \
			mbody="Hello World!!!", mtype=self.msg_typ)

		self.disconnect(wait=True)


class ConnectionFuzzer(sleekxmpp.ClientXMPP):
	"""
	A basic sleekXMPP bot that will try to log in
	and then log out.

	"""
	def __init__(self, jid, password):
		sleekxmpp.ClientXMPP.__init__(self, jid, password)
		self['feature_mechanisms'].unencrypted_plain = True
		self.connect(address=(args.server, 5222), use_tls = False)
		self.process(block=False)
		self.add_event_handler("session_start", self.start, threaded=True)
		
	def start(self, event):
		"""
		Process the session_start event.

		"""
		self.send_presence()
		self.disconnect(wait=False)
	

if __name__ == '__main__':
	try:
		# Argument parser set-up
		parser = argparse.ArgumentParser()
		parser.add_argument("-s", "--server", \
			help="XMPP server IP address to fuzz")
		parser.add_argument("-l", "--login", \
			help="Valid login name for message fuzzing(e.g username@domain)")
		parser.add_argument("-p", "--password", \
			help="Password for the login name provided")
		parser.add_argument("-c", "--connection", \
			help="Fuzz the JID fields(node, domain, resource)", \
			action="store_true")# action="store_true" not mandatory argument
		args = parser.parse_args()

		def parse_JID(data):
			"""
			Parse the username and domain name
			from the JID.

			"""

			match = JID_PATTERN.match(data)

			(node, domain, resource) = match.groups()

			return node, domain

		jid = parse_JID(args.login)

		usrname = jid[0]

		domain = jid[1]

		# Open fuzzing strings file
		try:
			fuzz = open("fuzz_strings.txt", "r")
		except IOError:
			print "File fuzz_strings.txt not found."
			sys.exit()
			
		if args.connection:
			print "Fuzzing JID fields..."
			line = fuzz.readline()
			flag = 0
			
			# For every line in file call ConnectionFuzzer using the line 
			# for username and /resource.
			while line != '':
				print str(flag) + " Fuzzing string... " + line.strip()
				ConnectionFuzzer(line.strip() + "@" + line.strip() + "/" + \
					line.strip(), "pass")
				ConnectionFuzzer(line.strip() + "@" + domain + \
					"/test", args.password)
				ConnectionFuzzer(usrname + "@" + line.strip() + \
					"/test", args.password)
				ConnectionFuzzer(args.login + "/" + \
					line.strip(), args.password)
				time.sleep(0.25)
				line = fuzz.readline()
				flag += 1

			fuzz.close()
			sys.exit()
					
		else:
			
			print "Fuzzing message fields mto, msubject and mtype..."
			line = fuzz.readline()
			flag1 = 0
			
			# For every line in file call MessageFuzzer using the line 
			# for recipients name and message type.
			while line != '':
				print str(flag1) + " Fuzzing string... " + line.strip()
				MessageFuzzer(args.login, args.password, line.strip() + "@" \
					+ domain, line.strip(), line.strip())
				time.sleep(0.25)
				line = fuzz.readline()
				flag1 += 1

			fuzz.close()
			sys.exit()
	except TypeError:
		print "Wrong or no arguments given. Use -h for help."
		sys.exit()
		
