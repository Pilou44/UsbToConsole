#!/usr/bin/env python

from actions import *

name = "Xbox 360 Controller"
guid = "030000005e0400008e02000014010000"
sega_md = { 
"2" : BTN_A, "0" : BTN_B, "1" : BTN_C_L, 
"4" : BTN_X, "3" : BTN_Y, "5" : BTN_Z_R, 
"7" : BTN_START, "6" : BTN_MODE_SELECT,
"0_1_-1" : LEFT,  
"0_1_1" : RIGHT, 
"0_1_0" : RELEASE_H, 
"0_2_1" : UP, 
"0_2_-1" : DOWN, 
"0_2_0" : RELEASE_V,
 }
snes = { 
"1" : BTN_A, "0" : BTN_B, 
"3" : BTN_X, "2" : BTN_Y, 
"4" : BTN_C_L, "5" : BTN_Z_R, 
"7" : BTN_START, "6" : BTN_MODE_SELECT,
"0_1_-1" : LEFT,  
"0_1_1" : RIGHT, 
"0_1_0" : RELEASE_H, 
"0_2_1" : UP, 
"0_2_-1" : DOWN, 
"0_2_0" : RELEASE_V,
 }
