import math

# Electrical Connection details
ML_CHA = 26
ML_CHB = 27
MR_CHA = 13
MR_CHB = 12
EL = 33
ER = 25
DLED = 2

# Dimensions
L = 0.145 # meters
D = 0.065 # meters

# Encoder Parameters
E_TPR = 40 # Ticks Per Rotation
E_RPT = (1/E_TPR) * (2 * math.pi) # Radian Per Ticks

# Tuning Parameter
## PI Gains for Motor Contorl
KP = 0.015
KI = 0.4
## Rates
CONTROL_HZ = 100.0
STATE_ESTIMATE_HZ = 10.0
