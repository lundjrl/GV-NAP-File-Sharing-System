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

'''
The main loop that starts the server
'''

def MyHandler(FTPHandler):
    def on_file_received(self, file):
        print('File received')

def main():
    authorizer = DummyAuthorizer()
    authorizer.add_anonymous('.', perm='elradfmwM')

    handler = MyHandler
    handler.authorizer = authorizer

    gw = os.popen("ip -4 route show default").read().split()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((gw[3],0))
    ipaddr = s.getsockname()[0]
    server = ThreadedFTPServer((ipaddr, 1030), handler)
    server.serve_forever()

'''
Runs the main loop
'''
if __name__ == "__main__":
    main()
