# Communication API

```mmd
1. (Mobot App) ---|CMDVEL:wr,wl|--> (Chassis)
2. (Mobot App) ---|GET:"Metadata"|--> (Chassis)
3. (Chassis) --|METADATA:wheel_diameter,wheel_to_wheel_seperation,max_wheel_speed,min_wheel_speed|--> (Mobot App)
```

where, wr, wl, wheel_diameter,wheel_to_wheel_seperation,max_wheel_speed,min_wheel_speed are floats is SI unit. 
- wr: Right wheel angular velocity
- wl: Left wheel angular velocity
- wheel_diameter: Diameter of the wheel
- wheel_to_wheel_seperation: Distance between the wheels
- max_wheel_speed: Maximum wheel angular speed
- min_wheel_speed: Minimum wheel angular speed
