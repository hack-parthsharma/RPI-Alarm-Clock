# RPi-Alarm-Clock
Raspberry Pi Alarm Clock, using a matrix keypad

A matrix keypad is something like this:

<img src="https://user-images.githubusercontent.com/7780269/46922636-d9ff9b80-d018-11e8-9e1f-14ab2c12b9af.jpg" width="400">

## Usage
1. Config your Raspberry Pi time zone settings, and connect it to a speaker.
2. Clone this repository on your Raspberry Pi.
3.
```
pip install -r requirements.txt
```
4. Connect a matrix keypad to your Raspberry Pi, and config ROW_PINS and COL_PINS in the source code, according to your keypad connection pins.
5.
```
python RPiAlarm.py
```
6. Suppose that you want to set an alarm for 6:05 PM. Type *1805# with your keypad (in *HHMM# format).
7. Wait until the supposed time (18:05) to hear the alarm sound.

<b>Notes:</b>

&bull; You can change the alarm time by repeating the number 6 process, which is mentioned above.<br>
&bull; You can turn off the alarm by just pressing * (star) button.<br>
&bull; By replacing alarm.mp3 file, you can change the alarm sound.
