import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

import joystick



# Initialize Pygame
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Perspective setup
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# Cube vertices and edges
vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, 1, 1),
    (-1, -1, 1),
)

edges = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7)
)

# Function to draw the cube
def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

x_angle = 0
y_angle = 0

# Main loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                y_angle -= 5
            if event.key == pygame.K_RIGHT:
                y_angle += 5
            if event.key == pygame.K_UP:
                x_angle -= 5
            if event.key == pygame.K_DOWN:
                x_angle += 5


    # Clear the screen and depth buffer
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    # Reset transformations and set the rotation
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glRotatef(x_angle, 1, 0, 0)  # Rotate up or down
    glRotatef(y_angle, 0, 1, 0)  # Rotate left or right

    # Draw the cube
    Cube()

    # Swap the display buffers
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()

def onJoyPress(app, button, joystick):
    if button == '5':
        sys.exit(0)

def onJoyRelease(app, button, joystick):
    """Tells you when a button is released on which joystick"""
    print(f"Joystick {joystick} button released: {button}")


def onJoyButtonHold(app, buttons, joystick):
    pass

def onDigitalJoyAxis(app, results, joystick):
    """This handles movement using the left analog stick on a PS4 controller.
    On the arcade box, this is the joystick.

    Axis 1 is Up/Down (-1 up, 1 down)
    Axis 0 is Left/Right (-1 left, 1 right)
    So, (1,-1) is up, while (0,1) is right.
    """
    app.text = f"Joystick {joystick} axis being held: {results}"
    if (1, -1) in results:      # up
        y_angle += 5
    elif (1, 1) in results:     # down
        y_angle -=5

    if (0, -1) in results:      # left
        # Apply rotation
        x_angle -=5
    elif (0, 1) in results:     # right
        # Apply rotation
        x_angle += 5



