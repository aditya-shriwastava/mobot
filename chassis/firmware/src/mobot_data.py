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
## Speed Limits
W_MAX = 4
W_MIN = 1

## Right Motor
MIN_OPR = 0.32
GAMMA_R = 50
KPR = 0.06
KIR = 0.485

### Left Motor
MIN_OPL = MIN_OPR
GAMMA_L = GAMMA_R
KPL = KPR
KIL = KIR

## Rates
CONTROL_HZ = 50.0
STATE_ESTIMATE_HZ = 20.0
