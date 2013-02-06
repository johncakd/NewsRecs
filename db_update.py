# !/usr/bin/python
# Coding: utf-8

from BeautifulSoup import BeautifulSoup
import urllib
import re, sys
import sqlite3


# DEFS
news_db = "news.db"
news_table = "newsfeed"

def create():
	conn = sqlite3.connect(news_db)
	c = conn.cursor()
	c.execute('''CREATE TABLE if not exists %s
	(title text, body text, date text)''' % (news_table))

def clear():
	conn = sqlite3.connect('news.db')
	c = conn.cursor()
	c.execute("drop table %s" % (news_table))
	create()

def fetch_day():
	html_base = "http://www.google.com.br"
	conn = sqlite3.connect(new_db)
	c = conn.cursor()
	max_pages = 19
	for page_number in range(max_pages+1):
		print 'Processing %d'%page_number
		html_source = html_base+str(page_number)+".html"
		html = urllib.urlopen(html_source+"0.html") 
		soup = BeautifulSoup(html)
		for entry in soup.findAll("tr", {"class": re.compile("forum")}):
			text = []
			for inner in entry.findAll({"td", "a"}):
				text.append(inner.string)
			text[0] = text[0][:-1]
			text[5] = (text[5].replace(" ", ""))
			c.execute("INSERT INTO experience VALUES('%s','%s','%s','%s','%s', datetime('now'))"%(
						text[0], text[2], text[3], text[4], text[5]))
	conn.commit()

def main ():
	create()
	#clear()
	#fetch_day()

if __name__ == '__main__':
	main()

