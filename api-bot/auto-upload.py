#!/usr/bin/env python
# -*- coding: utf-8 -*-

from InstagramAPI import InstagramAPI

import pickle
import time
import os

if __name__ == '__main__':
    session_filename = "session"

    try:
        api = pickle.load(open(session_filename))
        print "API Loaded from previous session"
    except IOError:
        api = InstagramAPI("leandro.liptak", "crearessanar")
        if not api.login():
            print "Login error."
            quit()
        else:
            pickle.dump(api, open(session_filename, "w"))
            print "API session saved to", session_filename

    while True:
        for photo in os.listdir("uploads"):
            api.uploadPhoto(photo, story=True)
        time.sleep(24 * 60 * 60)