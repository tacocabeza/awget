=============== HOW TO RUN ==================

ss.py:
	
	python3 ss.py -p [port number]

	note that -p flag is optional. If no port number is
	given then the default with be port 6666.

	so running ss.py like below should also work

	python3 ss.py

awget:
	
	python3 awget -c [chainfile.txt] -u [url]

	note that -c [chaingang.txt] flag is optional. If no chainfile is
	given then a default 'chaingang.txt' will be used.
	if this 'chaingang.txt' file does not exist in the directory
	the program will exit.


	-u [url] however is required. if -u [url] is omitted
	the program will exit.

	given the info above you could also run awget like this

	python3 awget -u [url]

	where the default chainfile is chaingang.txt. assuming it exists inthe directory
	of course.


	NOTE: order of arguments do not matter


a note on chainfiles:
	
	do not add extra lines empty lines or
	omit ip addresses or port numbers (i.e <ip, >/ < ,port>)


