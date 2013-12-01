import gmail, requests
import json, datetime, threading, time, smtplib, signal, sys


def start(username, password, callback=None, post=None, sleeptime=30):

	# Make sure callback or post address is provided, and not both
	if not (bool(callback) ^ bool(post)):
		return

	# Pre-read unread emails so we're only listening for new ones
	g = gmail.login(username, password)
	if not g.logged_in:
		return
	emails = g.inbox().mail(unread=True, after=datetime.date.today()-datetime.timedelta(1))
	for email in emails:
		email.read()
	g.logout()

	# Set up signal handler
	def stop(signal, frame):
		if g.logged_in:
			g.logout()
		sys.exit(0)
	signal.signal(signal.SIGINT, stop)

	# Start fetching emails
	while True:

		# Log into gmail
		g = gmail.login(username, password)
		if not g.logged_in:
			return

		# Fetch new emails and read them
		emails = g.inbox().mail(unread=True, after=datetime.date.today()-datetime.timedelta(1))
		for email in emails:
			email.fetch()
			email.read()
		g.logout()

		# Start responding/replying
		for email in emails:
			number = email.fr[:email.fr.index('@')]
			reply = None

			# Forward message, retrieve reply
			if callback is not None:
				reply = callback(number, email.body)
			else:
				r = requests.post(post, data={'number': number, 'message': email.body})
				reply = r.text

			# If there is one, send reply
			if reply is not None:
				# reply to email
				server = smtplib.SMTP('smtp.gmail.com:587')
				server.ehlo()
				server.starttls()
				server.ehlo()
				server.login(username,password)
				server.sendmail(username+'@gmail.com', email.fr, reply)
				server.quit()

		# Sleep for designated amount of time
		time.sleep(sleeptime)


