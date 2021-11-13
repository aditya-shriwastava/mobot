# Communication API
```mmd
graph LR;
  a(mobot-android) -->|'CMDVEL:v,w\r'| b(mobot-chassis);
  b -->|'ODOM:x,y,yaw\r'| a;
```
where, v, w, x, y, & yaw are floats is SI unit. 
- v: Translation Velocity
- w: Rotation Velocity
- x: x-coordinate of position
- y: y-coordinate of position
- yaw: rotation about z-axis
