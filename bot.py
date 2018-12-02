#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import sys

from src import InstaBot

username = sys.argv[1]
password = sys.argv[2]

tagfile = open("taglist")
taglist = filter(lambda tag: tag and tag[0] != '#', tagfile.read().split("\n"))
tagfile.close()

bot = InstaBot(username, password, tag_list=taglist, log_mod=1)

if len(sys.argv) > 3:
	userlist = sys.argv[3]
	bot.follow_from_growbot_whitelist(userlist)
else:
	bot.lean_mod()