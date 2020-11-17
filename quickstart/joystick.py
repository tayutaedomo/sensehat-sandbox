# Reference: https://note.com/agw/n/nc052420f3c37

from sense_hat import SenseHat

sense = SenseHat()

sense.clear()

x = 3
y = 3
sense.set_pixel(x,y,100,100,100)

VMAX = 7
VMIN = 0

colNo = 0
cols = [
    [200,0,0],
    [0,200,0],
    [0,0,200]
]

chFlg = 0
while chFlg >= 0:
    for event in sense.stick.get_events():
        print(event.direction, event.action)
        if event.direction == "down":
            if y < VMAX:
                y += 1
                chFlg = 1
        if event.direction == "up":
            if y > VMIN:
                y -= 1
                chFlg = 1
        if event.direction == "right":
            if x < VMAX:
                x += 1
                chFlg = 1
        if event.direction == "left":
            if x > VMIN:
                x -= 1
                chFlg = 1
        if event.direction == "middle":
            chFlg = -1
        if chFlg != 0:
            sense.clear()
        if chFlg == 1:
            sense.set_pixel(x,y,cols[colNo][0],cols[colNo][1],cols[colNo][2])
            chFlg = 0

