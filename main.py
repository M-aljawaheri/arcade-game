# Import necessary modules
from cmu_graphics import *
import joystick
import sys
import random
import time

currentNumber = ''
text = ''
showQR = False
qrStartTime = 0
qrIndex = 0

# Define the Numpad class
class Numpad:
    def __init__(self, app):
        self.app = app
        self.buttons = [str(i) for i in range(1, 10)] + ['0', '0', '0']
        self.selectedButtonIndex = 0

    def draw(self):
        for i, button in enumerate(self.buttons):
            x = 150 + (i % 3) * 100
            y = 200 + (i // 3) * 100
            if i == self.selectedButtonIndex:
                fillColor = 'yellow'
            else:
                fillColor = 'white'
            drawRect(x, y, 80, 80, fill=fillColor)
            drawLabel(button, x + 40, y + 40, size=30)

    def moveSelection(self, dx, dy):
        row = self.selectedButtonIndex // 3
        col = self.selectedButtonIndex % 3
        row = min(max(row + dy, 0), 2)
        col = min(max(col + dx, 0), 2)
        self.selectedButtonIndex = row * 3 + col
        self.selectedButtonIndex = min(len(self.buttons)-1, max(self.selectedButtonIndex, 0))

    def getCurrentSelection(self):
        return self.buttons[self.selectedButtonIndex]

# Define global functions for joystick handling
def onJoyPress(app, button, joystick):
    global currentNumber
    if button == '3':  # 'Y'
        checkNumber(app)
    elif button == '1':  # 'A' button
        currentNumber += app.numpad.getCurrentSelection()
    elif button == '2':  #   'X'
        currentNumber = currentNumber[:-1]
    elif button == '5':
        sys.exit(0)

def onJoyButtonHold(app, buttons, joystick):
    if 'H0' in buttons:  # Up
        app.numpad.moveSelection(0, -1)
    elif 'H2' in buttons:  # Down
        app.numpad.moveSelection(0, 1)
    if 'H3' in buttons:  # Left
        app.numpad.moveSelection(-1, 0)
    elif 'H1' in buttons:  # Right
        app.numpad.moveSelection(1, 0)


debouncer = time.time()
def onDigitalJoyAxis(app, results, joystick):
    """This handles movement using the left analog stick on a PS4 controller.
    On the arcade box, this is the joystick.
    
    Axis 1 is Up/Down (-1 up, 1 down)
    Axis 0 is Left/Right (-1 left, 1 right)
    So, (1,-1) is up, while (0,1) is right.
    """
    global debouncer
    time_since_debounce = time.time() - debouncer
    if (time_since_debounce > 0.2):
        debouncer = time.time()
    else:
        return

    if (1, -1) in results:
        app.numpad.moveSelection(0, -1)
    elif (1, 1) in results:
        app.numpad.moveSelection(0, 1)

    if (0, -1) in results:
        app.numpad.moveSelection(-1, 0)
    elif (0, 1) in results:
        app.numpad.moveSelection(1, 0)

def checkNumber(app):
    global currentNumber
    global showQR
    global qrStartTime
    global text
    if currentNumber == '1176':
        showQR = True
        qrStartTime = time.time()
    else:
        text = "Wrong number. Try again!"
        currentNumber = ''

def onAppStart(app):
    app.numpad = Numpad(app)
    app.qrImages = ['arcade-1.png', 'arcade-2.png', 'arcade-3.png', 'arcade-4.png']

def onStep(app):
    global text
    global currentNumber
    global showQR
    global qrStartTime
    global qrIndex
    currentTime = time.time()
    if showQR:
        if abs(currentTime - qrStartTime) > 30:
            showQR = False
            currentNumber = ''
            qrIndex = (qrIndex + 1) % len(app.qrImages)

def redrawAll(app):
    global text
    global currentNumber
    global showQR
    global qrStartTime
    global qrIndex

    currentTime = time.time()
    if showQR:
        drawLabel(f"You have {int(currentTime - qrStartTime)} seconds to scan this QR code", app.width//2, 50, size=30)
        drawImage(app.qrImages[qrIndex], 100, 100)
    else:
        app.numpad.draw()
        drawLabel(f"Enter Number: {currentNumber}", app.width//2, 100, size=30)
        drawLabel(f"X to backspace", app.width - app.width//7, 200, size=30)
        drawLabel(f"A to enter num", app.width - app.width//7, 240, size=30)
        drawLabel(f"Y to submit", app.width - app.width//7, 280, size=30)
        if text:
            drawLabel(text, app.width//2, 150, size=20)
            

# Initialize the app
runApp(width=800, height=600)