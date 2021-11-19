import math

# Electrical Connection details
ML_CHA = 27
ML_CHB = 26
MR_CHA = 13
MR_CHB = 12
EL_CHA = 33
EL_CHB = 25
ER_CHA = 18
ER_CHB = 19
DLED = 2

# Dimensions
L = 0.145 # meters
D = 0.065 # meters

# Encoder Parameters
E_TPR = 1945 // 2 # Ticks Per Rotation
E_RPT = (1/E_TPR) * (2 * math.pi) # Radian Per Ticks

# Tuning Parameter
## Right Motor
WR_MAX = 4
WR_MIN = 1
MIN_OPR = 0.32
GAMMA_R = 50
### PI Gains
KPR = 0.06
KIR = 0.485
### Left Motor
WL_MAX = WR_MAX
WL_MIN = WR_MIN
MIN_OPL = MIN_OPR
GAMMA_L = GAMMA_R
### PI Gains
KPL = KPR
KIL = KIR

## Rates
CONTROL_HZ = 100.0
STATE_ESTIMATE_HZ = 20.0
