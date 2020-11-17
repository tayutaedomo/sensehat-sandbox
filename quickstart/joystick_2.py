# Reference: https://note.com/agw/n/nc052420f3c37

from sense_hat import SenseHat


sense = SenseHat()

sense.clear()

r = [255,0,0]
b = [0,0,255]
i = [75,0,130]
v = [159,0,255]
e = [0,0,0]
w = [255,255,255]

imageOff = [
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e
]

imageUp = [
    e,e,e,w,e,e,e,e,
    e,e,e,w,e,e,e,e,
    e,e,e,w,e,e,e,e,
    e,e,e,w,w,w,w,e,
    e,e,e,w,e,e,e,e,
    e,e,e,w,e,e,e,e,
    e,e,e,w,e,e,e,e,
    w,w,w,w,w,w,w,w
]

imageDown = [
    r,r,r,r,r,r,r,r,
    e,e,e,r,e,e,e,e,
    e,e,e,r,e,e,e,e,
    e,e,e,r,r,r,r,e,
    e,e,e,r,e,e,e,e,
    e,e,e,r,e,e,e,e,
    e,e,e,r,e,e,e,e,
    e,e,e,r,e,e,e,e
]

imageRight = [
    e,e,e,e,i,e,e,e,
    e,e,e,i,e,e,e,e,
    i,i,i,i,i,i,i,i,
    e,e,i,e,e,e,e,e,
    e,i,e,i,i,i,i,i,
    i,e,e,i,e,e,e,i,
    e,e,e,i,e,e,e,i,
    e,e,e,i,i,i,i,i
]

imageLeft = [
    e,e,e,e,v,e,e,e,
    e,e,e,v,e,e,e,e,
    v,v,v,v,v,v,v,v,
    e,e,v,e,e,e,e,e,
    e,v,e,v,v,v,v,v,
    v,e,e,e,e,v,e,e,
    e,e,e,e,e,v,e,e,
    e,e,e,v,v,v,v,v
]

imageMiddle = [
    e,b,e,b,b,b,b,b,
    b,b,b,b,e,b,e,b,
    e,b,e,b,b,b,b,b,
    e,b,e,b,e,b,e,b,
    e,b,e,b,b,b,b,b,
    e,b,b,e,e,b,e,e,
    b,b,e,e,e,b,e,e,
    e,b,e,e,e,b,e,e
]

chFlg = 0
image = imageOff

while chFlg >= 0:
    for event in sense.stick.get_events():
        print(event.direction, event.action)
        if event.direction == "down":
            image = imageDown
            chFlg = 1
        if event.direction == "up":
            image = imageUp
            chFlg = 1
        if event.direction == "right":
            image = imageRight
            chFlg = 1
        if event.direction == "left":
            image = imageLeft
            chFlg = 1
        if event.direction == "middle":
            chFlg = -1
        if chFlg != 0:
            sense.clear()
        if chFlg == 1:
            sense.set_pixels(image)
            chFlg = 0

