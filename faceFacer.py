import cams
import driver
import time

speed = 0
steer = 0
ds = -1

while 1:
    positions = cams.getPositions()
    if len(positions):
        pos = positions[0]
        driver.steer(int(pos[1]))
    else:
        if steer<-41 or steer>40:
            ds = -ds
        steer += ds
        driver.steer(steer)
        print(steer)
        time.sleep(.5)
        

