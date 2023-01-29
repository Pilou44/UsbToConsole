#!/usr/bin/env python

# Import PyGame library
import pygame
import adapter
import MD3Buttons
import RetroflagSnes
import ArduinoMicro
from actions import *

import logger

controllers = { MD3Buttons, RetroflagSnes, ArduinoMicro, }

pad = {}
joysticks = {}

currentGuid = ""
currentAdapter = -1

def pressButton(btn):
  try:
    logger.debug(f"Button {btn} pressed.")
    btnValue = pad[btn]
    adapter.pressButton(btnValue)
  except KeyError:
    logger.debug("Button not managed")

def releaseButton(btn):
  try:
    logger.debug(f"Button {btn} released.")
    btnValue = pad[btn]
    adapter.releaseButton(btnValue)
  except KeyError:
    logger.debug("Button not managed")

def manageAxis(axis, value):
  logger.debug(f"Axis change: axis: {axis} value: {value}")
  axisValue = f"{axis}_{value}"
  try:
    btnValue = pad[axisValue]
    adapter.performAction(btnValue)
  except KeyError:
    logger.debug("Axis not managed.")

def manageHat(hat, value):
  logger.debug(f"Hat change: hat: {hat} value: {value}")
  try:
    first = value[0]
    second = value[1]

    fisrtHatValue = f"{hat}_1_{first}"
    secondHatValue = f"{hat}_2_{second}"

    btnValue = pad[fisrtHatValue]
    adapter.performAction(btnValue)

    btnValue = pad[secondHatValue]
    adapter.performAction(btnValue)
  except KeyError:
    logger.debug("Hat not managed.")

def checkConnections():
  global currentAdapter
  global currentGuid
  foundGuid = False
  if currentAdapter == adapter.NOT_INITIALIZED:
    logger.info(f"Adapter not initialized")
    pad.clear()
  elif currentAdapter == adapter.NOT_CONNECTED:
    logger.info(f"No adapter connected")
    pad.clear()
  elif currentGuid == "":
    logger.info(f"No controller connected")
    pad.clear()
  else:
    for controller in controllers:
      if controller.guid == currentGuid:
        foundGuid = True
        logger.info(f"{controller.name} connected")
        mapController(controller)
    if foundGuid == False:
      logger.info(f"Unknown controller")
      pad.clear()

def mapController(controller): # Add try / catch if adapter not defined for controller
  pad.clear()
  try:
    if currentAdapter == adapter.MEGADRIVE:
      logger.info(f"Map for Sega Megadrive")
      pad.update(controller.sega_md)
    elif currentAdapter == adapter.SUPER_NES:
      logger.info(f"Map for Super Nintendo")
      pad.update(controller.snes)
    elif currentAdapter == adapter.SATURN:
      logger.info(f"Map for Sega Saturn")
      pad.update(controller.saturn)
    else:
      logger.info(f"Unknown adapter")
  except AttributeError:
    logger.warning(f"Controller not usable with this adapter")

def main():
  global currentAdapter
  global currentGuid
  logger.info("!!!!!!!!!!!!!! START !!!!!!!!!!!!!!")

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
          logger.debug(f"Joystick {joy.get_instance_id()} connected\nname: {name}, id: {joy.get_id()}, guid: {joy.get_guid()}\naxes: {joy.get_numaxes()}, buttons: {joy.get_numbuttons()}, balls: {joy.get_numballs()}, hats: {joy.get_numhats()}")
          currentGuid = joy.get_guid()
          checkConnections()

      if event.type == pygame.JOYDEVICEREMOVED:
        del joysticks[event.instance_id]
        logger.debug(f"Joystick {event.instance_id} disconnected")
        currentGuid = ""
        checkConnections()

    pluggedAdapter = adapter.currentAdapter
    if pluggedAdapter != currentAdapter:
      logger.debug(f"Adapter status changed: {pluggedAdapter}")
      currentAdapter = pluggedAdapter
      checkConnections()

main()
