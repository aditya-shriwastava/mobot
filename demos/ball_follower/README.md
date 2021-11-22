# Ball Follower
> Robot should follow the ball.
## Steps
1. Detect the ball in the image.
  1. Location (i.e. Location of the center pixel)
  2. Distance (can be obtained from size of the ball)
2. Determine the longitudinal and lateral error wrt ideal ball pose.
3. Set v and w of the robot based on the error.

## Reference
1. [pytank](https://github.com/dac067/pytank/blob/master/houghcircle.py)
2. [How to find HSV range of an Object for Computer Vision applications](https://medium.com/programming-fever/how-to-find-hsv-range-of-an-object-for-computer-vision-applications-254a8eb039fc)
