import time
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
rotate_left = rotate_right = rotate_up = rotate_down = False
x_velocity = y_velocity = 0
rotation_acceleration = 90  # Degrees per second per second
rotation_decceleration = 1.5  # Degrees per second per second

# Main loop
running = True
last_time = time.time()
while running:
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time


    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                rotate_left = True
            elif event.key == K_RIGHT:
                rotate_right = True
            elif event.key == K_UP:
                rotate_up = True
            elif event.key == K_DOWN:
                rotate_down = True
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                rotate_left = False
            elif event.key == K_RIGHT:
                rotate_right = False
            elif event.key == K_UP:
                rotate_up = False
            elif event.key == K_DOWN:
                rotate_down = False

    # Update rotation velocity based on key state and acceleration
    if rotate_left:
        y_velocity -= rotation_acceleration * delta_time
    elif rotate_right:
        y_velocity += rotation_acceleration * delta_time
    else:
        if (y_velocity > 0):
            y_velocity -= min(y_velocity, rotation_decceleration)
        else:
            y_velocity += min(-y_velocity, rotation_decceleration)
        if (-1 < y_velocity < 1):
            y_velocity = 0

    if rotate_up:
        x_velocity -= rotation_acceleration * delta_time
    elif rotate_down:
        x_velocity += rotation_acceleration * delta_time
    else:
        if (x_velocity > 0):
            x_velocity -= min(x_velocity, rotation_decceleration)
        else:
            x_velocity += min(-x_velocity, rotation_decceleration)
        if (-1 < x_velocity < 1):
            x_velocity = 0

    # Apply rotation velocity to angles
    x_angle += x_velocity * delta_time
    y_angle += y_velocity * delta_time

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
