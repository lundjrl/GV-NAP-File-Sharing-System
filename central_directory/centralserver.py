'''
An FTP server module that allows anonymous login
and allows read/write access to anyone

@author Cody Chinn
@version Winter 2019
'''

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
import os
import socket
from threading import Thread

data_stored = {}
'''
This is a function that needs to be kicked off in a thread.
It continuously checks for new files in the current directory
which should only be update files on this server
'''
def check_dir():
	global data_stored
	while 1:
		file_dict= {}

		files = os.listdir()
		for file in files:
			file_dict[file] = file

		if 'update.txt' in file_dict:
		#Read in files line by line
			with open(file_dict['update.txt']) as f:
				content = f.readlines()
			if not content:
				pass
			else:
				# Get rid of the white space and '\n' chars
				content = [x.strip() for x in content]
				#Set first line of txt file to key
				#And every line after to it's list values
				#print(content[1:len(content)])
				data_stored[content[0]] = list(content[1:len(content)])
				print('Dictonary')
				print(data_stored)

				os.remove('update.txt')
				continue
				#print(data_stored) # Keep this here for testing data_stored
		elif 'search.txt' in file_dict:
			with open(file_dict['search.txt']) as f:
				search = f.readlines()
			if not search:
				pass
			else:
				for ip, file_name in data_stored.items():
					file = ''.join(file_name)
					if search[0] in file:
						print(ip)
					else:
						print('File not found')
				os.remove('search.txt')
				continue


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
    server = ThreadedFTPServer(('127.0.0.1', 1026), handler)
    server.serve_forever()


'''
Runs the main loop
'''
if __name__ == "__main__":
	#Create the thread for continuous checking
	#and kick it off with .start()
	thread = Thread(target = check_dir)
	thread.start()
	main()
	thread.join()
