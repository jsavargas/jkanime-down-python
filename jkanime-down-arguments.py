#!/usr/bin/env python
# -*- coding: utf-8 -*-

####### jsvargas
####### MODO DE USO
####### jkanime-down-arguments.py -s dragon-ball-super -i 10



from bs4 import BeautifulSoup
import requests
import urllib
import httplib
import json
import sys

import urllib2
import re

import json
from pprint import pprint

import datetime

import os
import argparse



parser = argparse.ArgumentParser()
parser.add_argument('-s','--serie', nargs='?', default=None,help='sum the integers (default: find the max)')
parser.add_argument('-c','--capitulo', nargs='?', default=None)
parser.add_argument('-i','--inicio', nargs='?', default=None)
parser.add_argument('-f','--final', nargs='?', default=None)
args = parser.parse_args()
#print(args)
#print args.example

var_serie  = args.serie
var_cap    = args.capitulo
var_inicio = args.inicio
var_final  = args.final


if(var_serie):
	print "SERIE: ",var_serie
else:
	exit()

if(var_cap or var_inicio):
	var_cap = (var_cap if var_cap else var_inicio)
	print "INICIO: ",var_cap	
else:
	exit()

if(var_final):
	print "FINAL: ",var_final
else:
	print "FINAL: ",var_inicio
	var_final = var_inicio
	
def getsource(url):
	user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
	headers = { 'User-Agent' : user_agent }

	req = urllib2.Request(url, None, headers)
	response = urllib2.urlopen(req)
	page = response.read()
	response.close() # its always safe to close an open connection
	
	return page

def getvideolink(page):
	soup = BeautifulSoup(page, 'html.parser')
		
	for param in soup.find_all('param',{'name' : 'flashvars'}):
		#print param['value']		
		matchObj = re.match( r'.*&file=(.*)', param['value'], re.M|re.I)		
		if matchObj:
			#print "matchObj.group() : ", matchObj.group()
			print "matchObj.group(1) : ", matchObj.group(1)
			return matchObj.group(1)

def downloadVideo(link,serie,capitulo):
	capitulo = str(capitulo).zfill(3)		
	varmkdir = "mkdir -p {}".format(serie)
	code = os.system(varmkdir)
	down = "wget --tries=5 " + str(link) + " -O " + str(serie) + "/" + str(serie) + "-" + str(capitulo) + ".mp4"
	print "WGET: ", down
	code = os.system(down)
	print "CODE:", code
	
	return code	
					
					
for num in range(int(var_inicio),(int(var_final) + 1)):  
	print "=============================================================================================="
	print "CAPITULO EN CURSO >>>>>>> ",num


	serie    = var_serie # 'dragon-ball-z'
	capitulo = num
	
	pagina = 'http://jkanime.net/' + serie + "/" + str(capitulo)
	
	print "PAGINA: ",pagina
	
	user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
	user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
	
	
	headers = { 'User-Agent' : user_agent }
	#req = urllib2.Request('http://www.instagram.com/jsavargas', None, headers)
	req = urllib2.Request(pagina, None, headers)
	response = urllib2.urlopen(req)
	page = response.read()
	
	response.close() # its always safe to close an open connection
	
	print "DESCARGANDO INICIANDO EL PROCESO"
	print datetime.datetime.now()
				
	
	
	if page:
		#print page
		#print "=============================================================================================="
		
		soup = BeautifulSoup(page, 'html.parser')
		#print(soup.prettify())
	
		#print "=============================================================================================="
		#print "=============================================================================================="
		#print "=============================================================================================="
	
		links1   = ''
		links2   = ''
		alllinks = []
		
		#for div in soup.find_all('div', class_=re.compile('the_video lgv_')):
		for div in soup.find_all('div', id=re.compile('the_video')):
			for iframe in div.find_all('iframe'):
				print "Found the iframe: ALLLINKS: ", iframe['src']
				alllinks.append(iframe['src'])
		
		for div in soup.find_all('div', {'id': 'the_video-1'}):
			for iframe in div.find_all('iframe'):
				#print iframe
				print "Found the iframe: links1: ", iframe['src']
				links1 = iframe['src']
		
		for div in soup.find_all('div', {'id': 'the_video-2'}):
			for iframe in div.find_all('iframe'):
				#print iframe
				print "Found the iframe: links2: ", iframe['src']
				links2 = iframe['src']
	
		
		print "=============================================================================================="
		#exit()	
		
		#download segunda web
		code = 1
		try:
			page   = getsource(links1)
			videos = getvideolink(page)
			
			if (videos):
				code = downloadVideo(videos,serie,capitulo)
				print "CODE VIDEO DOWNLOAD 1 :",code
		except Exception,e:
			print "ERROR VIDEO DOWNLOAD 1 >>>>>>>>", str(e)

		try:
			if(code != 0 and links2):
				page = getsource(links2)
				videos = getvideolink(page)
				if (videos):
					code = downloadVideo(videos,serie,capitulo)
					print "CODE VIDEO DOWNLOAD 2 :",code
		except Exception,e:
			print "ERROR VIDEO DOWNLOAD 2 >>>>>>>>", str(e)

		code = os.system('pwd')

	exit;
	
