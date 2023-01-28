#!/usr/bin/env python

# Import PyGame library
import pygame
import adapter
import MD3Buttons
import RetroflagSnes
from actions import *

controllers = { MD3Buttons, RetroflagSnes, }

pad = {}
joysticks = {}

currentGuid = ""
currentAdapter = -1

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
  axisValue = f"{axis}_{value}"
  try:
    btnValue = pad[axisValue]
    action = getAxisAction(btnValue)
    print(f"{action}")
    adapter.performAction(btnValue)
  except KeyError:
    print(f"Not managed axis {axisValue}")

def manageHat(hat, value):
  try:
    first = value[0]
    second = value[1]

    fisrtHatValue = f"{hat}_1_{first}"
    secondHatValue = f"{hat}_2_{second}"

    btnValue = pad[fisrtHatValue]
    action = getAxisAction(btnValue)
    print(f"{action}")
    adapter.performAction(btnValue)

    btnValue = pad[secondHatValue]
    action = getAxisAction(btnValue)
    print(f"{action}")
    adapter.performAction(btnValue)
  except KeyError:
    print(f"Not managed hat {value}")

def checkConnections():
  global currentAdapter
  global currentGuid
  foundGuid = False
  if currentAdapter == NOT_INITIALIZED:
    print(f"Adapter not initialized")
    pad.clear()
  elif currentAdapter == NOT_CONNECTED:
    print(f"No adapter connected")
    pad.clear()
  elif currentGuid == "":
    print(f"No controller connected")
    pad.clear()
  else
    for controller in controllers:
      if controller.guid == currentGuid:
        foundGuid = True
        print(f"{controller.name} connected")
        mapController(controller)
    if !foundGuid:
      print(f"Unknown controller")
      pad.clear()

def mapController(controller): # Add try / catch if adapter not defined for controller
  pad.clear()
  if currentAdapter == adapter.MEGADRIVE:
    print(f"Map for Sega Megadrive")
    pad.update(controller.sega_md)
  elif currentAdapter == adapter.SUPER_NES:
    print(f"Map for Super Nintendo")
    pad.update(controller.snes)
  elif currentAdapter == adapter.SATURN:
    print(f"Map for Sega Saturn")
    pad.update(controller.saturn)
  else:
    print(f"Unknown adapter")

def main():
  global currentAdapter
  global currentGuid
  print("!!!!!!!!!!!!!! START !!!!!!!!!!!!!!")

  adapter.init()
  currentAdapter = adapter.currentAdapter

  # Initialize Joystick(s).
  pygame.init()

  while True:
    for event in pygame.event.get():
      if event.type == pygame.JOYHATMOTION:
        manageHat(event.hat, event.value)

      if event.type == pygame.JOYAXISMOTION:
        manageAxis(event.axis, round(event.value))

      if event.type == pygame.JOYBUTTONDOWN:
        pressButton(f"{event.button}")

      if event.type == pygame.JOYBUTTONUP:
        releaseButton(f"{event.button}")

      if event.type == pygame.JOYDEVICEADDED:
          joy = pygame.joystick.Joystick(event.device_index)
          joysticks[joy.get_instance_id()] = joy
          name = joy.get_name()
          print(f"Joystick {joy.get_instance_id()} connected\nname: {name}, id: {joy.get_id()}, guid: {joy.get_guid()}\naxes: {joy.get_numaxes()}, buttons: {joy.get_numbuttons()}, balls: {joy.get_numballs()}, hats: {joy.get_numhats()}")
          currentGuid = joy.get_guid()
          checkConnections()

      if event.type == pygame.JOYDEVICEREMOVED:
        del joysticks[event.instance_id]
        print(f"Joystick {event.instance_id} disconnected")
        currentGuid = ""
        checkConnections()

    pluggedAdapter = adapter.currentAdapter
    if pluggedAdapter != currentAdapter:
      print(f"Adapter status changed: {currentAdapter}")
      currentAdapter = pluggedAdapter
      checkConnections()

main()
