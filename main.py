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

    def getCurrentSelection(self):
        return self.buttons[self.selectedButtonIndex]

# Define global functions for joystick handling
def onJoyPress(app, button, joystick):
    global currentNumber
    if button == '0':  # 'X' button
        currentNumber = currentNumber[:-1]
    elif button == '1':  # 'A' button
        currentNumber += app.numpad.getCurrentSelection()
    elif button == '2':  # 'B' button
        checkNumber(app)
        currentNumber = ''
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

def onDigitalJoyAxis(app, results, joystick):
    """This handles movement using the left analog stick on a PS4 controller.
    On the arcade box, this is the joystick.
    
    Axis 1 is Up/Down (-1 up, 1 down)
    Axis 0 is Left/Right (-1 left, 1 right)
    So, (1,-1) is up, while (0,1) is right.
    """
    if (1, -1) in results:
        app.numpad.moveSelection(0, 1)
    elif (1, 1) in results:
        app.numpad.moveSelection(0, -1)

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
    app.qrImages = ['QR_corridor.png'] # ['QR1.png', 'QR2.png', 'QR3.png', 'QR4.png']

x = 0
def redrawAll(app):
    global x
    global text
    global currentNumber
    global showQR
    global qrStartTime
    if x == 1:
        x += 1
        currentNumber = currentNumber + app.numpad.getCurrentSelection()
        currentNumber = currentNumber + app.numpad.getCurrentSelection()
        app.numpad.moveSelection(0, 1)
        app.numpad.moveSelection(0, 1)
        currentNumber = currentNumber + app.numpad.getCurrentSelection()
        app.numpad.moveSelection(1, 0)
        app.numpad.moveSelection(1, 0)
        app.numpad.moveSelection(0, -1)
        currentNumber = currentNumber + app.numpad.getCurrentSelection()
        checkNumber(app)

    print("hello world")
    app.numpad.moveSelection(1, 0)
    if showQR:
        currentTime = time.time()
        if currentTime - qrStartTime > 5:
            showQR = False
            currentNumber = ''
        else:
            qrIndex = abs(int((currentTime - qrStartTime) / 7.5) % 4)
            #drawLabel(f"You have 30 seconds to scan this QR code", app.width//2, 50, size=30)
            #drawImage(app.qrImages[qrIndex], 100, 100)
    else:
        app.numpad.draw()
        drawLabel(f"Enter Number: {currentNumber}", app.width//2, 100, size=30)
        drawLabel(f"X to backspace", app.width - app.width//7, 200, size=30)
        drawLabel(f"A to enter num", app.width - app.width//7, 240, size=30)
        drawLabel(f"B to submit", app.width - app.width//7, 280, size=30)
        if text:
            drawLabel(app.text, app.width//2, 150, size=20)

# Initialize the app
runApp(width=800, height=600)