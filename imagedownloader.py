#!/usr/bin/python3
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import urllib
import http.cookiejar
from html.parser import HTMLParser
import time
import os

url_prefix = 'http://mtgsalvation.gamepedia.com'
url = url_prefix + '/Template:List_of_Magic_sets'
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/45.0.2454.101 Chrome/45.0.2454.101 Safari/537.36'
headers={'User-Agent':user_agent,}
xml_root = ET.Element('root')
elementValuesAsAttributes = False;
project_folder_name = 'project' + str(int(time.time()))


def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
            
def get_response( local_url, opener ):
	request = urllib.request.Request(url_prefix + local_url , None, headers)
	response = None
	try:
		response = opener.open(request)
	except urllib.error.HTTPError as e:
		print(e.code)
		print(e.read()) 
		if(e.code == 302):
			print(e.headers['Location'])
			request = urllib.request.Request(e.headers['Location'] , None, headers)
			response = opener.open(request)
	return response

def parse_page( folder_name, local_url):
	cj = http.cookiejar.CookieJar()
	opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
	#new_request = urllib.request.Request(url_prefix + local_url , None, headers)
	response = None
	while response is None:
		response = get_response(local_url, opener)
	if(response is not None):
		data = response.read();
		target_page = BeautifulSoup(data, 'html.parser')
		image_container = target_page.find("div", {"class" : "fullMedia"})
		if image_container:
			link = image_container.find('a')
			print(link.get('href'))
			download_images(folder_name, link.get('href'), link.get('title'))
		print("Going to sleep for 2 secs")
		time.sleep(2)
	return
	
def download_images( folder_name, image_url, title ):
	urllib.request.urlretrieve(image_url, folder_name + "/" + title)
	
def createElement( element_type, element_value, parent):
	if not elementValuesAsAttributes:
		new_element = ET.SubElement(parent, element_type)
		new_element.text = element_value
		return new_element
	else:
		parent.set(element_type, element_value)
		return None
	
request=urllib.request.Request(url,None,headers) #The assembled request
response = urllib.request.urlopen(request)
data = response.read() # The data u need
soup = BeautifulSoup(data, 'html.parser');
if not os.path.exists(project_folder_name):
	os.makedirs(project_folder_name)
table = soup.find("table", {"class" : "wikitable"})	
for tr in table.find_all('tr'):
	edition_element = ET.Element('edition')
	link = tr.find('a', {"class" : "image"})
	if link is not None:
		print(link.get('href'))
		image_name = project_folder_name + '/' + link.get('href').replace('File:', '')
		createElement('image', image_name, edition_element)
		parse_page(project_folder_name, link.get('href')) 
	name_element = tr.find('i')
	if name_element is not None:
		anchor_name = name_element.find('a')
		if anchor_name is not None:
			print(anchor_name.get('title'))
			createElement('name', anchor_name.get('title'), edition_element)			
		#print(name_element.get('title'))
	print ("---------------")
	xml_root.append(edition_element)
tree = ET.ElementTree(xml_root)
indent(xml_root)
tree.write(project_folder_name + '/magicsymbols.xml')
print ("end")
