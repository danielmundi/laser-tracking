Laser Tracking
==============

Goal
----
This project aims at doing an object tracker based on a Raspberry Pi, Raspberry Pi camera, two servos motors and a laser pointer. Where the laser should follow the object identified by the camera.

Dependencies
------------
This project uses a Raspberry Pi 2, OpenCV v3.1, python3.4, raspicamera, NumPy, network connection to a computer (only used to send the camera frames for visualization).

Proceedure
----------
The algorithm tries to identify the object with OpenCV, filtering by color and shape, and then calculate the center point. The one current implemented tries to identify a green retangular object.

The approach chosen is to have a coordinates transformation from the camera view to the angles in the servo motors that control the laser. This way we can just use this transformation on the central point of the object identified and we'll have the values for the angles the servos should be pointing.

With the servo angles calculated, the Raspberry Pi sends a PWM pulse to rotate the servos to the desired position. Which makes the laser point to the target point.

Problems to be solved
---------------------
- The object identification algorithm is not robust, its performance vary a lot with the light conditions, making it impratical for regular use, it needs contant calibration and even so, the performance is still not good.
- In order to have the transformation matrix, it is necessary to calibrate the laser every time the system is moved. Therefore would be good to have an automatic calibration for the system.
- The precision on the servos angle could be improved by using better servos.

Future Improvements
-------------------
Identify the laser with the camera in order to implement a closed loop control that would allow a much better precision on the tracking - considering the servo precision is good enough.
