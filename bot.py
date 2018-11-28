#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import sys

from src import InstaBot
from src.check_status import check_status
from src.feed_scanner import feed_scanner
from src.follow_protocol import follow_protocol
from src.unfollow_protocol import unfollow_protocol

username = sys.argv[1]
password = sys.argv[2]

tagfile = open("taglist")
taglist = filter(lambda tag: tag and tag[0] != '#', tagfile.read().split("\n"))
tagfile.close()

bot = InstaBot(username, password, tag_list=taglist, log_mod=1)
bot.lean_mod()