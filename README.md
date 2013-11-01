Gwilio
======

Host your own Twilio clone for free.

Installation
------------

``` bash
pip install pygmail
pip install Gwilio
```

You should also create a new gmail address for your Gwilio server.

Usage
-----

Gwilio can receive SMS messages and can either reply to them or post the phone number and message to another server.

If you want to respond to messages directly, define a callback function which takes the phone number and the message as arguments.  Whatever string you return will be replied to the sender.

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
