'''
An FTP server module that allows anonymous login
and allows read/write access to anyone
@author Cody Chinn, Justin Johns, James Lund, Zachary Thomas
@version Winter 2019
'''

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
from ftplib import FTP
from threading import Thread
import os, socket, csv


# Create the FTP client object to send requests to the FTP servers
ftp = FTP('')

# filling data_stored with test values
#data_stored = {'35.40.130.191': ['foo', 'bar'], '36.40.130.191': ['new', 'test']}
data_stored={}
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
				# print('Dictonary')
				# print(data_stored)
				return_list(data_stored)
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



def return_list(data_stored):
	#global data_stored
	print(data_stored)
	file_list = []
	with open('FullList.csv', 'w') as csvfile:
		#delimiter=',', quotechar="|",quoting=csv.QUOTE_MINIMAL
		fieldnames = ['ip', 'files']
		filewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
		filewriter.writeheader()
		for key in data_stored:
			filewriter.writerow({'ip':key, 'files':data_stored[key]})


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
	#return_list()
	main()
	thread.join()
