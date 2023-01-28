#!/usr/bin/env python

import threading
import RPi.GPIO as GPIO
from time import sleep

NOT_INITIALIZED = -1
NOT_CONNECTED = 0b000
MEGADRIVE = 0b001
SUPER_NES = 0b010
SATURN = 0b011

run = False
currentAdapter = NOT_INITIALIZED
t1 = threading.Thread(target=pass)

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

def readPadAdapter():
  GPIO.setup(21, GPIO.IN)
  GPIO.setup(22, GPIO.IN)
  GPIO.setup(23, GPIO.IN)
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

def notifyNewAdapter(adapter):
  print(f"Adapter = {bin(adapter)}")

def main():
  while run:
    adapter = readPadAdapter
    if (adapter != currentAdapter):
      currentAdapter = adapter
      notifyNewAdapter(adapter)
    sleep(0.5)

def stop():
  print("Stop thread")
  run = False
  t1.join()
  currentAdapter = NOT_INITIALIZED

def init():
  GPIO.setmode(GPIO.BOARD )
  initGpio()
  t1 = threading.Thread(target=main, args=())
  print("Start thread")
  t1.start()

def getAdapter():
  return currentAdapter
