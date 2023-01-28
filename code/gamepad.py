#!/usr/bin/env python

# Import PyGame library
import pygame
import adapter
import Pad3Bcontroller
from actions import *

controllers = { Pad3Bcontroller, }

pad = {}

joysticks = {}

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

def getAxisAction(value):
  if value == LEFT:
    return "Press left\nRelease right"
  elif value == RIGHT:
    return "Release left\nPress right"
  elif value == RELEASE_H:
    return "Release left\nRelease right"
  elif value == UP:
    return "Press up\nRelease down"
  elif value == DOWN:
    return "Release up\nPress down"
  elif value == RELEASE_V:
    return "Release up\nRelease down"
  else:
    return f"Not assigned {value}"

def pressButton(btn):
  try:
    btnValue = pad[btn]
    btnName = getBtnName(btnValue)
    print(f"Joystick button {btnName} pressed.")
    adapter.pressButton(btnValue)
  except KeyError:
    print(f"Not managed key {btn}")

def releaseButton(btn):
  try:
    btnValue = pad[btn]
    btnName = getBtnName(btnValue)
    print(f"Joystick button {btnName} released.")
    adapter.releaseButton(btnValue)
  except KeyError:
    print(f"Not managed key {btn}")

def manageAxis(axis, value):
  value = f"{axis}_{value}"
  try:
    btnValue = pad[value]
    action = getAxisAction(btnValue)
    print(f"{action}")
    adapter.performAction(btnValue)
  except KeyError:
    print(f"Not managed axis {value}")

def main():
  print("!!!!!!!!!!!!!! START !!!!!!!!!!!!!!")

  adapter.init()
  currentAdapter = adapter.currentAdapter

  # Initialize Joystick(s).
  pygame.init()

  while True:
    for event in pygame.event.get():
      if event.type == pygame.JOYAXISMOTION:
        manageAxis(event.axis, round(event.value))

      if event.type == pygame.JOYBUTTONDOWN:
        pressButton(f"{event.button}")

      if event.type == pygame.JOYBUTTONUP:
        releaseButton(f"{event.button}")

      # Handle hotplugging
      if event.type == pygame.JOYDEVICEADDED:
          # This event will be generated when the program starts for every
          # joystick, filling up the list without needing to create them manually.
          joy = pygame.joystick.Joystick(event.device_index)
          joysticks[joy.get_instance_id()] = joy
          print(f"Joystick {joy.get_instance_id()} connected")
          for controller in controllers:
            if controller.name == joy.get_name():
              print(f"{joy.get_name()} connected")
              pad.update(controller.sega_md)

      if event.type == pygame.JOYDEVICEREMOVED:
        del joysticks[event.instance_id]
        pad.clear()
        print(f"Joystick {event.instance_id} disconnected")

    pluggedAdapter = adapter.currentAdapter
    if pluggedAdapter != currentAdapter:
      currentAdapter = pluggedAdapter
      print(f"Adapter status changed: {currentAdapter}")

main()
