#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import time
import socket
import random

ippPattern = re.compile(r'(?<="ipp":\s)\d+')
totalPattern = re.compile(r'(?<="total":\s)\d+')
wordPattern = re.compile(r'(?<="content": ")\S+(?=")')
pagePattern = re.compile(r'(?<=page=)\d+')
timestampPattern = re.compile(r'(?<=_=)\d+')
request_template = 'request.txt'

def CountTotalPage(json):
	ipp = int(ippPattern.findall(json)[0])
	total = int(totalPattern.findall(json)[0])
	c = total // ipp if total % ipp == 0 else total // ipp + 1
	return c

def FetchWordList(json):
	wl = wordPattern.findall(json)
	return wl

def HttpRequestJson(request):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('www.shanbay.com', 80))
	s.sendall(request)
	json = ''
	while 1:
		response = s.recv(4096)
		if not response:
			break
		json += response
	s.close()
	return json

def ReadRequestTemplate(filename):
	with open(filename, 'rb') as f:
		request = f.read()
	requestTemplate = pagePattern.sub('{page}', request)
	requestTemplate = timestampPattern.sub('{timestamp}', requestTemplate)
	return requestTemplate

def main():
	page = 1
	rt = ReadRequestTemplate(request_template) # request(txt) captured by burp suite etc.
	while 1:
		r = rt.format(page = page, timestamp = int(time.time()))
		json = HttpRequestJson(r)
		l = FetchWordList(json)
		print page, l
		with open('wordlist.txt', 'a') as f:
			for w in l:
				f.write(w)
				f.write('\n')
		totalpage = CountTotalPage(json)
		if page < totalpage:
			page += 1
			# sleep for a random time span
			sleeptime = random.uniform(0.5, 2)
			time.sleep(sleeptime)
		else:
			break
	print 'done.'


if '__main__' == __name__:
	main()
