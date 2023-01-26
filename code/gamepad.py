#!/usr/bin/env python

# Import PyGame library
import pygame
# Import GPIO library
import RPi.GPIO as GPIO
# Import the time library for time functions.
#from time import sleep

NOT_ASSIGNED = -1
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
BTN_START = 4
BTN_MODE_SELECT = 5
BTN_A = 6
BTN_B = 7
BTN_C_L = 8
BTN_X = 9
BTN_Y = 10
BTN_Z_R = 11
BTN_13 = 12
BTN_14 = 13

PAD_3B_CONTROLLER_NAME = "3B controller"

noPad = [ NOT_ASSIGNED, NOT_ASSIGNED, NOT_ASSIGNED, NOT_ASSIGNED, NOT_ASSIGNED, NOT_ASSIGNED, NOT_ASSIGNED, NOT_ASSIGNED, NOT_ASSIGNED, NOT_ASSIGNED, NOT_ASSIGNED, NOT_ASSIGNED, NOT_ASSIGNED, NOT_ASSIGNED ]
# Pad3Bcontroller = [ LEFT, RIGHT, UP, DOWN, BTN_B, BTN_A, NOT_ASSIGNED, NOT_ASSIGNED, BTN_C_L, NOT_ASSIGNED, NOT_ASSIGNED, NOT_ASSIGNED, BTN_START, NOT_ASSIGNED ]
Pad3Bcontroller = { "1" : BTN_B, "2" : BTN_A }

joysticks = {}
connectedPad = {}

# connectedPad = noPad
connectedPad = { "1" : BTN_B, "2" : BTN_A }

def getBtnName(btn):
  if btn == BTN_START:
    return "Start"
  elif btn == BTN_MODE_SELECT:
    return "Mode / Select"
  elif btn == BTN_A:
    return "A"
  elif btn == BTN_B:
    return "B"
  elif btn == BTN_C_L:
    return "C / L"
  elif btn == BTN_X:
    return "X"
  elif btn == BTN_Y:
    return "Y"
  elif btn == BTN_Z_R:
    return "Z / R"
  elif btn == BTN_13:
    return "13"
  elif btn == BTN_14:
    return "14"
  else:
    return "Not assigned"

def pressButton(btn):
  btnValue = connectedPad[btn]
  btnName = getBtnName(btnValue)
  print(f"Joystick button {btnName} pressed.")

def releaseButton(btn):
  btnValue = connectedPad[btn]
  btnName = getBtnName(btnValue)
  print(f"Joystick button {btnName} released.")

def main():
  # Initialize Joystick(s).
  pygame.init()
  # connectedPad = {}
  while True:
    for event in pygame.event.get():
      if event.type == pygame.JOYAXISMOTION:
        print(f"Joystick axis {event.axis} value  {round(event.value)}")

      if event.type == pygame.JOYBUTTONDOWN:
        # pressButton(event.button):
        pressButton(f"{event.button}")
        # print(f"Joystick button {event.button} pressed.")

      if event.type == pygame.JOYBUTTONUP:
        # releaseButton(event.button)
        print(f"Joystick button {event.button} released.")

      # Handle hotplugging
      if event.type == pygame.JOYDEVICEADDED:
          # This event will be generated when the program starts for every
          # joystick, filling up the list without needing to create them manually.
          joy = pygame.joystick.Joystick(event.device_index)
          joysticks[joy.get_instance_id()] = joy
          print(f"Joystick {joy.get_instance_id()} connencted")
          if (joy.get_name() == PAD_3B_CONTROLLER_NAME):
            print(f"{joy.get_name()} connected")
            # connectedPad = Pad3Bcontroller
            connectedPad.update(Pad3Bcontroller)
          else:
            print(f"Unknown gamepad")
            # connectedPad = noPad
            connectedPad.clear()

      if event.type == pygame.JOYDEVICEREMOVED:
        del joysticks[event.instance_id]
        connectedPad = noPad
        print(f"Joystick {event.instance_id} disconnected")

main()
