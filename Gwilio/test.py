import Gwilio

def callback(number, message):
	if number == '9734876086':
		return 'thanks!'

Gwilio.start('gwilio123', 'homegrowntwilio', post='http://fidler.io:8888')

