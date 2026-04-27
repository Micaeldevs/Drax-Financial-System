import pyautogui
from time import sleep
import subprocess

subprocess.Popen(["python", "main.py"])
pyautogui.PAUSE = 1


pyautogui.click(809, 1404)
pyautogui.typewrite("1")

pyautogui.press("enter")
pyautogui.typewrite("1")

pyautogui.press('enter')
pyautogui.typewrite('Seguro')
pyautogui.press('enter')
pyautogui.typewrite('550a')
pyautogui.press('enter')
pyautogui.typewrite('550')
pyautogui.press('enter')
#sleep(2)
#print(pyautogui.position())