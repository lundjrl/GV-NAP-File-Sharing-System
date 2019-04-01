'''
FTP Client module. Handles commands CONNECT, LIST, STORE and RETRIEVE
to communicate with an FTP server.

@author Cody Chinn
@version Winter 2019

'''
import os

# pip install ftpdlib before running the client
from ftplib import FTP

# Create the FTP client object to send requests to the FTP server
ftp = FTP('')

# Check whether or not the client is connected to a server
connected = False


'''
Handles a CONNECT request to communicate with an FTP server.

@param ip (str)- The ip address of the server
@param port (str)- The port number to access the FTP server on
'''
def connect(ip, port):
	global connected

	try:
		# Cast port to int for ftpdlib then login
		ftp.connect(ip, int(port))
		ftp.login()
		print('You\'re connected to ' + str(ip) + ' on port ' + port)
		connected = True
		prompt()
	except Exception as e:
		# If the server can't be found, handle the error
		print(e)
		prompt()


'''
Handles the STORE request. Sends a file to the FTP server the client
is connected to

@param filename (str) - The name of the file being sent to the server
'''
def store(filename):
	try:
		# Full ftpdlib command to send a file to a server
		ftp.storbinary('STOR ' + filename, open(filename, 'rb'))
		print('Successfully uploaded ' + filename)
	except:
		# If the file couldn't be sent, handle the error
		print('2')

'''
Handles the RETRIEVE request being sent to the FTP server.

@param filename (str) - name of the file being requested from
		  	the ftp server
'''
def retrieve(filename):
	try:
		# Open the locally stored file and send it to the server
		localfile = open(filename, 'wb')
		ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
		localfile.close()
		print('Successfully downloaded ' + filename)
	except:
		# If the file can't be found, handle the error
		print('Cannot find ' + filename + ' on the FTP server')

'''
Checks to see if the client is connected to an FTP server

@return connected (bool) - True if connected, False if not
'''
def checkConnection():
	global ftp, connected

	try:
		# Noop is a way to check connection to server
		ftp.voidcmd("NOOP")
		connected = True
	except:
		# If connection is lost or was never started, handle error
		connected = False
		print('You aren\'t connected to a server, please use CONNECT to try again')

	return connected


'''
Stores the files from the client and the search term in a text file
'''
def createLocalDescription(search):
	gw = os.popen("ip -4 route show default").read().split()
	updatefile = open("update.txt","w")
	updatefile.write(gw[3] + "\n")
	currentfiles = os.listdir()
	for i in currentfiles:
		updatefile.write(i + "\n")
	updatefile.write(str(search) + '\n')
	updatefile.close()


'''
The command interface for the FTP client. This is called at the
end of every command sent to the server to keep the interface open.
Also checks the input from the user for the four accepted arguments
and sends the commands to the appropriate handlers.
'''
def prompt():
	global connected, ftp

	# Wait for the user to input a command
	cmd = input('\nFTP>>> ')

	# Checks for CONNECT
	if 'CONNECT' in cmd:
		# Split the command into a list so we can pass it
		# to the CONNECT handler. Also checks for the valid
		# number of parameters.
		cmdList = cmd.split()
		if len(cmdList) == 3:
			connect(cmdList[1], cmdList[2])
			# Empty the command list for reuse
			cmdList = []
		else:
			# Handle an incorrect number of parameters for CONNECT
			print('CONNECT takes two parameters. IP and port number')
			prompt()

	elif 'SEARCH' in cmd and checkConnection():
		cmdList = cmd.split()
		if len(cmdList) == 2:
			print('hit')
			createLocalDescription(cmdList[1])
			store('update.txt')
			prompt()

	# Handle the LIST command and check the
	# connection to an FTP server
	elif 'LIST' in cmd and checkConnection():
		ftp.retrlines('LIST')
		prompt()

	# Handle the STORE command and check the
	# connection to an FTP server
	elif 'STORE' in cmd and checkConnection():
		# Split the store command into a list
		cmdList = cmd.split()
		# Check for correct number of parameters
		if len(cmdList) == 2:
			# store the file on the FTP server
			store(cmdList[1])
			prompt()
		else:
			# Handle the incorrect number of parameters error
			print('STORE takes one parameter- The file you would like to upload')
			prompt()

	# Handle the RETRIEVE command from the users and checks
	# connection to an FTP server
	elif 'RETRIEVE' in cmd and checkConnection():
		# Split the retrieve command into a list
		cmdList = cmd.split()
		# Check the list length to make sure the
		# command has correct syntax
		if len(cmdList) == 2:
			# Send the file name to retrieve function
			retrieve(cmdList[1])
			prompt()
		else:
			# Handle an incorrectly formatted retrieve command
			print('RETRIEVE takes exactly one parameter- The file you would like to download')
			prompt()

	# Quit the ftp client, if logged into a server
	# Also quit the current FTP session
	elif 'QUIT' in cmd:
		try:
			ftp.quit()
			print('Goodbye')
		except:
			print('Goodbye')

	# If not connected to a server, tell the user to connect to one
	elif not connected:
		print('You aren\'t connected to an FTP server. Please connect first')
		prompt()

	# If a command can't be found, list the coomands for the user
	else:
		print('Valid commands are CONNECT, LIST, RETRIEVE and STORE')
		prompt()


# Start the client
if __name__ == '__main__':
	print('Python FTP Client is up and running, \nPlease use CONNECT to connect to the FTP server')
	# gw = os.popen("ip -4 route show default").read().split()
	# updatefile = open("update.txt","w")
	# updatefile.write(gw[3] + "\n")
	# currentfiles = os.listdir()
	# for i in currentfiles:
	# 	updatefile.write(i + "\n")
	# updatefile.close()
	prompt()
