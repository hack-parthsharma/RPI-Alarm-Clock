from pad4pi import rpi_gpio
from datetime import datetime
from datetime import timedelta
from time import sleep
from playsound import playsound
import RPi.GPIO as GPIO


ALARM_SOUND_FILE_PATH = "alarm.mp3"
ALARM_DURATION = timedelta(minutes=5)
OUTPUT_PIN_NUMBER = 21 #BCM, will be turn on for alarm
ALARM_ON_PIN_NUMBER = 20 #BCM, indicates whether alarm is on or not
TIME_CHECK_PERIOD = 1 #seconds
KEYPAD = [
  ["1", "2", "3"],
  ["4", "5", "6"],
  ["7", "8", "9"],
  ["*", "0", "#"]
]
ROW_PINS = [4, 14, 15, 17] #BCM
COL_PINS = [18, 27, 22] #BCM

factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

keypad_str = ""
start_alarm_time = None
end_alarm_time = None
is_alarm_on = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(OUTPUT_PIN_NUMBER, GPIO.OUT, initial=0)
GPIO.setup(ALARM_ON_PIN_NUMBER, GPIO.OUT, initial=0)


def set_is_alarm_on(value):
  global is_alarm_on
  is_alarm_on = value
  if is_alarm_on:
    GPIO.output(ALARM_ON_PIN_NUMBER, GPIO.HIGH)
  else:
    GPIO.output(OUTPUT_PIN_NUMBER, GPIO.LOW)
    GPIO.output(ALARM_ON_PIN_NUMBER, GPIO.LOW)


def set_alarm_time(time_str):
  global start_alarm_time
  global end_alarm_time
  try:
    start_alarm_time = datetime.strptime(time_str, "%H%M")
    if start_alarm_time < datetime.now():
      start_alarm_time = start_alarm_time + timedelta(days=1)
    end_alarm_time = datetime.strptime(time_str, "%H%M") + ALARM_DURATION
    set_is_alarm_on(True)
  except:
    set_is_alarm_on(False)


def set_interrupts():
  keypad.registerKeyPressHandler(on_key_press)


def cleanup():
  GPIO.output(OUTPUT_PIN_NUMBER, GPIO.LOW)
  GPIO.cleanup()
  keypad.cleanup()


def wait_for_alarm():
  global is_alarm_on
  while True:
    sleep(TIME_CHECK_PERIOD)
    now_time = datetime.now().time()
    if is_alarm_on and start_alarm_time and end_alarm_time:
      if now_time.hour == start_alarm_time.time().hour and now_time.minute == start_alarm_time.time().minute:
        GPIO.output(OUTPUT_PIN_NUMBER, GPIO.HIGH)
      elif now_time.hour == end_alarm_time.time().hour and now_time.minute == end_alarm_time.time().minute:
        GPIO.output(OUTPUT_PIN_NUMBER, GPIO.LOW)
        playsound(ALARM_SOUND_FILE_PATH)
        set_is_alarm_on(False)


def on_key_press(key):
  global keypad_str
  if key == "*":
    set_is_alarm_on(False)
    keypad_str = ""
  elif key == "#":
    set_alarm_time(keypad_str)
  else:
    keypad_str = keypad_str + key
    if len(keypad_str) > 4:
      keypad_str = ""


set_interrupts()
try:
  wait_for_alarm()
except:
  cleanup()
