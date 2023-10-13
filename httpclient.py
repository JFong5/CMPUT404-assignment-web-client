#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        #Get each line of the data and split it into a list
        dataLines = data.split("\r\n")
        #Get the httpCode 
        httpCode = (dataLines[0].split()[1])
        #print(httpCode)
        return int(httpCode)

    def get_headers(self,data):
        #Get header
        dataLines = data.split('\r\n\r\n')
        header = dataLines[0]
        #print(header)
        return header

    def get_body(self, data):
        #Get the body content
        body = data.split("\r\n\r\n")[1]
        #print(body)
        return body
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        '''
        Get Funciton
        '''
        code = 500
        body = ""
        
        #Get the host, port and path
        parsedUrl = urllib.parse.urlparse(url)
        host = parsedUrl.hostname
        port = parsedUrl.port
        path = parsedUrl.path
        
        #In the even where there is no host
        if host == None:
            host = url
        #In the event port is None, set it as 80
        if port == None:
            port = 80
        #In the event path is ""
        if path == "":
            path = "/"
        
        #Connect to host and port and sendall request data 
        self.connect(host, port)
        #request = "GET" + " " + path + " " +"HTTP/1.1\r\n" + "Host:" + " " + host + "\r\n" + "Connection: close\r\n\r\n" #This is the brute force method
        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        self.sendall(request)

        #Get the response data and close the socket
        response = self.recvall(self.socket)
        print(response)
        self.close()

        #Get the http code and the body content
        code = self.get_code(response)
        body = self.get_body(response)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        """
        Post Function
        """
        code = 500
        body = ""
        
        #Get the host, port and path
        parsedUrl = urllib.parse.urlparse(url)
        host = parsedUrl.hostname
        port = parsedUrl.port
        path = parsedUrl.path 

        #In the even where there is no host
        if host == None:
            host = url
        #In the event port is None, set it as 80
        if port == None:
            port = 80
        #In the event path is ""
        if path == "":
            path = "/"
        
        #Connect to host and port and Sendall data
        self.connect(host,port)
        postContent = "" #Get the Post Content
        if args is None:
            postContent = ""
        else:
            postContent = urllib.parse.urlencode(args)
        #request = "POST" + " " + path + " " + "HTTP/1.1\r\n" + "Host: " + host + "\r\n" + "Content-Type: application/x-www-form-urlencoded\r\n" + "Content-Length:" + " " + str(len(postContent)) + "\r\n" + "Connection: close\r\n\r\n" + postContent #This is the brute force method
        request = f"POST {path} HTTP/1.1\r\nHost: {host}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {len(postContent)}\r\nConnection: close\r\n\r\n" + postContent
        self.sendall(request)

        #Get the response data and close the socket
        response = self.recvall(self.socket)
        self.close()

        #Get the http code and the body content
        code = self.get_code(response)
        body = self.get_body(response)
        
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
