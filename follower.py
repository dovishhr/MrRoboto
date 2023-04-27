import cams
import driver

speed = 0

while 1:
    positions = cams.getPositions()
    if len(positions):
        pos = positions[0]
        driver.steer(int(pos[1]))
        newSpeed = (pos[0]-4)*6
        if newSpeed > 70:
            newSpeed = 70
        if newSpeed//1 != speed//1:
            speed = newSpeed
            print(speed)
            driver.speed(speed)
    else:
        if speed:
            speed = 0
            driver.speed(speed)


