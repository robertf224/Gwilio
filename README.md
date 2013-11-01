Gwilio
======

Host your own Twilio clone for free.  All you need to do is create a Gwilio server using a gmail address, and then define behavior for how to respond to SMS messages to that gmail address (Gwilio uses the SMS to email gateways provided by ISPs).

Installation
------------

``` bash
pip install pygmail
pip install Gwilio
```

You should also create a new gmail address for your Gwilio server.

Usage
-----

Gwilio can receive SMS messages and can either reply to them or post the phone number and message to another server, mimicking the functionality provided by Twilio.

If you want to respond to messages directly, define a callback function which takes the phone number and the message as arguments.  Whatever string you return will be the reply sent to the sender.

``` python
import Gwilio

def callback(number, message):
	if number == '9735550123' and message == 'password':
		return 'you may enter'

Gwilio.start('gmail-username', 'gmail-password', callback)
```

If you want to post the phone number and message to another server, just specify the post address.

``` python
import Gwilio

Gwilio.start('gmail-username', 'gmail-password', post='http://example.com/post-endpoint')
```

In both of these examples, you would send SMS messages to gmail-username@gmail.com for your defined behavior to be carried out.
