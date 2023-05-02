# Travis Morwood
# Mr. Roboto Defense

## The problem:

There are often obstacles within the operating space of vehicles, and most standard vehicles have no way to detect those obstacles, and avoid them on their own. When the vehicles cannot see the obstacles, they are unable to avoid them during operation, thus almost guaranteeing that those vehicles will at one point or another collide with the obstacles in their operating zone. These collisions can be very costly and even life threatening, depending on the speed of the vehicle, and composition of the obstacle. 

## My solution:

Provide a proof of concept the vehicles with a way to overcome that limitation by attaching dual optical sensors to the front of it. Then give it a brain to be able to process the images that it sees, and control over its forward/backward motion, and steering angle. Thus providing it with the means to detect objects, and avoid them.

## Demo:
https://youtu.be/nlP1j-2fDnc

## Technical Overview:

The technologies I used include:
### Remote Control Car
Cheaper than a big one, also less expensive when it crashes into things
Used as a base for all the other electronic components
### Raspberry Pi 4
I used one as the brain for the car, it ran all the software that controlled all of the components.
### Pair of Webcams
The eyes for the car, I use them to triangulate the location of the objects
Various other electronic components:
Motor controllers, power converters, I changed out the steering servo, and other things.
### Rpi.GPIO
I used this to send WPM signals to the servo motor as well as the drive motor controller, to allow for control over the steer angle as well as vehicle speed.
### OpenCV
I used this to manage all of the camera and image processing, it scans from the camera, and uses facial detection to look for any faces within the images individually.
It then reports back the local positions of the faces within their respective frames.

### Python
I used python to stitch together all the previous components, as well as doing the math for the triangulation of the objects. 
Also used to make the decisions on what to do with that information, such as dodging, or trying to follow it

## Framework setup:
### cams.py 
The main goal of this file is to handle everything to do with the cameras.
The most important thing within it is the function that produces the vector of positions of the objects, relative to the car itself.
Get positions uses some helper functions:
 get distances, which sort the objects by perceived size, and then uses the angles off of each camera to triangulate and calculate a distance value for each object.
Get headings, which basically just converts the pixel position of the objects to local angles, and then averages the two to give it a heading of the object.
Several other helper functions that help with the above
### Driver.py
This file is for handling all things motion
Motor class that is used for motor control, as I was using PWM for both steering motor and drive motor, this made it easier.
DriveMotor class is used to overwrite the set function of the motor class so that the PWM can be manipulated to be high on one pin and low on the other for forward driving, and vice versa for reverse driving, it does this by taking in Motor object for each wire that needs to be controlled by PWM.
It then has simple functions that can be called to steer and set the speed of the car.
	Once this all was done, creating different driving algorithms became simple
	See the Demos for explanations of the implemented algorithms.
