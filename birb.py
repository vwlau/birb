#!/usr/bin/python3

'''
to enter virtual environgment and run, in ~/birb/, type:
source venv/bin/activate
to exit virtual environement, type:
deactivate
'''

import os
import feedparser
import sqlite3
import json
from pushbullet import Pushbullet

dn = os.path.dirname(os.path.realpath(__file__))
db_file = os.path.join(dn, 'mechmarket.sqlite')
json_file = os.path.join(dn, 'search_terms.json')

#connects to sqlite database
db_connection = sqlite3.connect(db_file)
cur = db_connection.cursor()
#creates the database and table if it doesn't already exist
cur.execute('CREATE TABLE IF NOT EXISTS posts (title TEXT, id TEXT)')

#checks to see if post is already in database
def post_not_in_db(post_title, post_id):
	cur.execute('SELECT * from posts WHERE title=? AND id=?', (post_title, post_id))
	if not cur.fetchall():
		return True
	else:
		return False

#adds a post to the sqlite database
def add_post_to_db(post_title, post_id):
	cur.execute('INSERT INTO posts VALUES (?,?)', (post_title, post_id))
	db_connection.commit()

#sends pushbullet a notification
def send_pb_note(title, msg):
	ACCESS_TOKEN = 'YOUR ACCESS TOKEN HERE'

	pb = Pushbullet(ACCESS_TOKEN)
	push = pb.push_note(title, msg)

#depreciated in favor of storing in a json file
'''def get_search_terms(file):
	f = open(file, 'r')
	search_terms = f.readlines()
	search_terms = [terms.rstrip() for terms in search_terms] #remove the '\n' char
	f.close()
	return search_terms'''

#retrieves all keywords to search for from file and returns a list of search terms to use
def load_json(json_file):
	with open(json_file, "r") as read_file:
		data = json.load(read_file)
		return data['terms']

#returns true if search term is in search text, false if not
def contains_search_term(search_term, search_text):
	return search_term in search_text.lower()

#returns true if multiple search terms are all in search text, false if not
def contains_multi_subterms(search_list, search_text):
	for sub_term in search_list:
		if sub_term not in search_text.lower():
			return False
	else:
		return True

def main():
	#get the rss feed
	feed = feedparser.parse("https://www.reddit.com/r/mechmarket/new/.rss")

	#get the search terms
	search_terms = load_json(json_file)

	#iterate through all the posts 
	for post in feed.entries:
		if post_not_in_db(post['title'], post['id']):
			#print(post['title']) for debugging
			add_post_to_db(post['title'], post['id'])
			for term in search_terms:
				if(len(term.split())>1): #if search term is more than one word
					if contains_multi_subterms(term.split(), post['summary']):
						send_pb_note(term, post['link'])
				elif contains_search_term(term, post['summary']):
					send_pb_note(term, post['link'])

if __name__ == '__main__':
	main()
	db_connection.close()
