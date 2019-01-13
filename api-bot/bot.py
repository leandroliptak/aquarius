#!/usr/bin/env python
# -*- coding: utf-8 -*-

# leandro.liptak id 4017599252

from InstagramAPI import InstagramAPI
import gender_guesser.detector as gender
import time
import re
import emoji
import pickle

import sqlite3
import unicodedata
from datetime import datetime, timedelta
import random

from sql_updates import check_and_update, check_already_liked
from sql_updates import check_already_followed, check_already_unfollowed
from sql_updates import insert_media, insert_username, insert_unfollow_count
from sql_updates import get_usernames_first, get_usernames
from sql_updates import get_username_random, get_username_to_unfollow_random
from sql_updates import check_and_insert_user_agent

str_message = "Hola %s! Como estas?\n\nTe escribimos porque creemos que puede interesarte la astrologia, como herramienta de autoconocimiento y autodescubrimiento de las potencialidades de cada ser humano. Por ese motivo, te contamos que desde Venus Saturno estaremos dictando tres cursos en verano, dos introductorios y un tercero mas avanzado. Los cursos se dictan presenciales en Belgrano (CABA, Arg.) pero tambien existe modalidad online para el mas inicial.\n\nTodos los cursos son dictados por Leandro Liptak, astrologo y autor del libro Curso de Astrologia Espiritual.\n\nEsperamos no molestar con este mensaje, y de ser asi te pedimos disculpas. En caso quieras mas informacion te invitamos a revisar nuestro perfil, y podes dejarnos un e-mail para enterarte de las novedades. Los cursos comienzan en Enero y duran todos 3 meses.\n\nSaludos,\nEquipo de Venus Saturno"

class Bot:
    def __init__(self):
		database_name='follows_db.db'
		self.database_name = database_name
		self.follows_db = sqlite3.connect(database_name, timeout=0, isolation_level=None)
		self.follows_db_c = self.follows_db.cursor()
		check_and_update(self)

		self.follow_time = 5 * 60 * 60

def get_name_and_gender(user):
	names = name_cleanup(user["full_name"]).split()

	first_name = ""
	gender = "unknown"

	if names:
		first_name = remove_accents(names[0])
		gender = gender_detector.get_gender(first_name)
	return first_name, gender

def name_cleanup(name):
	name = emoji.demojize(name)
	name = re.sub(":[^:]*:", "", name)
	return name

def unfollow_anyone(bot):
    username_row = get_username_to_unfollow_random(bot)
    if not username_row:
        return False

    current_id = username_row[0]

    if api.unfollow(int(current_id)):
    	insert_unfollow_count(bot, user_id=current_id)
    	print "    Unfollow OK", current_id
    else:
    	print "    Unfollow Return code", api.LastResponse

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii
######

last_dm_time = datetime.now() - timedelta(hours=2)

b = Bot()
session_filename = "session"

try:
	api = pickle.load(open(session_filename))
	print "API Loaded from previous session"
except IOError:
	api = InstagramAPI("astro.venus.saturno", "vivaelverano")
	if not api.login():
		print "Login error."
		quit()
	else:
		pickle.dump(api, open(session_filename, "w"))
		print "API session saved to", session_filename

gender_detector = gender.Detector()

reference_account = "the.weatherman" #"astro_logiando" #"lu.gaitan"

api.searchUsername(reference_account)
userid = api.LastJson["user"]["pk"]

maxid = ""
while api.getUserFollowers(userid, maxid):
	users = api.LastJson["users"]
	print "Fetched", len(users), "users."
	maxid = api.LastJson["next_max_id"]

	for user in users:
		u_id = user["pk"]
		u_name = user["username"]

		name, g = get_name_and_gender(user)
		print "  ", u_id, u_name, name, g

		resume_dm = (datetime.now() - last_dm_time) > timedelta(hours=1)

		if not check_already_followed(b, str(u_id)):
			print "    Following."
			if api.follow(u_id):
				print "    Follow OK"
				insert_username(b, str(u_id), u_name)
				time.sleep(30 + random.randint(0,30))
			else:
				time.sleep(10 * 60)

			if resume_dm and g == "female":
				print "    Sending DM"
				if api.direct_message(str_message % name, [u_id]):
					print "    DM", api.LastResponse
					time.sleep(30 + random.randint(0,30))
				else:
					last_dm_time = datetime.now()

			unfollow_anyone(b)
			time.sleep(30 + random.randint(0,30))

	time.sleep(5)