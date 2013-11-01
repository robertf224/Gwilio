import gmail, requests
import json, datetime, threading, time, smtplib, signal, sys


def start(username, password, callback=None, post=None):

	# make sure callback or post address is provided, and not both
	if not (bool(callback) ^ bool(post)):
		return

	# Pre-read unread emails so we're only listening for new ones
	g = gmail.login(username, password)
	if not g.logged_in:
		return
	emails = g.inbox().mail(unread=True, after=datetime.date.today())
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
		g = gmail.login(username, password)
		if not g.logged_in:
			return

		# fetch emails
		emails = g.inbox().mail(unread=True, after=datetime.date.today())
		for email in emails:
			email.fetch()
			email.read()
		g.logout()

		# start responding/replying
		for email in emails:
			number = email.fr[:email.fr.index('@')]
			if callback is not None:
				reply = callback(number, email.body)
				if reply is not None:
					# reply to email
					server = smtplib.SMTP('smtp.gmail.com:587')
					server.ehlo()
					server.starttls()
					server.ehlo()
					server.login(username,password)
					server.sendmail(username+'@gmail.com', email.fr, reply)
					server.quit()
			else:
				requests.post(post, data={'number': number, 'message': email.body})

		time.sleep(20)


