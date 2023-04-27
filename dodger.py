import cams
import driver
import sys
import time 

print(sys.argv)
driver.speed(int(sys.argv[2]))

for _ in range(int(sys.argv[1])):
    positions = cams.getPositions()
    if len(positions):
        pos = positions[0]
        if int(pos[1])>0:#right
            driver.steer(-35)
            print(-int(pos[1])+int(pos[0]))
            time.sleep(0.5)
            driver.steer(0)
        else:#left
            print(-int(pos[1])+int(pos[0]))
            driver.steer(40)
            time.sleep(0.5)
            driver.steer(0)
    #else:
        #driver.steer(0)

driver.speed(0)
