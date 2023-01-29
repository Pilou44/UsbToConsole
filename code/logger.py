#!/usr/bin/env python

import sys
import logging
logging.basicConfig(filename='/home/wechantloup/gamepad/gamepad.log', encoding='utf-8', level=logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)

def excepthook(exc_type, exc_value, exc_traceback):
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    # call the default excepthook
    sys.__excepthook__(type_, value, traceback)

sys.excepthook = excepthook

def debug(txt):
  logging.debug(txt)

def info(txt):
  logging.info(txt)

def wranin(txt):
  logging.wranin(txt)

def error(txt):
  logging.error(txt)

def error(txt, exc_info):
  logging.error(txt, exc_info)
