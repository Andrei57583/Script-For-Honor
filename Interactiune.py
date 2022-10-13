from time import time
from DirectInputs import PressKey,ReleaseKey
from DirectInputs import W,A,S,D
from DirectInputs import Right,Left,Up,Num4,Num5
import time

def tap(key):
    PressKey(key)
    time.sleep(0.1)
    ReleaseKey(key)

def switch_guard(directie):
    tap(directie)
    match directie:
        case 200: print("atacul a venit din directia SUS")
        case 203: print("atacul a venit din directia STANGA")
        case 205: print("atacul a venit din directia DREAPTA")
    

def attack(directie):
    switch_guard(directie)
    tap(Num4)

def parry(directie):
    switch_guard(directie)
    tap(Num5)