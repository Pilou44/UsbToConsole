#!/usr/bin/env python

# Import PyGame library
import pygame
# Import GPIO library
import RPi.GPIO as GPIO
# Import the time library for time functions.
#from time import sleep

# Initialize Joystick(s).
pygame.init()
# pygame.joystick.init()

joysticks = {}

while True:
  for event in pygame.event.get():
    if event.type == pygame.JOYAXISMOTION:
      print("Joystick axis ", event.axis, " value  ", round(event.value))

    if event.type == pygame.JOYBUTTONDOWN:
      print("Joystick button ", event.button, " pressed.")

    if event.type == pygame.JOYBUTTONUP:
      print("Joystick button ", event.button, " released.")

    # Handle hotplugging
    if event.type == pygame.JOYDEVICEADDED:
        # This event will be generated when the program starts for every
        # joystick, filling up the list without needing to create them manually.
        joy = pygame.joystick.Joystick(event.device_index)
        joysticks[joy.get_instance_id()] = joy
        print(f"Joystick {joy.get_instance_id()} connencted")

    if event.type == pygame.JOYDEVICEREMOVED:
      del joysticks[event.instance_id]
      print(f"Joystick {event.instance_id} disconnected")
  # pygame.joystick.init()
  # joystickCount = pygame.joystick.get_count()

  # if joystickCount == 0:
  #   # No joystick or controller found.
  #   print("No joystick or controller found.")
  # else:
  #   joystick = pygame.joystick.Joystick(0)
  #   joystick.init()
  #   print("Joysticks found:", joystickCount, "(", joystick.get_name(), ")")
  #   # Get the number of buttons and axes.
  #   buttons = joystick.get_numbuttons()
  #   axes = joystick.get_numaxes()
  #   print("Specs: axes:", axes, ", buttons:", buttons)
  #   print("Press the buttons or rotate the axes!, press CTRL+C to end the script.")
  #   while joystickCount > 0:
  #     print("Joysticks found:", joystickCount)
  #     pygame.joystick.init()
  #     joystickCount = pygame.joystick.get_count()
    

# # See if a joystick or controller is connected.
# if pygame.joystick.get_count() == 0:
#   # No joystick or controller found.
#   print("No joystick or controller found.")
#   exit()

# # Set Broadcom SOC op pinmode
# #GPIO.setmode(GPIO.BCM)
# # Turn off warnings.
# #GPIO.setwarnings(False)
 
# # Set the GPIO pins for the stepper motor:
# #StepPins = [4,17,27,22]
 
# # Set all pins as output.
# #for pin in StepPins:
# #  GPIO.setup(pin,GPIO.OUT)
# #  GPIO.output(pin, False)
 
# joystick = pygame.joystick.Joystick(0)
# joystick.init()
 
# # Joystick or controller information
# print("Joysticks found:", pygame.joystick.get_count(), "(", joystick.get_name(), ")")
# # Get the number of buttons and axes.
# buttons = joystick.get_numbuttons()
# axes = joystick.get_numaxes()
# print("Specs: axes:", axes, ", buttons:", buttons)
# print("Press the buttons or rotate the axes!, press CTRL+C to end the script.")

