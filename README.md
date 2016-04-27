laser tracking
==============

This project aims at doing an object tracker based on a Raspberry Pi, Raspberry Pi camera, two servos motors and a laser pointer.

The object is recognized with OpenCV analyzing the camera frames.

Then the coordinates of the object are calculated and the laser position estimated.

Then the system rotates the laser so it points towards the object.

Simultaneously tracking the laser position in order to correct any errors in the calculation, since the model is not perfect.
