#!/usr/bin/env python

import threading
import RPi.GPIO as GPIO
from time import sleep
from actions import *

NOT_INITIALIZED = -1
NOT_CONNECTED = 0b000
MEGADRIVE = 0b001
SUPER_NES = 0b010
SATURN = 0b011

IO_UP = 3
IO_DOWN = 5
IO_LEFT = 7
IO_RIGHT = 8
IO_BTN_START = 10
IO_BTN_MODE_SELECT = 11
IO_BTN_A = 12
IO_BTN_B = 13
IO_BTN_C_L = 15
IO_BTN_X = 16
IO_BTN_Y = 18
IO_BTN_Z_R = 19
IO_BTN_13 = 26
IO_BTN_14 = 29

run = False
currentAdapter = NOT_INITIALIZED
t1 = threading.Thread()

def initGpio():
  GPIO.setup(IO_UP, GPIO.OUT, initial=GPIO.LOW)
  GPIO.setup(IO_DOWN, GPIO.OUT, initial=GPIO.LOW)
  GPIO.setup(IO_LEFT, GPIO.OUT, initial=GPIO.LOW)
  GPIO.setup(IO_RIGHT, GPIO.OUT, initial=GPIO.LOW)
  GPIO.setup(IO_BTN_START, GPIO.OUT, initial=GPIO.LOW)
  GPIO.setup(IO_BTN_MODE_SELECT, GPIO.OUT, initial=GPIO.LOW)
  GPIO.setup(IO_BTN_A, GPIO.OUT, initial=GPIO.LOW)
  GPIO.setup(IO_BTN_B, GPIO.OUT, initial=GPIO.LOW)
  GPIO.setup(IO_BTN_C_L, GPIO.OUT, initial=GPIO.LOW)
  GPIO.setup(IO_BTN_X, GPIO.OUT, initial=GPIO.LOW)
  GPIO.setup(IO_BTN_Y, GPIO.OUT, initial=GPIO.LOW)
  GPIO.setup(IO_BTN_Z_R, GPIO.OUT, initial=GPIO.LOW)
  GPIO.setup(IO_BTN_13, GPIO.OUT, initial=GPIO.LOW)
  GPIO.setup(IO_BTN_14, GPIO.OUT, initial=GPIO.LOW)

def getBtnGpio(btn):
  if btn == BTN_START:
    return IO_BTN_START
  elif btn == BTN_MODE_SELECT:
    return IO_BTN_MODE_SELECT
  elif btn == BTN_A:
    return IO_BTN_A
  elif btn == BTN_B:
    return IO_BTN_B
  elif btn == BTN_C_L:
    return IO_BTN_C_L
  elif btn == BTN_X:
    return IO_BTN_X
  elif btn == BTN_Y:
    return IO_BTN_Y
  elif btn == BTN_Z_R:
    return IO_BTN_Z_R
  else:
    return -1

def pressButton(btn):
  btnIo = getBtnGpio(btn)
  if btnIo > 0:
    GPIO.output(btnIo, GPIO.HIGH)

def releaseButton(btn):
  btnIo = getBtnGpio(btn)
  if btnIo > 0:
    GPIO.output(btnIo, GPIO.LOW)

def performAction(value):
  if value == LEFT:
      GPIO.output(IO_LEFT, GPIO.HIGH)
      GPIO.output(IO_RIGHT, GPIO.LOW)
  elif value == RIGHT:
      GPIO.output(IO_LEFT, GPIO.LOW)
      GPIO.output(IO_RIGHT, GPIO.HIGH)
  elif value == RELEASE_H:
      GPIO.output(IO_LEFT, GPIO.LOW)
      GPIO.output(IO_RIGHT, GPIO.LOW)
  elif value == UP:
      GPIO.output(IO_UP, GPIO.HIGH)
      GPIO.output(IO_DOWN, GPIO.LOW)
  elif value == DOWN:
      GPIO.output(IO_UP, GPIO.LOW)
      GPIO.output(IO_DOWN, GPIO.HIGH)
  elif value == RELEASE_V:
      GPIO.output(IO_UP, GPIO.LOW)
      GPIO.output(IO_DOWN, GPIO.LOW)

def readPadAdapter():
  GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  d1 = 0
  d2 = 0
  d3 = 0
  if GPIO.input(21):
    d1 = 1
  if GPIO.input(22):
    d2 = 1
  if GPIO.input(23):
    d3 = 1
  value = (d3 << 2) | (d2 << 1) | d1
  return value

def main():
  global run, currentAdapter
  while run:
    adapter = readPadAdapter()
    if (adapter != currentAdapter):
      currentAdapter = adapter
    sleep(0.5)

def stop():
  global run, t1, currentAdapter
  run = False
  t1.join()
  currentAdapter = NOT_INITIALIZED

def init():
  global run, t1
  GPIO.setmode(GPIO.BOARD )
  initGpio()
  t1 = threading.Thread(target=main, daemon=True)
  run = True
  t1.start()

def getAdapter():
  global currentAdapter
  return currentAdapter
