#!/usr/bin/env python

# Import PyGame library
import pygame
# Import GPIO library
import RPi.GPIO as GPIO
# Import the time library for time functions.
#from time import sleep

joysticks = {}

def main():
  # Initialize Joystick(s).
  pygame.init()
  while True:
    for event in pygame.event.get():
      if event.type == pygame.JOYAXISMOTION:
        print(f"Joystick axis {event.axis} value  {round(event.value)}")

      if event.type == pygame.JOYBUTTONDOWN:
        print(f"Joystick button {event.button} pressed.")

      if event.type == pygame.JOYBUTTONUP:
        print(f"Joystick button {event.button} released.")

      # Handle hotplugging
      if event.type == pygame.JOYDEVICEADDED:
          # This event will be generated when the program starts for every
          # joystick, filling up the list without needing to create them manually.
          joy = pygame.joystick.Joystick(event.device_index)
          joysticks[joy.get_instance_id()] = joy
          print(f"Joystick {joy.get_instance_id()} connencted")
          print(f"Joystick name: {joy.get_name()}")

      if event.type == pygame.JOYDEVICEREMOVED:
        del joysticks[event.instance_id]
        print(f"Joystick {event.instance_id} disconnected")

main()
