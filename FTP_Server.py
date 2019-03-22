'''
An FTP server module that allows anonymous login
and allows read/write access to anyone

@author Cody Chinn
@version Winter 2019
'''

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer


'''
The main loop that starts the server
'''
def main():
	# Creates authorization for anonymous users
	# and gives them Read/Write access to the server
	authorizer = DummyAuthorizer()
	authorizer.add_anonymous('.', perm='elradfmwM')

	# Using the default pyftpdlib handler to handle
	# requests sent to the server
	handler = FTPHandler
	handler.authorizer = authorizer

	# Starts the threaded server on the localhost ip
	# on port 1026 then runs it forever
	server = ThreadedFTPServer(('127.0.0.1', 1026), handler)
	server.serve_forever()

'''
Runs the main loop
'''
if __name__ == "__main__":
	main()
