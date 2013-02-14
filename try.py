# !/usr/bin/python
# Coding: utf-8


from BeautifulSoup import BeautifulSoup
import urllib, urllib2
import re, sys
import sqlite3


# DEFS
news_db = "ia_trab.db"
news_table = "main"

def create():
	conn = sqlite3.connect(news_db)
	c = conn.cursor()
	c.execute('''CREATE TABLE if not exists %s
	(url text, title text, body text)''' % (news_table))

def clear():
	conn = sqlite3.connect('news.db')
	c = conn.cursor()
	c.execute("drop table %s" % (news_table))
	create()

def crawl_runtime():
	html_base = "http://www.run-time.com.br/noticias/pagina/"
	conn = sqlite3.connect(news_db)
	c = conn.cursor()
	alreadySeen = set()


	for counter in range(1,7):
		html = html_base + str(counter) + '/' 
		request = urllib2.Request(html)
		fd = urllib2.urlopen(request)
		content = fd.read()
		soup = BeautifulSoup(content)
		for link in soup.findAll(href = re.compile("noticia/")):
			alreadySeen.add(link.get('href'))


	for i in alreadySeen: print i


def inovacao():

	j = 1
	conn = sqlite3.connect(news_db)
	c = conn.cursor()


	html_base = "http://www.inovacaotecnologica.com.br/noticias/assuntos.php?assunto="
	titles = ["eletronica", "energia", "espaco", "informatica", "materiais", "mecanica", "meioambiente", "nanotecnologia", "robotica"]
	alreadySeen = set()
	

#finding all links	
	for subject in titles:
		for counter in range(0,21):
			html = html_base + subject + "&base=" + str(counter*15)
			request = urllib2.Request(html)
			fd = urllib2.urlopen(request)
			content = fd.read()
			soup = BeautifulSoup(content)
			for link in soup.findAll(href = re.compile("noticias/noticia.php")):
				alreadySeen.add(link.get('href'))


#extracting the text from links and connecting to db				
	for link in alreadySeen:
		body = ""
		html = "http://www.inovacaotecnologica.com.br" + link[2:]
		request = urllib2.Request(html)
		fd = urllib2.urlopen(request)
		content = fd.read()
		soup = BeautifulSoup(content.decode('utf-8','ignore')) #para site em ISO
		title = soup.title.string
		if title is None: 
			title = ' '.join([str(x) for x in soup.title])
	
		for tag in soup.findAll(id="colCenN"):
			for x in tag.findAll("p"):
				body += " " + x.text
		j += 1
		print j
		print html
		html = html.replace("'", " ")
		title = title.replace("'", " ")
		body = body.replace("'", " ")
		c.execute("insert into main values('%s', '%s', '%s')" % (html, title, body))			
		conn.commit()



def main ():

	create()

	inovacao()
	#clear()

if __name__ == '__main__':
	main()

