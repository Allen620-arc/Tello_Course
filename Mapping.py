from djitellopy import tello
import Key_Press_Mod as kp
import numpy as np
from time import sleep
import cv2
import math

########## PARAMETERS ##########
forward_speed = 117 / 10  # Forward Speed in cm/s (15 cm/s)
angle_speed = 360 / 10  # Angular Speed Degrees
interval = 0.25

distance_interval = forward_speed * interval
angle_interval = angle_speed * interval
################################
x, y = 500, 500
angle = 0
yaw = 0

kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())

points = [(0, 0), (0, 0)]

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50
    distance = 0
    global x, y, yaw, angle

    if kp.getKey("LEFT"):
        lr = -speed
        distance = distance_interval
        angle = -180

    elif kp.getKey("RIGHT"):
        lr = speed
        distance = -distance_interval
        angle = 180

    if kp.getKey("UP"):
        fb = speed
        distance = distance_interval
        angle = 270

    elif kp.getKey("DOWN"):
        fb = -speed
        distance = -distance_interval
        angle = -90

    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed

    if kp.getKey("a"):
        yv = speed
        yaw += angle_interval

    elif kp.getKey("d"):
        yv = -speed
        yaw -= angle_interval

    if kp.getKey("q"):
        me.land()
        sleep(1)

    if kp.getKey("e"):
        me.takeoff()

    sleep(interval)
    angle += yaw
    x += int(distance * math.cos(math.radians(angle)))
    y += int(distance * math.sin(math.radians(angle)))

    return [lr, fb, ud, yv, x, y]


me.takeoff()


def drawPoints(img, points):
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, points[-1], 10, (0, 255, 255), cv2.FILLED)
    cv2.putText(img, f'({(points[-1][0] - 500) / 10}, {(points[-1][1] - 500) / 10})m',
                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)

while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    img = np.zeros((1000, 1000, 3), np.uint8)
    if (points[-1][0] != vals[4] or points[-1][1] != vals[5]):
        points.append((vals[4], vals[5]))
    drawPoints(img, points)
    cv2.imshow("Output", img)

    cv2.waitKey(1)
